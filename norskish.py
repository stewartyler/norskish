from openai import OpenAI
import pyperclip
from pynput import keyboard
import threading
import subprocess
import json
import keyring
import os
import certifi

os.environ["SSL_CERT_FILE"] = certifi.where()

# Retrieve from macOS Keychain
key = keyring.get_password("openai", "api_key")
client = OpenAI(api_key=key)

def mac_notify(title, message):
    print()
    subprocess.run([
        "terminal-notifier",
        "-title", title,
        "-message", message
    ])

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

    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        # Fallback in case GPT messes up the format
        result = {
            "corrected_text": content,
            "explanation": "Ingen forklaring tilgjengelig. Svaret var ikke i riktig JSON-format."
        }

    return result

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

def for_canonical(f):
    return lambda k: f(l.canonical(k))

hotkey = keyboard.HotKey(
    keyboard.HotKey.parse('<ctrl>+<shift>+c'),
    lambda: threading.Thread(target=handle_clipboard).start()
)

print("🇳🇴 Norskish kjører! Trykk Ctrl+Shift+C for å korrigere det som er kopiert.")

with keyboard.Listener(
    on_press=for_canonical(hotkey.press),
    on_release=for_canonical(hotkey.release)
) as l:
    l.join()