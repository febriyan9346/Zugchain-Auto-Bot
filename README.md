# Zugchain Auto Bot

![Zugchain](https://img.shields.io/badge/Zugchain-Testnet-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

Automated bot for Zugchain Testnet to manage staking, claiming rewards, and faucet interactions.

## 🌐 Official Links

- **Zugchain Testnet**: [https://testnet.zugchain.org/?ref=ZUG-AKATL53I](https://testnet.zugchain.org/?ref=ZUG-AKATL53I)
- **Explorer**: [https://explorer.zugchain.org](https://explorer.zugchain.org)
- **RPC**: https://rpc.zugchain.org

## ✨ Features

- 🔐 **Multi-Account Support**: Manage multiple wallets simultaneously
- 🔄 **Auto Staking**: Automatically stake ZUG tokens
- 💰 **Auto Claim**: Automatically claim staking rewards
- 🚰 **Faucet Integration**: Auto-claim from faucet with 2Captcha support
- 🌐 **Proxy Support**: Run with or without proxy
- 📊 **Profile Tracking**: Monitor points, claims, and rank
- ⏰ **Cycle Management**: Automated 24-hour cycle execution
- 🎨 **Colorful Logs**: Beautiful console output with timestamps

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Zugchain wallet private keys
- (Optional) 2Captcha API key for faucet claiming
- (Optional) Proxy list

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/febriyan9346/Zugchain-Auto-Bot.git
cd Zugchain-Auto-Bot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure your accounts**

Create `accounts.txt` and add your private keys (one per line):
```
0xyourprivatekey1
0xyourprivatekey2
0xyourprivatekey3
```

4. **(Optional) Configure proxy**

Create `proxy.txt` and add your proxies (one per line):
```
http://user:pass@ip:port
socks5://user:pass@ip:port
ip:port:user:pass
```

5. **(Optional) Configure 2Captcha**

Create `2captcha.txt` and add your API key:
```
your_2captcha_api_key_here
```

## 💻 Usage

Run the bot:
```bash
python bot.py
```

### Interactive Options

When you run the bot, you'll be prompted to configure:

1. **Proxy Mode**
   - `1`: Run with proxy
   - `2`: Run without proxy

2. **Auto Claim Faucet**
   - `y`: Enable faucet claiming (requires 2Captcha)
   - `n`: Disable faucet claiming

3. **Stake Amount**
   - Enter the amount of ZUG to stake
   - Leave empty to skip staking

4. **Auto Claim Stake**
   - `y`: Enable automatic claim of staking rewards
   - `n`: Disable automatic claiming

## 📁 File Structure

```
Zugchain-Auto-Bot/
├── bot.py              # Main bot script
├── accounts.txt        # Private keys (create this)
├── proxy.txt          # Proxy list (optional)
├── 2captcha.txt       # 2Captcha API key (optional)
├── requirements.txt   # Python dependencies
├── README.md         # This file
└── LICENSE           # MIT License
```

## 🔧 Configuration

### Smart Contract Addresses

- **Stake Contract**: `0x4ed9828ba8487b9160C820C8b72c573E74eBbD0A`
- **Chain ID**: `824642`

### API Endpoints

- Sync: `https://testnet.zugchain.org/api/user/sync`
- Faucet: `https://testnet.zugchain.org/api/faucet`
- Staking History: `https://testnet.zugchain.org/api/staking/history`
- Profile: `https://testnet.zugchain.org/api/incentive/profile`

## 🛡️ Security Notes

- **Never share your private keys** with anyone
- Keep your `accounts.txt` file secure and private
- Add `accounts.txt`, `proxy.txt`, and `2captcha.txt` to `.gitignore`
- Use environment variables for sensitive data in production

## 📊 Features Breakdown

### Staking
- Automatically stakes specified amount of ZUG tokens
- Sends transactions to the staking contract
- Monitors transaction status

### Claiming
- Retrieves staking history
- Claims rewards for all active stakes
- Syncs claims with the API

### Faucet
- Solves captcha using 2Captcha service
- Automatically claims testnet tokens
- Handles rate limiting

### Profile Tracking
- Displays current points
- Shows total claims
- Monitors leaderboard rank

## 🔄 Bot Cycle

The bot operates in 24-hour cycles:

1. Login to all accounts
2. Claim faucet (if enabled)
3. Stake tokens (if configured)
4. Claim rewards (if enabled)
5. Display profile statistics
6. Wait 24 hours before next cycle

## ⚠️ Troubleshooting

### Common Issues

**"accounts.txt missing"**
- Create the file and add your private keys

**"Login failed"**
- Check your internet connection
- Verify your private keys are correct
- Try using a proxy

**"Captcha solving failed"**
- Verify your 2Captcha API key
- Check 2Captcha balance
- Ensure captcha service is working

**RPC Connection Issues**
- Check if RPC URL is accessible
- Try using a proxy
- Wait and retry later

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This bot is for educational purposes only. Use at your own risk. The authors are not responsible for any losses or damages incurred through the use of this software.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

## Support Us with Cryptocurrency

You can make a contribution using any of the following blockchain networks:

| Network | Wallet Address |
|---------|---------------|
| **EVM** | `0x216e9b3a5428543c31e659eb8fea3b4bf770bdfd` |
| **TON** | `UQCEzXLDalfKKySAHuCtBZBARCYnMc0QsTYwN4qda3fE6tto` |
| **SOL** | `9XgbPg8fndBquiYXkGpNYKHHhymdmVhmF6nMkPxhXTki` |
| **SUI** | `0x8c3632ddd46c984571bf28f784f7c7aeca3b8371f146c4024f01add025f993bf` |

Your support helps us maintain and improve this project. Thank you! 🙏
