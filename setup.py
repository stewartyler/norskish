from setuptools import setup
import certifi

APP = ['norskish.py']
DATA_FILES = [( 'certifi', [certifi.where()] )]
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'norskish.icns',
    'resources': [certifi.where()],
    'plist': {
        'CFBundleName': 'Norskish',
        'CFBundleDisplayName': 'Norskish',
        'CFBundleIdentifier': 'com.yourname.norskish',
        'CFBundleVersion': '0.1',
        'LSUIElement': True,  # Hides dock icon and app switcher entry
    },
    'packages': ['openai', 'pyperclip', 'pynput', 'dotenv', 'keyring'],
}

setup(
    app=APP,
    name='Norskish',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)