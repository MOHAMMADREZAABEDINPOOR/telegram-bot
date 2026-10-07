<div align="center">

<img src="assets/readme/hero.gif" width="1200" alt="GEMINI TELEGRAM BOT — rotating 3D geometry" />

**[English](README.md) · [فارسی](README.fa.md)**

<img src="assets/readme/identity.svg" width="1200" alt="ai / English and Persian documentation" />

</div>

# GEMINI TELEGRAM BOT

A compact Telegram long-polling bot that sends user text to the Gemini REST API and applies a system prompt loaded from a local text file.

[GitHub](https://github.com/MOHAMMADREZAABEDINPOOR/telegram-bot) · [PIMX / Profile](https://github.com/MOHAMMADREZAABEDINPOOR) · [Static artwork](assets/readme/hero.png)

## Features

- Telegram getUpdates polling and update offset tracking
- Gemini generateContent requests through requests
- Editable UTF-8 system_prompt.txt
- Typing status, text replies and error handling

## Stack

| Tool | Version / source |
|---|---|
| requests==2.32.3 | `requirements.txt` |

## Getting started

Python 3; a desktop/Tk installation for Tkinter or turtle examples. Tkinter is provided by the Python installation, not pip. Legacy dependencies may need a compatible Python version.

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

Credentials are read from process environment variables or a local `.env` file. `.env.example` is a template; copy it to `.env` and fill in your own values.

## Configuration

These names are found in the example configuration or source; not all are required. Check their defaults/usage in those files and supply secrets only in your local or hosting environment.

| Name | Role |
|---|---|
| `GEMINI_API_KEY` | Credential/connection setting; keep private |
| `TELEGRAM_BOT_TOKEN` | Credential/connection setting; keep private |

## Usage

Copy .env.example to .env, set TELEGRAM_BOT_TOKEN and GEMINI_API_KEY, customize system_prompt.txt and run bot.py. Process environment variables take precedence over the local file.

## Project structure

| Path | Role |
|---|---|
| [`assets/`](assets/) | Brand/media/README assets |
| [`bot.py`](bot.py) | Project entry/configuration file |

## Commands and checks

No automated test command is declared in a manifest. Verify behavior through a local example run.

## Deployment

Host a long-running bot process with environment secrets and private storage. Run a single polling instance. Check network access and dependency compatibility on the host.

## Limitations

Requests are handled sequentially and require network access. The bot does not provide persistent multi-turn memory. If polling conflicts with an existing webhook or another instance, stop that instance/remove the webhook first.

## Troubleshooting

- Authentication/provider errors: verify credentials and selected model/provider.
- No Telegram updates: check polling/webhook mode and concurrent bot instances.
- Missing dependencies: use the declared manifest or inspect imports if no manifest is provided.

## Contributing

Create a focused branch, verify the affected behavior and explain the change clearly. Keep private data, build outputs and local databases out of commits.

## License

No repository-level license file is included in this snapshot. Public visibility alone does not grant reuse rights; contact the repository owner for terms.

---

Part of **PIMX** · Documentation in English and Persian.
