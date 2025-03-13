# How to Run

---

**1. Create a Telegram Bot Using BotFather**
- Open the Telegram app  
- Search for `BotFather` and select the official `@BotFather` account  
- Type `/start` and press Enter  
- Type `/newbot` and press Enter  
- Enter a name for your bot (e.g., `AlertBot`)  
- Choose a unique username for your bot (must end with `_bot`, e.g., `my_test_bot`)  
- After creation, **BotFather will provide an API token** → Save this token securely

**2. Install Required Libraries**  
```bash
pip install python-telegram-bot
```
**3. Run and Test the Bot**
- edit `setting.yml`
    - `ARKHAM_API_KEY` : API key of ARKHAM
    - `TELEGRAM_BOT_TOKEN` : API key which `@BotFather` gave you 
- download [hacker-addres.json](https://hackscan.hackbounty.io/public/hack-address.json)
- run it in the terminal
   ```bash
   python bot-telegram.py
   ```
- Search for `@my_test_bot` on Telegram  
