# 🚀 Noones Telegram Bot

This is a Python-based Telegram bot integrated with the [Noones](https://noones.com) API to automate P2P trading. It sends automated messages to buyers and notifies you via Telegram when a new trade is initiated.

## 📦 Features

- Automatically detects new `ACTIVE` trades
- Sends a welcome message and bank payment details
- Sends Telegram notifications with buyer info
- Flask app for deployment health checks

## 🔧 Environment Variables

| Variable           | Description                              |
|--------------------|------------------------------------------|
| `API_KEY`          | Your Noones API key                      |
| `API_SECRET`       | Your Noones API secret                   |
| `TELEGRAM_TOKEN`   | Your Telegram bot token                  |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID to receive alerts |
| `PORT`             | (Optional) Port for Flask app (default: 5000) |

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/noones-telegram-bot.git
cd noones-telegram-bot
