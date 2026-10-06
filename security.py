from datetime import datetime
from config import AUDIT_LOG, CONFIRM_DANGEROUS


def audit(action, status, detail=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    line = (
        f"[{timestamp}] "
        f"ACTION={action} "
        f"STATUS={status} "
        f"DETAIL={detail}\n"
    )

    try:
        with open(AUDIT_LOG, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception as e:
        print(f"⚠️ Audit error: {e}")


def confirm(action, target="", risk="HIGH"):

    print()
    print("╔════════════════════════════════════╗")
    print("║       ⚠️  CONFIRMATION REQUIRED    ║")
    print("╠════════════════════════════════════╣")
    print(f"║ Action : {action}")
    print(f"║ Target : {target}")
    print(f"║ Risk   : {risk}")
    print("╚════════════════════════════════════╝")

    try:
        answer = input("Continue? [y/N]: ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        answer = ""

    if answer == "y":
        audit(action, "APPROVED", target)
        return True

    audit(action, "DENIED", target)
    print("❌ Action cancelled.")
    return False


def security_check(action, target="", risk="LOW"):

    if risk == "LOW":
        return True

    if not CONFIRM_DANGEROUS:
        audit(
            action,
            "BLOCKED",
            "Dangerous action disabled"
        )

        print("🛑 Dangerous actions are disabled.")
        return False

    return confirm(
        action,
        target,
        risk
    )
