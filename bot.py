import logging
import os
import time
from pathlib import Path
from typing import Optional

import requests

# Local secrets stay beside this script and outside version control.
_environment_path = Path(__file__).with_name(".env")
if _environment_path.is_file():
    for _line in _environment_path.read_text(encoding="utf-8").splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _name, _value = _line.split("=", 1)
            os.environ.setdefault(_name.strip(), _value.strip().strip("\"'"))

# ==========================
#  تنظیمات و مقادیر ثابت
# ==========================

# توکن ربات تلگرام
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

# کلید API جمنای
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# نام مدل جمنای که استفاده می‌کنیم
GEMINI_MODEL_NAME = "gemini-2.5-flash"

# نام فایل سیستم‌پرامپت (پرامپت ثابت که همیشه قبل از متن کاربر به مدل داده می‌شود)
SYSTEM_PROMPT_FILE = str(Path(__file__).with_name("system_prompt.txt"))

# آدرس پایه‌ی API تلگرام با توکن ربات
TELEGRAM_API_BASE = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# آدرس REST API جمنای برای متد generateContent
GEMINI_API_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"
)

# تنظیم لاگینگ برای نمایش لاگ‌ها در ترمینال
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def load_system_prompt() -> str:
    """
    خواندن متن سیستم‌پرامپت از فایل متنی.
    اگر فایل وجود نداشته باشد، یک رشته خالی برگردانده می‌شود.
    """
    path = Path(SYSTEM_PROMPT_FILE)
    if not path.exists():
        logger.warning("فایل %s پیدا نشد. سیستم‌پرامپت خالی استفاده می‌شود.", SYSTEM_PROMPT_FILE)
        return ""
    return path.read_text(encoding="utf-8").strip()


# متن سیستم‌پرامپت را فقط یک‌بار در شروع برنامه می‌خوانیم
SYSTEM_PROMPT = load_system_prompt()


def call_gemini(user_text: str) -> str:
    """
    ارسال درخواست به REST API جمنای با استفاده از کتابخانه requests.
    متن سیستم‌پرامپت (در صورت وجود) قبل از متن کاربر به مدل داده می‌شود.
    """
    try:
        # اگر سیستم‌پرامپت وجود دارد، آن را همراه با متن کاربر به مدل می‌فرستیم
        if SYSTEM_PROMPT:
            final_text = f"{SYSTEM_PROMPT}\n\n---\nUser: {user_text}"
        else:
            final_text = user_text

        # بدنه‌ی JSON مطابق فرمت مورد انتظار مدل Gemini
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": final_text}],
                }
            ]
        }

        # ارسال درخواست POST به سرور جمنای
        resp = requests.post(GEMINI_API_URL, json=payload, timeout=30)
        if resp.status_code != 200:
            # اگر کد وضعیت HTTP غیر از ۲۰۰ بود، لاگ خطا و پیام مناسب برمی‌گردانیم
            logger.error("Gemini HTTP %s: %s", resp.status_code, resp.text)
            return f"خطای Gemini (HTTP {resp.status_code})"

        data = resp.json()

        # استخراج متن پاسخ از ساختار استاندارد خروجی مدل Gemini
        candidates = data.get("candidates", [])
        if not candidates:
            return "پاسخی از Gemini دریافت نشد."

        content = candidates[0].get("content", {})
        parts = content.get("parts", [])
        texts = [p.get("text", "") for p in parts if isinstance(p, dict)]
        answer = "\n".join(t for t in texts if t).strip()
        return answer or "پاسخی از Gemini دریافت نشد."

    except Exception as exc:  # pylint: disable=broad-except
        # هر خطای غیرمنتظره‌ای را لاگ می‌کنیم و متن خطا را برای کاربر می‌فرستیم
        logger.exception("خطا در تماس با Gemini: %s", exc)
        return f"خطا در ارتباط با Gemini: {exc}"


def send_telegram_message(chat_id: int, text: str) -> None:
    """
    ارسال یک پیام متنی ساده به چت تلگرام با استفاده از متد sendMessage.
    """
    try:
        requests.post(
            f"{TELEGRAM_API_BASE}/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=20,
        )
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("خطا در ارسال پیام تلگرام: %s", exc)


