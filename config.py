from pathlib import Path

APP_NAME = "AI Assistant"
VERSION = "3.0"

BASE_DIR = Path(__file__).resolve().parent
HOME_DIR = Path.home()

AUDIT_LOG = BASE_DIR / "audit.log"

# Safety
CONFIRM_DANGEROUS = True
DRY_RUN = True

# Search limits
MAX_RESULTS = 50
MAX_LARGEST_FILES = 20

# Command timeout
COMMAND_TIMEOUT = 30
