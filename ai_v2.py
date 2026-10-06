#!/usr/bin/env python3

import sys
import subprocess
import urllib.request
import socket
import re
from pathlib import Path


HOME = Path.home()


# =========================
# CORE
# =========================

def run(cmd, timeout=30):
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        if result.stdout.strip():
            print(result.stdout.strip())

        if result.returncode != 0 and result.stderr.strip():
            print("ERROR:", result.stderr.strip())

        return result.returncode

    except subprocess.TimeoutExpired:
        print("⏱️ Command timeout.")
        return 1


# =========================
# SYSTEM
# =========================

def system():
    print("\n🖥️ SYSTEM STATUS\n")

    print("Hostname:", socket.gethostname())

    print("\nCPU:")
    run("nproc")

    print("\nRAM:")
    run("free -h")

    print("\nStorage:")
    run("df -h /")

    print("\nUptime:")
    run("uptime")


def processes():
    print("\n⚙️ TOP PROCESSES\n")

    run(
        "ps aux --sort=-%mem | "
        "head -11"
    )


# =========================
# STORAGE
# =========================

def storage():
    print("\n💾 STORAGE\n")
    run("df -h")


def largest_files():
    download = HOME / "storage" / "downloads"

    if not download.exists():
        download = HOME

    print(f"\n🔎 Scanning: {download}\n")

    run(
        f"find '{download}' -type f "
        f"-printf '%s %p\\n' 2>/dev/null | "
        f"sort -nr | head -20",
        timeout=60
    )


# =========================
# FILE SEARCH
# =========================

def search_file(keyword):
    print(f"\n🔎 Searching for: {keyword}\n")

    run(
        f"find '{HOME}' "
        f"-iname '*{keyword}*' "
        f"2>/dev/null | head -50",
        timeout=60
    )


# =========================
# PROJECTS
# =========================

def projects():
    print("\n📁 PROJECTS\n")

    for item in sorted(HOME.iterdir()):
        if item.is_dir() and not item.name.startswith("."):
            print("📁", item.name)


# =========================
# WEBSITE
# =========================

def website(url):

    if not re.match(r"^https?://", url):
        url = "https://" + url

    print(f"\n🌐 Checking {url}\n")

    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "AI-Assistant/2.0"
            }
        )

        with urllib.request.urlopen(
            req,
            timeout=10
        ) as response:

            print("Status :", response.status)
            print("URL    :", response.url)
            print("Online : YES")

    except Exception as e:
        print("Online : NO")
        print("Reason :", e)


# =========================
# SMART PARSER
# =========================

def parse(text):

    q = text.lower().strip()

    # ---------------------
    # EXIT
    # ---------------------

    if q in ["exit", "quit", "keluar"]:
        return "EXIT"


    # ---------------------
    # HELP
    # ---------------------

    if q in [
        "help",
        "bantuan",
        "apa yang bisa kamu lakukan"
    ]:
        return "HELP"


    # ---------------------
    # SYSTEM
    # ---------------------

    system_words = [
        "cek sistem",
        "lihat sistem",
        "system",
        "status sistem",
        "cek ram",
        "cek memory",
        "cek cpu",
        "cek kondisi hp",
        "info sistem"
    ]

    if any(x in q for x in system_words):
        return "SYSTEM"


    # ---------------------
    # PROCESSES
    # ---------------------

    process_words = [
        "proses berjalan",
        "proses yang jalan",
        "proses apa",
        "lihat proses",
        "cek proses",
        "ram paling banyak"
    ]

    if any(x in q for x in process_words):
        return "PROCESSES"


    # ---------------------
    # STORAGE
    # ---------------------

    storage_words = [
        "cek storage",
        "cek penyimpanan",
        "berapa storage",
        "berapa ruang",
        "ruang tersisa",
        "storage tersisa",
        "disk penuh",
        "penyimpanan penuh"
    ]

    if any(x in q for x in storage_words):
        return "STORAGE"


    # ---------------------
    # LARGE FILES
    # ---------------------

    large_words = [
        "file terbesar",
        "file paling besar",
        "file besar",
        "apa yang bikin storage penuh",
        "apa yang membuat storage penuh",
        "yang makan storage",
        "yang memakan storage",
        "yang paling banyak makan ruang"
    ]

    if any(x in q for x in large_words):
        return "LARGEST"


    # ---------------------
    # PROJECTS
    # ---------------------

    project_words = [
        "lihat project",
        "daftar project",
        "project saya",
        "proyek saya",
        "project apa saja"
    ]

    if any(x in q for x in project_words):
        return "PROJECTS"


    # ---------------------
    # WEBSITE
    # ---------------------

    if (
        "cek website" in q
        or "website ini hidup" in q
        or "website ini online" in q
        or "website ini down" in q
    ):

        match = re.search(
            r"(https?://[^\s]+|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
            text
        )

        if match:
            return ("WEBSITE", match.group(1))

        return "WEBSITE_MISSING"


    # ---------------------
    # FIND FILE
    # ---------------------

    prefixes = [
        "cari file ",
        "cari ",
        "search ",
        "temukan "
    ]

    for prefix in prefixes:

        if q.startswith(prefix):

            keyword = text[len(prefix):].strip()

            if keyword:
                return ("SEARCH", keyword)


    return "UNKNOWN"


# =========================
# HELP
# =========================

def help_menu():

    print("""
🤖 AI ASSISTANT V2

Contoh bahasa natural:

  ai cek sistem
  ai cek ram
  ai cek storage
  ai apa yang bikin storage penuh
  ai cari file zip
  ai lihat project saya
  ai cek website google.com
  ai lihat proses yang berjalan

Perintah langsung:

  ai system
  ai storage
  ai largest
  ai projects
  ai processes

Interactive mode:

  ai
""")


# =========================
# EXECUTOR
# =========================

def execute(action):

    if action == "EXIT":
        return False

    if action == "HELP":
        help_menu()

    elif action == "SYSTEM":
        system()

    elif action == "PROCESSES":
        processes()

    elif action == "STORAGE":
        storage()

    elif action == "LARGEST":
        largest_files()

    elif action == "PROJECTS":
        projects()

    elif action == "WEBSITE_MISSING":
        print("🌐 Masukkan website.")
        print("Contoh: ai cek website google.com")

    elif isinstance(action, tuple):

        command, value = action

        if command == "SEARCH":
            search_file(value)

        elif command == "WEBSITE":
            website(value)

    else:
        print("""
🤔 Saya belum memahami permintaan itu.

Coba:
  ai help
""")

    return True


# =========================
# MAIN
# =========================

def main():

    if len(sys.argv) > 1:

        text = " ".join(sys.argv[1:])

        action = parse(text)

        execute(action)

        return


    print("""
╔══════════════════════════════╗
║       AI ASSISTANT V2        ║
║      Smart Command Mode      ║
╚══════════════════════════════╝

Ketik 'help' untuk bantuan.
Ketik 'exit' untuk keluar.
""")

    while True:

        try:

            text = input("\nai> ").strip()

            action = parse(text)

            if not execute(action):
                break

        except KeyboardInterrupt:
            print("\n👋 Bye.")
            break


if __name__ == "__main__":
    main()
