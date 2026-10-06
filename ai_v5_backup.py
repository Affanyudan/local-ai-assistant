import sys
import re

from config import APP_NAME, VERSION
from tools import TOOLS, list_tools
from security import audit, security_check
from llm import ask, enabled


def show_help():

    print()
    print("🤖 AI ASSISTANT")
    print()
    print("Contoh:")
    print()
    print("  cek sistem")
    print("  cek storage")
    print("  lihat proses")
    print("  file terbesar")
    print("  lihat project")
    print("  cari file python")
    print("  cek website google.com")
    print("  terminal pwd")
    print("  terminal python --version")
    print()
    print("Perintah:")
    print("  help      - bantuan")
    print("  tools     - daftar tools")
    print("  exit      - keluar")
    print()


def parse(text):

    original = text.strip()
    text = original.lower()

    if not text:
        return "unknown", None

    if text in (
        "exit",
        "quit",
        "keluar",
        "q"
    ):
        return "exit", None

    if text in (
        "help",
        "bantuan",
        "menu"
    ):
        return "help", None

    if text in (
        "tools",
        "tool",
        "daftar tools",
        "kemampuan"
    ):
        return "tools", None

    system_words = [
        "cek sistem",
        "lihat sistem",
        "status sistem",
        "info sistem",
        "cek ram",
        "cek memory",
        "cek cpu",
        "cek kondisi hp",
        "kondisi sistem",
    ]

    if any(
        word in text
        for word in system_words
    ):
        return "system", None

    process_words = [
        "lihat proses",
        "cek proses",
        "proses berjalan",
        "proses yang berjalan",
        "proses apa",
        "ram paling banyak",
    ]

    if any(
        word in text
        for word in process_words
    ):
        return "processes", None

    storage_words = [
        "cek storage",
        "cek penyimpanan",
        "berapa storage",
        "storage tersisa",
        "ruang tersisa",
        "disk penuh",
        "penyimpanan penuh",
    ]

    if any(
        word in text
        for word in storage_words
    ):
        return "storage", None

    largest_words = [
        "file terbesar",
        "file paling besar",
        "file besar",
        "apa yang bikin storage penuh",
        "apa yang membuat storage penuh",
        "yang makan storage",
        "yang memakan storage",
        "yang paling banyak makan ruang",
    ]

    if any(
        word in text
        for word in largest_words
    ):
        return "largest", None

    project_words = [
        "lihat project",
        "daftar project",
        "project saya",
        "project apa saja",
        "lihat proyek",
        "daftar proyek",
        "proyek saya",
    ]

    if any(
        word in text
        for word in project_words
    ):
        return "projects", None

    website_words = [
        "cek website",
        "cek situs",
        "website ini online",
        "website ini down",
        "cek url",
    ]

    if any(
        word in text
        for word in website_words
    ):

        match = re.search(
            r"(https?://[^\s]+|"
            r"[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
            original
        )

        if match:
            return (
                "website",
                match.group(1)
            )

        return "website", None

    # TERMINAL
    terminal_patterns = [
        "terminal ",
        "jalankan ",
        "run ",
        "execute ",
        "command ",
        "perintah ",
    ]

    for prefix in terminal_patterns:

        if text.startswith(prefix):

            command = original[
                len(prefix):
            ].strip()

            if command:
                return (
                    "terminal",
                    command
                )

    # FILE SEARCH
    search_prefixes = [
        "cari file ",
        "cari ",
        "search ",
        "temukan ",
        "find ",
    ]

    for prefix in search_prefixes:

        if text.startswith(prefix):

            keyword = original[
                len(prefix):
            ].strip()

            if keyword:
                return (
                    "search",
                    keyword
                )

    return "unknown", None


def execute(action, value=None):

    if action == "exit":

        print()
        print("👋 Goodbye.")
        return False

    if action == "help":

        show_help()
        return True

    if action == "tools":

        list_tools()
        return True

    if action == "unknown":

        print()
        print(
            "🤔 Saya belum memahami "
            "permintaan itu."
        )

        if enabled():
            print(
                "💡 LLM mode tersedia."
            )

        print(
            "Ketik 'help' untuk "
            "melihat contoh."
        )

        return True

    if action not in TOOLS:

        print()
        print(
            f"❌ Tool tidak ditemukan: "
            f"{action}"
        )

        audit(
            action,
            "INVALID",
            str(value or "")
        )

        return True

    tool = TOOLS[action]

    print()
    print(
        f"🔧 Tool : {tool['name']}"
    )

    print(
        f"Risk   : {tool['risk']}"
    )

    if not security_check(
        action,
        str(value or ""),
        tool["risk"]
    ):
        return True

    audit(
        action,
        "START",
        str(value or "")
    )

    try:

        function = tool["function"]

        if value is not None:
            function(value)

        else:
            function()

        audit(
            action,
            "DONE",
            str(value or "")
        )

    except Exception as e:

        print()
        print("❌ Tool error:")
        print(e)

        audit(
            action,
            "ERROR",
            str(e)
        )

    return True


def llm_fallback(
    text,
    action,
    value
):

    if action != "unknown":
        return action, value

    if not enabled():
        return action, value

    print()
    print("🧠 Asking LLM...")

    result = ask(text)

    if not result:
        return action, value

    tool_name = result.get("tool")
    argument = result.get("argument")

    if tool_name in TOOLS:

        audit(
            "llm",
            "TOOL_SELECTED",
            f"{tool_name} | {argument}"
        )

        return (
            tool_name,
            argument or None
        )

    audit(
        "llm",
        "INVALID_TOOL",
        str(tool_name)
    )

    return action, value


def main():

    if len(sys.argv) > 1:

        text = " ".join(
            sys.argv[1:]
        )

        action, value = parse(text)

        action, value = llm_fallback(
            text,
            action,
            value
        )

        execute(
            action,
            value
        )

        return

    print()
    print(
        "╔══════════════════════════════════════╗"
    )

    print(
        f"║  🤖 {APP_NAME} V{VERSION:<24}║"
    )

    print(
        "╚══════════════════════════════════════╝"
    )

    print()
    print(
        "Type 'help' for commands."
    )

    print(
        "Type 'tools' to list tools."
    )

    print(
        "Type 'exit' to quit."
    )

    print()

    while True:

        try:

            text = input(
                "You > "
            ).strip()

        except KeyboardInterrupt:

            print()
            print("👋 Goodbye.")
            break

        except EOFError:

            print()
            print("👋 Goodbye.")
            break

        if not text:
            continue

        action, value = parse(text)

        action, value = llm_fallback(
            text,
            action,
            value
        )

        if not execute(
            action,
            value
        ):
            break


if __name__ == "__main__":
    main()
