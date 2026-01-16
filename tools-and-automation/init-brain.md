# 🧠 Brain Initializer (init-brain.sh)

> **"A clean home for a clear mind."** - Initializing the Cognitive State.

## 1. 🏛️ Purpose
**Version:** v4.1 (Root Aware)
**Description:** Safely initializes the `.agent/brain` directory and default artifacts (`task.md`, `walkthrough.md`) to ensure cognitive continuity for AI agents.

## 2. 🛡️ Safety Mechanisms
| Mechanism | Status | Description |
| :--- | :--- | :--- |
| **Idempotency** | ✅ Enforced | Checks `if [ ! -d ]` before creating. Skips existing files. |
| **Exit-on-Error** | ✅ Active | `set -e` injected for safety. |
| **Root Check** | ✅ Active | Fails if not a git repository. |

## 3. ⚙️ Usage
```bash
./tools/init-brain.sh
```

## 4. 🧠 Logic Flow
1.  **Repo Check:** Confirms execution within a valid Git repository.
2.  **Directory Creation:** Creates `.agent/brain/` if missing.
3.  **Artifact Generation:** Populates `task.md`, `walkthrough.md`, `implementation_plan.md`, and `DSOM_TEMPLATE.md` with default boilerplate content *only if they don't exist*.

## 5. 📝 Extracted Comments
> "Safely initializes the Deep State of Mind (DSOM) directory and artifacts at the repository root to ensure cognitive continuity for AI agents."
