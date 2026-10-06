from datetime import datetime
from config import AUDIT_LOG


def audit(action, status, detail=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    line = (
        f"[{timestamp}] "
        f"ACTION={action} "
        f"STATUS={status} "
        f"DETAIL={detail}\n"
    )

    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(line)


def confirm(action, target="", risk="LOW"):
    print()
    print("╔════════════════════════════════════╗")
    print("║       ⚠️  CONFIRMATION REQUIRED    ║")
    print("╠════════════════════════════════════╣")
    print(f"║ Action : {action}")
    print(f"║ Target : {target}")
    print(f"║ Risk   : {risk}")
    print("╚════════════════════════════════════╝")

    answer = input("Continue? [y/N]: ").strip().lower()

    if answer == "y":
        audit(action, "APPROVED", target)
        return True

    audit(action, "DENIED", target)
    print("❌ Action cancelled.")

    return False
