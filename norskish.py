import os
import certifi

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
os.environ["PATH"] = "/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin"

from openai import OpenAI
import pyperclip
from pynput import keyboard
import threading
import subprocess
import json
import keyring

# Retrieve from macOS Keychain
key = keyring.get_password("openai", "api_key")

# Fetch OpenAI client
client = OpenAI(api_key=key)

def mac_notify(title, message):
    subprocess.run([
        "osascript", "-e",
        f'display notification "{message}" with title "{title}"'
    ], check=True)


def correct_norwegian(text):
    prompt = f"""\
        Du er en norsklærer. Korriger teksten under og forklar kort hva som er rettet.
        Svar kun som et gyldig JSON-objekt på dette formatet:

        {{
        "corrected_text": "<den korrigerte teksten>",
        "explanation": "<kort forklaring på hva som ble rettet>"
        }}

        Tekst: {text}
        """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Du er en hjelpsom norsklærer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=500
    )

    content = response.choices[0].message.content

    if content.startswith("```"): # Check if the response is in code block format
        content = content.strip("`").strip("json").strip()

    try:
        result = json.loads(content)
        return result  # Contains both "corrected_text" and "explanation"
    except json.JSONDecodeError:
        # Fallback if model didn't follow JSON instructions at all...
        return {
            "corrected_text": content,
            "explanation": "Kunne ikke tolke svaret som JSON – returnerte råtekst."
        }

def handle_clipboard():
    text = pyperclip.paste()
    if text.strip():
        print("🔍 Korrigerer tekst...")
        result = correct_norwegian(text)
        corrected = result["corrected_text"]
        explanation = result["explanation"]
        pyperclip.copy(corrected)
        print(f"🇳🇴 Teksten er korrigert og kopiert til utklippstavlen. {explanation}")
        mac_notify("🇳🇴 Norsk tekst korrigert", f"{explanation}\n\nDen korrigerte teksten er kopiert til utklippstavlen.")
    else:
        mac_notify("🇳🇴 Ingen tekst!", "Utklippstavlen er tom.")

def on_hotkey_trigger():
    threading.Thread(target=handle_clipboard).start()

hotkey = keyboard.HotKey(
    keyboard.HotKey.parse('<ctrl>+<shift>+c'),
    on_hotkey_trigger
)

def for_canonical(listener, f):
    return lambda k: f(listener.canonical(k))

print("🇳🇴 Norskish kjører! Trykk Ctrl+Shift+C for å korrigere det som er kopiert.")

with keyboard.Listener(
    on_press=None,
    on_release=None
) as l:
    l.on_press = for_canonical(l, hotkey.press)
    l.on_release = for_canonical(l, hotkey.release)
    l.join()