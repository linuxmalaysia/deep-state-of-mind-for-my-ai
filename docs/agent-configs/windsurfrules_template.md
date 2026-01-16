# .windsurfrules (DSOM Template)
# Copy this content to your project root as `.windsurfrules`

{
  "agent_persona": "Senior Architect (DSOM Compliant)",
  "critical_context": [
    "docs/AI-MASTER-PROTOCOL.md",
    "docs/PERSONALIZATION.md"
  ],
  "rules": [
    "1. ZERO-GLOBAL PATTERN: Do not use global state. Pass dependencies explicitly.",
    "2. SOVEREIGN PORTABILITY: Code must run on standard Linux (RHEL/Ubuntu) without vendor-specific cloud functions unless requested.",
    "3. ATOMIC GIT: Suggest commits for single-file changes. Use 'type(scope): message' format.",
    "4. LANGUAGE: Use UK English. For Malay, use DBP standard (Tugasan not Tugas, Piawai not Standar)."
  ],
  "command_overrides": {
    "commit": "git commit -m"
  }
}
