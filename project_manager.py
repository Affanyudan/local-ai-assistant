import os
import signal
import subprocess
import time

from pathlib import Path


HOME = Path.home()
PID_DIR = HOME / ".ai-assistant-pids"

PID_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================
# PROJECT DISCOVERY
# ==========================================

def find_projects():

    projects = []

    skip = {
        ".cache",
        ".config",
        ".local",
        ".cargo",
        ".rustup",
        ".venv",
        "__pycache__",
        "storage",
    }

    try:

        for item in HOME.iterdir():

            if not item.is_dir():
                continue

            if item.name.startswith("."):
                continue

            if item.name in skip:
                continue

            # Python project
            if (
                (item / "main.py").exists()
                or
                (item / "app.py").exists()
                or
                (item / "bot.py").exists()
                or
                (item / "farmer.py").exists()
                or
                (item / "requirements.txt").exists()
                or
                (item / "pyproject.toml").exists()
            ):
                projects.append(item)

            # Node project
            elif (
                (item / "package.json").exists()
            ):
                projects.append(item)

            # Rust project
            elif (
                (item / "Cargo.toml").exists()
            ):
                projects.append(item)

    except Exception as e:

        print(
            "ERROR:",
            e
        )

    return sorted(
        projects,
        key=lambda p: p.name.lower()
    )


# ==========================================
# PROJECT INFO
# ==========================================

def project_info(name=None):

    projects = find_projects()

    if not projects:

        print()
        print(
            "📁 No projects detected."
        )
        return

    print()
    print("📁 DETECTED PROJECTS")
    print()

    for project in projects:

        marker = ""

        if name:
            if project.name.lower() == name.lower():
                marker = " ← selected"

        print(
            f"• {project.name}{marker}"
        )

        if (project / "main.py").exists():
            print("    Python: main.py")

        elif (project / "app.py").exists():
            print("    Python: app.py")

        elif (project / "bot.py").exists():
            print("    Python: bot.py")

        elif (project / "farmer.py").exists():
            print("    Python: farmer.py")

        elif (project / "package.json").exists():
            print("    Node.js project")

        elif (project / "Cargo.toml").exists():
            print("    Rust project")


# ==========================================
# FIND PROJECT
# ==========================================

def get_project(name):

    projects = find_projects()

    if not name:
        return None

    name = name.strip().lower()

    # Exact match
    for project in projects:

        if project.name.lower() == name:
            return project

    # Partial match
    matches = [
        p for p in projects
        if name in p.name.lower()
    ]

    if len(matches) == 1:
        return matches[0]

    return None


# ==========================================
# DETECT START COMMAND
# ==========================================

def detect_command(project):

    if (project / "main.py").exists():
        return [
            "python",
            "main.py"
        ]

    if (project / "app.py").exists():
        return [
            "python",
            "app.py"
        ]

    if (project / "bot.py").exists():
        return [
            "python",
            "bot.py"
        ]

    if (project / "farmer.py").exists():
        return [
            "python",
            "farmer.py"
        ]

    if (project / "package.json").exists():
        return [
            "npm",
            "start"
        ]

    if (project / "Cargo.toml").exists():
        return [
            "cargo",
            "run"
        ]

    return None


# ==========================================
# PID FILE
# ==========================================

def pid_file(project):

    safe_name = "".join(
        c if c.isalnum() or c in "-_"
        else "_"
        for c in project.name
    )

    return PID_DIR / f"{safe_name}.pid"


def read_pid(project):

    file = pid_file(project)

    if not file.exists():
        return None

    try:

        return int(
            file.read_text().strip()
        )

    except Exception:
        return None


def write_pid(project, pid):

    pid_file(project).write_text(
        str(pid)
    )


def remove_pid(project):

    file = pid_file(project)

    try:

        file.unlink()

    except FileNotFoundError:
        pass


# ==========================================
# PROCESS CHECK
# ==========================================

def process_exists(pid):

    if not pid:
        return False

    try:

        os.kill(
            pid,
            0
        )

        return True

    except ProcessLookupError:

        return False

    except PermissionError:

        return True

    except Exception:

        return False


