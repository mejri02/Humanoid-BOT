```markdown
# 🤖 Humanoid Auto BOT

> Automated solution for Humanoid Network airdrop farming with multi-account support

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Proxy Recommendation](#proxy-recommendation)
- [Support](#support)

## 🎯 Overview

Humanoid Auto BOT is an automated tool designed for efficient airdrop farming on the Humanoid Network. It automates account management, task completion, and training submissions across multiple accounts with built-in proxy support.

**🔗 Get Started:** [Register on Humanoid](https://prelaunch.humanoidnetwork.org/ref/E2YE9U)

> **Important:** Use new EVM wallets for best results.

## ✨ Features

- 🔐 **Secure Authentication** - Automatic wallet authentication with nonce signing
- 📊 **Multi-Account Management** - Process multiple accounts in sequence
- 🌐 **Proxy Support** - HTTP/HTTPS/SOCKS4/SOCKS5 proxy compatibility
- 🔄 **Smart Proxy Rotation** - Automatic rotation for invalid proxies
- 🏋️ **Auto Training Submission** - Automatically scrape and submit models/datasets from HuggingFace
- ✅ **Task Automation** - Complete all available tasks automatically
- 📈 **Points Tracking** - Real-time points monitoring
- 🕐 **Scheduled Execution** - 12-hour automatic cycle

## 📋 Requirements

- **Python:** Version 3.9 or higher
- **Required Libraries:**
  - aiohttp
  - aiohttp-socks
  - fake-useragent
  - eth-account
  - eth-utils
  - colorama
  - pytz

## 🛠 Installation

### 1. Prepare Your Environment

Create a project folder and navigate to it:

```bash
mkdir Humanoid-BOT
cd Humanoid-BOT
```

2. Create Requirements File

Create a file named requirements.txt with the following content:

```txt
aiohttp==3.9.1
aiohttp-socks==0.8.4
fake-useragent==1.4.0
eth-account==0.11.0
eth-utils==2.3.1
colorama==0.4.6
pytz==2024.1
```

3. Install Dependencies

```bash
pip install -r requirements.txt
```

⚙️ Configuration

Account Setup

Create accounts.txt file and add your wallet private keys (one per line):

```
0xYourPrivateKey1
0xYourPrivateKey2
0xYourPrivateKey3
```

Proxy Setup (Optional)

Create proxy.txt file and add your proxies:

```
# Simple format
ip:port

# With protocol
http://ip:port
https://ip:port
socks5://ip:port

# With authentication
http://username:password@ip:port
```

🚀 Usage

1. Save the bot code as bot.py in your project folder
2. Run the bot:

```bash
python bot.py
```

Bot Workflow

When starting the bot:

1. Proxy Selection: Choose to run with or without proxies
2. Account Processing: Each account will be processed sequentially
3. Automated Tasks:
   · Account authentication
   · Training submission (models & datasets)
   · Task completion
   · Referral application
4. Cycle: Automatically repeats every 12 hours

🔧 Troubleshooting

Common Issues

1. "Invalid Private Key" error:
   · Ensure private keys start with 0x
   · Verify key format is correct
2. Proxy connection failures:
   · Test proxies individually
   · Ensure proxy format is correct
   · Check authentication credentials
3. Import errors:
   · Verify all requirements are installed
   · Check Python version (3.9+ required)

File Structure

```
Humanoid-BOT/
├── bot.py              # Main bot script
├── accounts.txt        # Wallet private keys
├── proxy.txt          # Proxy list (optional)
└── requirements.txt   # Python dependencies
```

📝 Notes

· The bot runs on a 12-hour cycle automatically
· Each session includes:
  · Account login
  · Training submissions (up to daily limits)
  · Task completion
  · Points tracking
· Use proxies to avoid rate limiting and improve success rates
· Always test with one account first before adding multiple

⚠️ Disclaimer

This tool is for educational purposes only. Use at your own risk. The developers are not responsible for any account restrictions or losses incurred while using this bot.