def send_chat_action(chat_id: int, action: str = "typing") -> None:
    """
    ارسال وضعیت (مثل typing) به تلگرام تا کاربر ببیند ربات در حال نوشتن است.
    """
    try:
        requests.post(
            f"{TELEGRAM_API_BASE}/sendChatAction",
            json={"chat_id": chat_id, "action": action},
            timeout=20,
        )
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("خطا در ارسال اکشن تلگرام: %s", exc)


def handle_update(update: dict) -> None:
    """
    پردازش یک آپدیت تلگرام.
    فقط روی پیام‌های متنی کار می‌کنیم و بقیه انواع آپدیت را نادیده می‌گیریم.
    """
    # از داخل آپدیت، شیء message را می‌گیریم
    message = update.get("message")
    if not message:
        return

    # مشخصات چت (برای گرفتن chat_id) و متن پیام
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    text = message.get("text")

    # اگر chat_id یا متن پیام نداشتیم، کاری نمی‌کنیم
    if chat_id is None or text is None:
        return

    logger.info("پیام از %s: %s", chat_id, text)

    # به کاربر نشان می‌دهیم که ربات در حال تایپ است
    send_chat_action(chat_id, "typing")

    # ارسال متن کاربر به جمنای و دریافت پاسخ
    answer = call_gemini(text)

    # فرستادن پاسخ مدل به تلگرام
    send_telegram_message(chat_id, answer)


def get_updates(offset: Optional[int] = None, timeout: int = 30) -> list[dict]:
    """
    گرفتن آپدیت‌ها از تلگرام با روش long polling.
    offset باعث می‌شود آپدیت‌های تکراری دوباره دریافت نشوند.
    """
    params: dict = {"timeout": timeout}
    if offset is not None:
        params["offset"] = offset

    resp = requests.get(f"{TELEGRAM_API_BASE}/getUpdates", params=params, timeout=timeout + 5)
    if resp.status_code != 200:
        logger.error("Telegram getUpdates HTTP %s: %s", resp.status_code, resp.text)
        return []

    data = resp.json()
    if not data.get("ok"):
        logger.error("Telegram getUpdates not ok: %s", data)
        return []

    # لیست آپدیت‌ها را برمی‌گردانیم
    return data.get("result", [])


def main() -> None:
    if not TELEGRAM_BOT_TOKEN or not GEMINI_API_KEY:
        raise RuntimeError("Set TELEGRAM_BOT_TOKEN and GEMINI_API_KEY in .env or the process environment")
    """
    حلقه اصلی ربات تلگرام.
    به صورت مداوم از تلگرام getUpdates می‌گیرد و هر آپدیت را پردازش می‌کند.
    """
    logger.info("ربات استارت شد و در حال polling است (بدون کتابخانه اضافی).")
    last_update_id: Optional[int] = None  # آخرین آیدی آپدیتی که پردازش شده

    while True:
        try:
            # اگر last_update_id داشتیم، از آپدیت بعدی به بعد را می‌گیریم
            updates = get_updates(offset=last_update_id + 1 if last_update_id else None)

            for upd in updates:
                # به‌روزرسانی آخرین آیدی پردازش‌شده
                upd_id = upd.get("update_id")
                if upd_id is not None:
                    last_update_id = upd_id

                # پردازش خود آپدیت (اگر پیام متنی بود پاسخ می‌دهیم)
                handle_update(upd)

        except KeyboardInterrupt:
            # اگر در ترمینال Ctrl+C بزنیم، به شکل تمیز از حلقه خارج می‌شویم
            logger.info("خروج با Ctrl+C")
            break
        except Exception as exc:  # pylint: disable=broad-except
            # هر خطایی در حلقه اصلی را لاگ می‌کنیم و چند ثانیه صبر می‌کنیم
            logger.exception("خطای عمومی در حلقه اصلی: %s", exc)
            time.sleep(5)


if __name__ == "__main__":
    # شروع اجرای برنامه از اینجا
    main()

