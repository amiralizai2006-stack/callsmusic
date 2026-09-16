from os import getenv

from dotenv import load_dotenv

load_dotenv()
SESSION_NAME = getenv('SESSION_NAME', 'session')
BOT_TOKEN = getenv('BOT_TOKEN')
API_ID = int(getenv('API_ID', '0') or 0)
API_HASH = getenv('API_HASH')
DURATION_LIMIT = int(getenv('DURATION_LIMIT', '7'))
COMMAND_PREFIXES = list(getenv('COMMAND_PREFIXES', '/ !').split())
SUDO_USERS = list(map(int, filter(None, getenv('SUDO_USERS', '').split())))

# Optional session string for userbot mode (if used)
STRING_SESSION = getenv('STRING_SESSION')

# Owner/support/config
OWNER_ID = int(getenv('OWNER_ID', '0') or 0)
SUPPORT_USERNAME = getenv('SUPPORT_USERNAME')
REQUIRED_CHANNEL = getenv('REQUIRED_CHANNEL')

# Subscriptions DB path
SUBSCRIPTIONS_DB = getenv('SUBSCRIPTIONS_DB', 'callsmusic_subscriptions.db')
