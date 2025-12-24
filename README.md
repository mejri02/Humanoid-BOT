# 🚀 Humanoid BOT

> Automated airdrop farming solution for efficient time and multi-account management

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
- [Contributing](#contributing)

## 🎯 Overview

Humanoid BOT is an automated tool designed to streamline onchain operations across multiple accounts. It provides seamless integration with Humanoid network and offers robust proxy support for enhanced security and reliability.

**🔗 Get Started:** [Register on Humanoid](https://prelaunch.humanoidnetwork.org/ref/E2YE9U)

> **Important:** Connect new evm wallet.

## ✨ Features

- 🔄 **Automated Account Management** - Retrieve account information automatically
- 🌐 **Flexible Proxy Support** - Run with or without proxy configuration
- 🔀 **Smart Proxy Rotation** - Automatic rotation of invalid proxies
- 💰 **Training Submission** – Automated submit training models and datasets
- 📥 **Tasks Completion** – Automated complete available tasks
- 👥 **Multi-Account Support** - Manage multiple accounts simultaneously

## 📋 Requirements

- **Python:** Version 3.9 or higher
- **Required Libraries:** See `requirements.txt` below

## 🛠 Installation

### 1. Prepare Your Project Folder

Create a folder for the bot and navigate to it:

```bash
mkdir Humanoid-BOT
cd Humanoid-BOT


2. Create Requirements File

Create requirements.txt with the following content:

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

Create accounts.txt in the project directory:

```
your_private_key_1
your_private_key_2
your_private_key_3
```

Proxy Configuration (Optional)

Create proxy.txt in the project directory:

```
# Simple format
ip:port

# With protocol specification
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

Runtime Options

When starting the bot, you'll be prompted to choose:

1. Proxy Mode Selection:
   · Option 1: Run with proxy
   · Option 2: Run without proxy
2. Auto-Rotation:
   · y: Enable automatic invalid proxy rotation
   · n: Disable auto-rotation

Bot Features

· Automatic Login: Signs messages with wallet private keys
· Training Submission: Scrapes models/datasets from HuggingFace
· Task Completion: Automatically completes all available tasks
· Points Tracking: Shows current points for each account
· Auto Cycle: Runs every 12 hours automatically

🌐 Proxy Recommendation

For best results, use residential or mobile proxies. The bot supports:

· HTTP/HTTPS proxies
· SOCKS4/SOCKS5 proxies
· Authenticated proxies
· Automatic proxy rotation

💬 Support

For questions or issues:

1. Check the configuration files are properly formatted
2. Ensure all dependencies are installed
3. Verify your private keys are correct
4. Test proxies individually before adding to the list

🤝 Contributing

1. ⭐ Star the project if you find it useful
2. 🐛 Report issues you encounter
3. 💡 Suggest improvements or new features

---

Note: This bot is for educational purposes. Use at your own risk and always comply with the terms of service of the platforms you interact with.


