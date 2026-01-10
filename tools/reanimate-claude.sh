#!/bin/bash
# ==============================================================================
# 📜 DSOM Claude Reanimation Generator (v1.0)
#
# Date:    2026-01-11
# Author:  Harisfazillah Jamel (LinuxMalaysia)
# Partner: Generated with the help of Google Gemini
# License: GNU GPL v3.0 or later
# ==============================================================================

OUTPUT="DSOM-CLAUDE-INIT.md"

echo "📝 Generating DSOM Context for Claude.ai..."

{
    echo "# 🧠 DSOM CLAUDE INITIALIZATION"
    echo "Generated: $(date)"
    echo "---"
    echo "## ⚖️ MASTER PROTOCOL"
    cat docs/AI-MASTER-PROTOCOL.md 2>/dev/null || echo "Follow Zero-Global and Atomic Git laws."
    echo ""
    echo "## 🎯 CURRENT TASK"
    cat .agent/brain/task.md
    echo ""
    echo "## 🏁 MENTAL ANCHOR (WALKTHROUGH)"
    cat .agent/brain/walkthrough.md
    echo ""
    echo "## 🗺️ IMPLEMENTATION PLAN"
    cat .agent/brain/implementation_plan.md
} > "$OUTPUT"

echo "✅ File '$OUTPUT' created. Upload this to your Claude Project Knowledge Base."

