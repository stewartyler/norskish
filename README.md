# 🇳🇴 Norskish

**Norskish** is a lightweight macOS app that helps you correct Norwegian grammar quickly from anywhere. Using a global hotkey (`Ctrl+Shift+C`) it will take whatever Norwegian text is in your clipboard and pass the corrected Norwegian text back to your clipboard. Built using Python, OpenAI's GPT-4o model, and macOS-native notifications.

### Features
- Clipboard-based correction with explanation
- macOS notifications
- Menu-less background app
- Keychain-secured OpenAI API key
- No Python installation required for users

### Setup
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Add your OpenAI API key:  
   `python -c "import keyring; keyring.set_password('openai', 'api_key', 'your-key')"`
4. Build the app: `python setup.py py2app`
5. Find it in `dist/Norskish.app`

### Launching on Startup
To have Norskish start automatically when you log in:
1. Open **System Settings**
2. Go to **General > Login Items**
3. Under **"Open at Login"**, click the **`+` button**
4. Select your installed `Norskish.app` from `/Applications` or `~/Applications`
✅ That’s it — the app will now launch silently in the background on startup.

### Credits
Built by Tyler Stewart. Inspired by the need to write better norsk på jobb 💼🇳🇴

### License
MIT — Free to use, fork, remix, and improve.