# ==========================================
# PROJECT STATUS
# ==========================================

def project_status(name=None):

    projects = find_projects()

    if name:

        project = get_project(name)

        if not project:

            print()
            print(
                f"❌ Project tidak ditemukan: {name}"
            )
            return

        projects = [project]

    print()
    print("📊 PROJECT STATUS")
    print()

    for project in projects:

        pid = read_pid(project)

        if process_exists(pid):

            print(
                f"🟢 {project.name}"
                f"   RUNNING"
                f"   PID={pid}"
            )

        else:

            if pid:
                remove_pid(project)

            print(
                f"🔴 {project.name}"
                f"   STOPPED"
            )


# ==========================================
# START PROJECT
# ==========================================

def start_project(name):

    project = get_project(name)

    if not project:

        print()
        print(
            f"❌ Project tidak ditemukan: {name}"
        )
        return

    existing_pid = read_pid(project)

    if process_exists(existing_pid):

        print()
        print(
            f"🟢 {project.name} sudah berjalan."
        )

        print(
            f"PID: {existing_pid}"
        )

        return

    command = detect_command(project)

    if not command:

        print()
        print(
            "❌ Tidak menemukan "
            "entry point project."
        )
        return

    log_dir = project / ".ai-assistant"

    log_dir.mkdir(
        exist_ok=True
    )

    log_file = (
        log_dir
        / "runtime.log"
    )

    print()
    print(
        f"🚀 Starting: {project.name}"
    )

    print(
        "📂 Directory:",
        project
    )

    print(
        "▶️ Command:",
        " ".join(command)
    )

    print(
        "📝 Log:",
        log_file
    )

    try:

        log = open(
            log_file,
            "a",
            encoding="utf-8"
        )

        process = subprocess.Popen(
            command,
            cwd=project,
            stdout=log,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )

        write_pid(
            project,
            process.pid
        )

        time.sleep(1)

        if process_exists(
            process.pid
        ):

            print()
            print(
                "✅ Project started."
            )

            print(
                f"PID: {process.pid}"
            )

        else:

            remove_pid(project)

            print()
            print(
                "❌ Project berhenti "
                "setelah dijalankan."
            )

            print(
                f"Cek log: {log_file}"
            )

    except Exception as e:

        print()
        print(
            "❌ Start error:",
            e
        )


# ==========================================
# STOP PROJECT
# ==========================================

def stop_project(name):

    project = get_project(name)

    if not project:

        print()
        print(
            f"❌ Project tidak ditemukan: {name}"
        )
        return

    pid = read_pid(project)

    if not process_exists(pid):

        remove_pid(project)

        print()
        print(
            f"🔴 {project.name} "
            f"tidak sedang berjalan."
        )

        return

    print()
    print(
        f"🛑 Stopping: {project.name}"
    )

    print(
        f"PID: {pid}"
    )

    try:

        os.killpg(
            os.getpgid(pid),
            signal.SIGTERM
        )

        for _ in range(10):

            if not process_exists(pid):
                break

            time.sleep(0.5)

        if process_exists(pid):

            print(
                "⚠️ Process belum berhenti."
            )

            print(
                "Kirim SIGKILL..."
            )

            os.killpg(
                os.getpgid(pid),
                signal.SIGKILL
            )

        remove_pid(project)

        print(
            "✅ Project stopped."
        )

    except Exception as e:

        print(
            "❌ Stop error:",
            e
        )


# ==========================================
# LOG
# ==========================================

def project_log(name, lines=30):

    project = get_project(name)

    if not project:

        print(
            f"❌ Project tidak ditemukan: {name}"
        )
        return

    log_file = (
        project
        / ".ai-assistant"
        / "runtime.log"
    )

    print()
    print(
        f"📜 LOG: {project.name}"
    )
    print()

    if not log_file.exists():

        print(
            "Belum ada runtime log."
        )

        return

    try:

        content = (
            log_file
            .read_text(
                encoding="utf-8",
                errors="replace"
            )
            .splitlines()
        )

        for line in content[-lines:]:
            print(line)

    except Exception as e:

        print(
            "ERROR:",
            e
        )
