import subprocess
import socket
import urllib.request
import re
import shlex

from pathlib import Path

from config import (
    HOME_DIR,
    MAX_RESULTS,
    MAX_LARGEST_FILES,
    COMMAND_TIMEOUT,
)

from project_manager import (
    project_info,
    project_status,
    start_project,
    stop_project,
    project_log,
)


def run(command, timeout=COMMAND_TIMEOUT):

    try:

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        output = result.stdout.strip()

        if output:
            print(output)

        if result.returncode != 0:

            error = result.stderr.strip()

            if error:
                print("ERROR:", error)

        return result.returncode

    except subprocess.TimeoutExpired:

        print("⏱️ Command timeout.")
        return 1

    except Exception as e:

        print("ERROR:", e)
        return 1


def system_info():

    print()
    print("🖥️ SYSTEM INFORMATION")
    print()

    print("Hostname:")
    print(socket.gethostname())

    print()
    print("CPU:")
    run("nproc")

    print()
    print("Memory:")
    run("free -h")

    print()
    print("Storage:")
    run("df -h /")

    print()
    print("Uptime:")
    run("uptime")


def processes():

    print()
    print("⚙️ TOP PROCESSES")
    print()

    run(
        "ps aux --sort=-%mem | head -11"
    )


def storage():

    print()
    print("💾 STORAGE")
    print()

    run("df -h")


def largest_files():

    download = (
        HOME_DIR
        / "storage"
        / "downloads"
    )

    if not download.exists():
        download = HOME_DIR

    print()
    print("🔎 Scanning:")
    print(download)
    print()

    run(
        f"find {shlex.quote(str(download))} "
        f"-type f "
        f"-printf '%s %p\\n' "
        f"2>/dev/null | "
        f"sort -nr | "
        f"head -{MAX_LARGEST_FILES}",
        timeout=60
    )


def search_file(keyword):

    print()
    print(f"🔎 Searching: {keyword}")
    print()

    safe_keyword = re.sub(
        r"[^a-zA-Z0-9._+@%-]",
        "",
        keyword
    )

    if not safe_keyword:

        print("Invalid search keyword.")
        return

    run(
        f"find {shlex.quote(str(HOME_DIR))} "
        f"-iname '*{safe_keyword}*' "
        f"2>/dev/null | "
        f"head -{MAX_RESULTS}",
        timeout=60
    )


def projects():

    project_info()


def check_website(url):

    if not re.match(
        r"^https?://",
        url,
        re.IGNORECASE
    ):
        url = "https://" + url

    print()
    print("🌐 Checking:")
    print(url)
    print()

    try:

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent":
                "AI-Assistant/6.0"
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=10
        ) as response:

            print(
                "Status :",
                response.status
            )

            print(
                "URL    :",
                response.url
            )

            print(
                "Online : YES"
            )

    except Exception as e:

        print("Online : NO")
        print("Reason :", e)


TOOLS = {

    "system": {
        "name":
            "System Monitor",
        "description":
            "CPU, RAM, disk and uptime",
        "risk":
            "LOW",
        "function":
            system_info,
    },

    "processes": {
        "name":
            "Process Monitor",
        "description":
            "Show running processes",
        "risk":
            "LOW",
        "function":
            processes,
    },

    "storage": {
        "name":
            "Storage Monitor",
        "description":
            "Show storage usage",
        "risk":
            "LOW",
        "function":
            storage,
    },

    "largest": {
        "name":
            "Large File Scanner",
        "description":
            "Find largest files",
        "risk":
            "LOW",
        "function":
            largest_files,
    },

    "projects": {
        "name":
            "Project Explorer",
        "description":
            "List detected projects",
        "risk":
            "LOW",
        "function":
            projects,
    },

    "search": {
        "name":
            "File Search",
        "description":
            "Search files",
        "risk":
            "LOW",
        "function":
            search_file,
    },

    "website": {
        "name":
            "Website Checker",
        "description":
            "Check website availability",
        "risk":
            "LOW",
        "function":
            check_website,
    },

    "project_status": {
        "name":
            "Project Status",
        "description":
            "Check project processes",
        "risk":
            "LOW",
        "function":
            project_status,
    },

    "project_start": {
        "name":
            "Project Starter",
        "description":
            "Start detected project",
        "risk":
            "HIGH",
        "function":
            start_project,
    },

    "project_stop": {
        "name":
            "Project Stopper",
        "description":
            "Stop project process",
        "risk":
            "HIGH",
        "function":
            stop_project,
    },

    "project_log": {
        "name":
            "Project Log",
        "description":
            "Show recent project logs",
        "risk":
            "LOW",
        "function":
            project_log,
    },
}


def list_tools():

    print()
    print("🧰 AVAILABLE TOOLS")
    print()

    for key, tool in TOOLS.items():

        print(
            f"• {key:<18} "
            f"{tool['name']:<24} "
            f"Risk={tool['risk']}"
        )

    print()
