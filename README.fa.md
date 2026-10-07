<div align="center">

<img src="assets/readme/hero.gif" width="1200" alt="GEMINI TELEGRAM BOT: a conversational assistant with two Gemini-colored stars" />

**[English](README.md) · [فارسی](README.fa.md)**

</div>

<div dir="rtl">

# ✨ GEMINI TELEGRAM BOT

ربات کوچک تلگرام با long polling که متن کاربر را به REST API جمنای می‌فرستد و پرامپت ثابت را از فایل متنی می‌خواند.

[GitHub](https://github.com/MOHAMMADREZAABEDINPOOR/telegram-bot) · [PIMX / Profile](https://github.com/MOHAMMADREZAABEDINPOOR) · [بنر ثابت](assets/readme/hero.png)

| نمای کلی | جزئیات |
|:---|:---|
| ✨ تجربه | ربات تلگرام و ابزارهای همراه آن |
| 🧰 فناوری | `requests==2.32.3` |
| 🌐 زبان راهنما | [English](README.md) · [فارسی](README.fa.md) |

[✨ امکانات](#امکانات) · [🚀 شروع کار](#شروع-کار) · [⚙️ تنظیمات](#تنظیمات) · [🌍 استقرار](#استقرار)

---

<a id="امکانات"></a>

## ✨ امکانات

| بخش | قابلیت موجود |
|:---|:---|
| ⚡ روند کار | پایش getUpdates و نگهداری offset پیام |
| 🧠 هوشمندی | درخواست generateContent جمنای با requests |
| ⚡ روند کار | فایل قابل ویرایش UTF-8 با نام system_prompt.txt |
| ⚡ روند کار | وضعیت تایپ، پاسخ متنی و مدیریت خطا |

<a id="پشته-فنی"></a>

## 🧰 پشته فنی

| ابزار | نسخه یا منبع |
|---|---|
| requests==2.32.3 | `requirements.txt` |

<a id="شروع-کار"></a>

## 🚀 شروع کار

Python 3 و محیط دسکتاپ برای پروژه‌های Tkinter/Turtle؛ Tkinter از اجزای نصب Python است و با pip نصب نمی‌شود. برای وابستگی‌های قدیمی از نسخه Python سازگار استفاده کنید.

<div dir="ltr">

```bash
git clone https://github.com/MOHAMMADREZAABEDINPOOR/telegram-bot.git
cd telegram-bot

python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1; macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
# PowerShell: $env:TELEGRAM_BOT_TOKEN = "your-token"
# PowerShell: $env:GEMINI_API_KEY = "your-key"
# macOS/Linux: export TELEGRAM_BOT_TOKEN="your-token" GEMINI_API_KEY="your-key"
python bot.py
```

</div>

اعتبارنامه از محیط یا فایل محلی `.env` خوانده می‌شود. `.env.example` فقط نمونه است؛ آن را به `.env` کپی و مقدارها را تنظیم کنید.

<a id="تنظیمات"></a>

## ⚙️ تنظیمات

کلیدهای زیر از فایل نمونه یا کد استخراج شده‌اند؛ همه الزاماً اجباری نیستند. مقدار و پیش‌فرض را در همان فایل بررسی و اسرار را فقط در محیط محلی یا هاست تنظیم کنید.

| نام | کاربرد |
|---|---|
| `GEMINI_API_KEY` | اعتبارنامه یا اتصال؛ خصوصی نگه دارید |
| `TELEGRAM_BOT_TOKEN` | اعتبارنامه یا اتصال؛ خصوصی نگه دارید |

<a id="استفاده"></a>

## 🎯 استفاده

فایل .env.example را به .env کپی، TELEGRAM_BOT_TOKEN و GEMINI_API_KEY را تنظیم، system_prompt.txt را ویرایش و bot.py را اجرا کنید. متغیر محیط فرایند بر فایل محلی اولویت دارد.

<a id="ساختار-پروژه"></a>

## 🗂️ ساختار پروژه

| مسیر | نقش |
|---|---|
| [`assets/`](assets/) | فایل برند، رسانه و README |
| [`bot.py`](bot.py) | فایل ورودی یا تنظیم پروژه |

<a id="فرمان‌ها-و-بررسی"></a>

## 🧪 فرمان‌ها و بررسی

فرمان آزمون خودکار در manifest تعریف نشده است. اجرای محلی و بررسی رفتار نمونه را انجام دهید.

<a id="استقرار"></a>

## 🌍 استقرار

ربات را با فرایند پایدار، اسرار محیطی و فضای ذخیره خصوصی میزبانی کنید. تنها یک نمونه polling اجرا کنید. تنظیم شبکه و نسخه وابستگی را روی هاست بررسی کنید.

<a id="محدودیت‌ها"></a>

## 📌 محدودیت‌ها

درخواست‌ها ترتیبی هستند و اینترنت لازم است. ربات حافظه دائمی چندنوبتی ندارد. در تداخل polling با وب‌هوک یا نمونه دیگر، ابتدا نمونه دیگر یا وب‌هوک را متوقف کنید.

<a id="رفع-مشکل"></a>

## 🛠️ رفع مشکل

- خطای سرویس یا ورود: اعتبارنامه و مدل و سرویس انتخابی را بررسی کنید.
- پیام تلگرام نمی‌رسد: حالت polling و وب‌هوک و نمونه همزمان را بررسی کنید.
- وابستگی غایب: از manifest استفاده یا در نبود آن importها را بررسی کنید.

<a id="مشارکت"></a>

## 🤝 مشارکت

برای تغییر، شاخه مستقل بسازید، رفتار فعلی را بررسی کنید و توضیح روشن همراه تغییر بفرستید. اطلاعات خصوصی، خروجی build و دیتابیس محلی را commit نکنید.

<a id="مجوز"></a>

## 📄 مجوز

فایل مجوز در این نسخه موجود نیست. نمایش عمومی کد به‌تنهایی مجوز استفاده مجدد نیست؛ برای شرایط استفاده با مالک مخزن هماهنگ کنید.

---

ساخته‌شده در مجموعه **PIMX** · مستندات فارسی و انگلیسی.

---

<div align="center">

✨ **GEMINI TELEGRAM BOT** · [English](README.md) · [فارسی](README.fa.md)

</div>

</div>
