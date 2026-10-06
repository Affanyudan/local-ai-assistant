cd ~/ai-assistant

cat > README.md <<'EOF'
# 🤖 AI Assistant V6

> Lightweight, secure, extensible AI-powered CLI assistant for Linux, Termux, and Proot Ubuntu.

**AI Assistant V6** adalah command-line assistant yang dirancang untuk membantu mengelola sistem Linux, menjalankan command yang aman, memonitor project, serta mengelola aplikasi/project secara langsung dari terminal.

Project ini mengutamakan **simplicity, security, modularity, dan extensibility** sehingga dapat dikembangkan dari local rule-based assistant menjadi AI-powered automation platform.

---

## ✨ Highlights

- 🖥️ System information
- ⚙️ Process monitoring
- 💾 Storage monitoring
- 📁 Large file detection
- 🔎 File search
- 🌐 Website availability check
- 🧰 Safe terminal command execution
- 📦 Project discovery
- 📊 Project status monitoring
- ▶️ Start project
- ⛔ Stop project
- 📜 Project runtime logs
- 🧠 Optional LLM integration
- 🔐 Security confirmation for dangerous actions
- 📝 Audit logging
- 🧩 Modular tool architecture
- 📱 Termux + Proot Ubuntu friendly
- 🚀 Designed for future V7/V8 automation

---

# 📌 Version

**Current Version: V6**

V6 introduces the **Project Manager**, allowing AI Assistant to discover, monitor, start, stop, and inspect local projects.

---

# 🧠 Architecture

AI Assistant uses a modular architecture:

```text
                    ┌─────────────────────┐
                    │      User CLI       │
                    │        ai           │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       ai.py         │
                    │ Command Parser      │
                    │ LLM Fallback        │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
        ┌────────────┐ ┌────────────┐ ┌────────────┐
        │   tools.py │ │ security.py│ │   llm.py   │
        │ Tool Layer │ │  Security  │ │ LLM Layer  │
        └──────┬─────┘ └────────────┘ └────────────┘
               │
               ▼
        ┌────────────────────┐
        │ project_manager.py │
        │ Project Management │
        └────────────────────┘
               │
               ▼
        ┌────────────────────┐
        │ Local Linux System │
        └────────────────────┘
