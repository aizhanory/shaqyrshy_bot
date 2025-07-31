# Shaqyrshy Bot

**Shaqyrshy Bot** is a private Telegram assistant bot created for a small student group.  
It helps manage academic routines like schedules, deadlines, and exams in a friendly and minimal interface.

---

## ⚙️ Features

- 📅 `/schedule` – View the weekly class schedule
- 📁 `/deadlines` – See all active deadlines with countdowns
- 🎓 `/exams` – View upcoming midterms and final exams
- 📣 `/call` – Mention all members manually or by using trigger words like “шакырш”
- 🔔 Auto deadline watcher – Notifies the group when a deadline expires and removes it
- 🔐 Admin-only access in private for editing data

---

## 📂 Project Structure

```
📁 shaqyrshy_bot/
├── .venv/                         # Virtual Environment 
├── handlers/
│   ├── group/                    # Group commands
│   │   ├── call.py
│   │   ├── notify.py
│   │   ├── notify_deadline_end.py
│   │   └── __init__.py
│   └── private/                  # Private commands (for owner only)
│       ├── flows/
│       │   ├── add_deadline.py
│       │   ├── add_exam.py
│       │   ├── add_schedule.py
│       │   ├── crud_handler.py
│       │   ├── delete_flow.py
│       │   ├── edit_flow.py
│       │   ├── show_all.py
│       │   ├── start.py
│       │   └── __init__.py
│       └── __init__.py
├── keyboards/
│   ├── confirm_cancel.py
│   ├── menu.py
│   ├── section_menus.py
│   └── __init__.py
├── storage/                      # JSON Storage and States
│   ├── deadlines.json
│   ├── exams.json
│   ├── json_helpers.py
│   ├── schedule.json
│   ├── selected_section.py
│   ├── user_state.py
│   └── __init__.py
├── .env                          # Environment variables
├── commands.py                   # Menu commands
├── config.py                     # Settings, token, ID and paths
├── hybrid_middleware.py          # Middleware for Handler Distribution
├── main.py                       # Entry point to the bot
├── requirements.txt              # Project dependencies
└── README.md                     # Documentation (you are here!)
```

---

## ⚙️ Tech Stack

- Python 3.10+
- Aiogram v3
- APScheduler
- Pytz
- JSON (for local storage)

---

## ▶︎ Running the Bot

1. Clone the repo  
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create new file `.env` and write there:
   ```python
   BOT_TOKEN = # your_bot_token
   ALLOWED_CHAT_ID = # will be updated later
   ADMIN_ID =  # will be updated later
   ```

4. Run:
   ```bash
   python main.py
   ```

5.	Get your chat and user IDs
- Add the bot to your Telegram group.
- Your terminal will print chat_id and user_id.
- Copy them and update your `.env`

6.  Restart the bot
    ```bash
    python main.py
    ```

---

## 🔒 Note

This bot is **private** and tailored specifically for use by a single Telegram group.
It is not designed for public deployment or multi-group support (yet).

