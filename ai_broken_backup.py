#!/usr/bin/env python3
from llm import ask, enabled
import sys

from tools import (
    TOOLS,
    list_tools,
)

from security import audit

from config import (
    APP_NAME,
    VERSION,
)


# ==========================================
# SMART PARSER
# ==========================================

def parse(text):

    q = text.lower().strip()

    # EXIT
    if q in [
        "exit",
        "quit",
        "keluar",
        "q"
    ]:
        return ("exit", None)


    # HELP
    if q in [
        "help",
        "bantuan",
        "menu"
    ]:
        return ("help", None)


    # TOOLS
    if q in [
        "tools",
        "tool",
        "daftar tools",
        "kemampuan"
    ]:
        return ("tools", None)


    # SYSTEM
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

    if any(x in q for x in system_words):
        return ("system", None)


    # PROCESSES
    process_words = [
        "lihat proses",
        "cek proses",
        "proses berjalan",
        "proses yang berjalan",
        "proses apa",
        "ram paling banyak",
    ]

    if any(x in q for x in process_words):
        return ("processes", None)


    # STORAGE
    storage_words = [
        "cek storage",
        "cek penyimpanan",
        "berapa storage",
        "storage tersisa",
        "ruang tersisa",
        "disk penuh",
        "penyimpanan penuh",
    ]

    if any(x in q for x in storage_words):
        return ("storage", None)


    # LARGE FILES
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

    if any(x in q for x in largest_words):
        return ("largest", None)


    # PROJECTS
    project_words = [
        "lihat project",
        "daftar project",
        "project saya",
        "proyek saya",
        "project apa saja",
    ]

    if any(x in q for x in project_words):
        return ("projects", None)


    # WEBSITE
    if (
        "cek website" in q
        or "cek situs" in q
        or "website ini online" in q
        or "website ini down" in q
    ):

        import re

        match = re.search(
            r"(https?://[^\s]+|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
            text
        )

        if match:
            return (
                "website",
                match.group(1)
            )

        return (
            "website_missing",
            None
        )


    # SEARCH
    prefixes = [
        "cari file ",
        "cari ",
        "search ",
        "temukan ",
        "find ",
    ]

    for prefix in prefixes:

        if q.startswith(prefix):

            keyword = text[
                len(prefix):
            ].strip()

            if keyword:
                return (
                    "search",
                    keyword
                )


    return ("unknown", None)


# ==========================================
# HELP
# ==========================================

def help_menu():

    print("""
╔══════════════════════════════════════╗
║        AI ASSISTANT V3               ║
║   Smart + Tools + Security           ║
╚══════════════════════════════════════╝

SYSTEM
  ai cek sistem
  ai cek ram
9  ai cek cpu
  ai lihat proses

STORAGE
  ai cek storage
  ai file terbesar
  ai apa yang bikin storage penuh

FILES
  ai cari file zip
  ai cari python

PROJECTS
  ai lihat project saya

WEB
  ai cek website google.com

TOOLS
  ai tools

INTERACTIVE
  ai

EXIT
  ai exit
""")


# ==========================================
# EXECUTOR
# ==========================================

def execute(action, value=None):

    if action == "exit":

        print("👋 Bye.")
        return False


    if action == "help":

        help_menu()
        return True


    if action == "tools":

        list_tools()
        return True


    if action == "website_missing":

        print(
            "🌐 Contoh: "
            "ai cek website google.com"
        )

        return True


    if action == "unknown":

        print(
            "\n🤔 Saya belum memahami "
            "permintaan itu."
        )

        print(
            "Ketik 'ai help' "
            "atau 'ai tools'."
        )

        return True


    # TOOL
    if action in TOOLS:

        tool = TOOLS[action]

        print()
        print(
            f"🔧 Tool: {tool['name']}"
        )

        print(
            f"Risk: {tool['risk']}"
        )

        audit(
            action,
            "START",
            str(value or "")
        )

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

        return True


    print("Unknown action.")

    return True


# ==========================================
# MAIN
# ==========================================

def main():

    if len(sys.argv) > 1:

        text = " ".join(
            sys.argv[1:]
        )
action, value = parse(text)

if action == "unknown" and enabled():
    result = ask(text)

    if result and result.get("tool") != "none":
        action = result.get("tool")
        value = result.get("argument") or None

execute(
    action,
    value
)

        return


    print()
    print(
        f"🤖 {APP_NAME} V{VERSION}"
    )

    print(
        "Type 'help' for commands."
    )

    print(
        "Type 'exit' to quit."
    )

    while True:

        try:

            text = input("\nai> ").strip()

            action, value = parse(text)

if action == "unknown" and enabled():

    result = ask(text)

    if result and result.get("tool") != "none":
        action = result.get("tool")
        value = result.get("argument") or None

if not execute(action, value):
    break

        except KeyboardInterrupt:

            print(
                "\n👋 Bye."
            )

            break


if __name__ == "__main__":
    main()
