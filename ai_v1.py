#!/usr/bin/env python3

import sys
import subprocess
import shutil
import os
import socket
import urllib.request
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent


def run_cmd(cmd):
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout.strip()
        error = result.stderr.strip()

        if output:
            print(output)

        if error and result.returncode != 0:
            print(f"\nError: {error}")

        return result.returncode

    except subprocess.TimeoutExpired:
        print("Command timeout.")
        return 1


def system_info():
    print("\n=== SYSTEM INFO ===\n")

    print("Hostname :", socket.gethostname())

    print("\nUptime:")
    run_cmd("uptime")

    print("\nMemory:")
    run_cmd("free -h")

    print("\nStorage:")
    run_cmd("df -h /")

    print("\nCPU:")
    run_cmd("nproc")


def storage_info():
    print("\n=== STORAGE ===\n")
    run_cmd("df -h")


def largest_files():
    print("\n=== 20 FILE TERBESAR ===\n")

    download = Path.home() / "storage" / "downloads"

    if not download.exists():
        download = Path.home()

    run_cmd(
        f"find '{download}' -type f -printf '%s %p\\n' "
        f"2>/dev/null | sort -nr | head -20"
    )


def find_files(keyword):
    print(f"\n=== SEARCH: {keyword} ===\n")

    home = Path.home()

    run_cmd(
        f"find '{home}' -iname '*{keyword}*' "
        f"2>/dev/null | head -50"
    )


def check_website(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    print(f"\nChecking: {url}\n")

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "AI-Assistant/1.0"}
        )

        with urllib.request.urlopen(request, timeout=10) as response:
            print("STATUS :", response.status)
            print("URL    :", response.url)
            print("ONLINE : YES")

    except Exception as e:
        print("ONLINE : NO")
        print("ERROR  :", e)


def projects():
    print("\n=== PROJECTS ===\n")

    for item in Path.home().iterdir():
        if item.is_dir() and not item.name.startswith("."):
            print("📁", item.name)


def help_menu():
    print("""
AI ASSISTANT V1

Commands:

  ai
  ai help

  ai system
  ai storage
  ai largest files
  ai projects

  ai find <keyword>

  ai check <website>

Natural language examples:

  ai "cek storage"
  ai "cek ram"
  ai "lihat system"
  ai "file terbesar"
  ai "cari file python"
  ai "cek website google.com"
  ai "lihat project"

Examples:

  ai system
  ai find .zip
  ai check https://google.com
""")


def process(text):
    original = text.strip()
    q = original.lower()

    if not q or q in ("help", "-h", "--help"):
        help_menu()
        return

    # SYSTEM
    if any(x in q for x in [
        "system",
        "sistem",
        "ram",
        "memory",
        "cpu",
        "info hp",
        "info server"
    ]):
        system_info()
        return

    # STORAGE
    if any(x in q for x in [
        "storage",
        "disk",
        "penyimpanan",
        "ruang"
    ]):
        storage_info()
        return

    # LARGE FILES
    if any(x in q for x in [
        "file terbesar",
        "file besar",
        "largest file",
        "file paling besar"
    ]):
        largest_files()
        return

    # PROJECTS
    if any(x in q for x in [
        "project",
        "projects",
        "proyek"
    ]):
        projects()
        return

    # FIND
    if q.startswith("find "):
        find_files(original[5:])
        return

    if q.startswith("cari "):
        find_files(original[5:])
        return

    if q.startswith("search "):
        find_files(original[7:])
        return

    # WEBSITE
    if q.startswith("check "):
        check_website(original[6:].strip())
        return

    if q.startswith("cek "):
        target = original[4:].strip()

        if "." in target:
            check_website(target)
            return

    if "cek website" in q:
        target = q.split("cek website", 1)[1].strip()

        if target:
            check_website(target)
        else:
            print("Contoh: ai \"cek website google.com\"")

        return

    print("Saya belum mengerti perintah itu.")
    print("Ketik: ai help")


def main():
    if len(sys.argv) > 1:
        process(" ".join(sys.argv[1:]))
    else:
        print("AI Assistant V1")
        print("Ketik 'help' untuk bantuan.")
        print()

        while True:
            try:
                text = input("ai> ").strip()

                if text.lower() in ("exit", "quit", "q"):
                    break

                process(text)

            except KeyboardInterrupt:
                print("\nBye.")
                break


if __name__ == "__main__":
    main()
