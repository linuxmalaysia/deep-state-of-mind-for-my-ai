---
okf_version: 0.1
type: agent_skill
title: "🔌 OpenAPI Spec Generation Skill"
timestamp: "2026-09-02T12:00:00Z"
description: "Generates, validates, and maintains OpenAPI 3.1+ specifications from code paths or design-first drafts to ensure API contract compliance."
topics: ["openapi", "api", "rest", "swagger", "dsom"]
name: openapi-spec-generation
---
# 🔌 OpenAPI Spec Generation Skill (`openapi-spec-generation`)

## Purpose
The `openapi-spec-generation` skill provides a comprehensive solution for generating, validating, and maintaining OpenAPI 3.1+ (and latest) specifications across code-first and design-first workflows. It ensures strict API contract compliance, simplifies developer onboarding, and facilitates client SDK and documentation generation.

---

## Key Capabilities

1. **Code-First Extraction**:
   - Inspect route handlers, request models, response schemas, and authentication middleware in source code.
   - Generate schema definitions without hallucinating fields or parameters.
2. **Design-First API Drafting**:
   - Author compliant OpenAPI 3.1+ YAML/JSON specifications prior to backend implementation.
3. **Contract Verification & Examples**:
   - Include realistic request payloads, success responses, error schemas, and pagination headers.
   - Ensure authentication schemes (OAuth2, Bearer Tokens, API Keys) are explicitly specified.

---

## When to Use This Skill

- Documenting new RESTful API endpoints or updating existing route specifications.
- Generating client SDKs or interactive Swagger/ReDoc reference pages.
- Auditing backend route handlers against contract specifications during CI/CD checks.

---

## Workflow Instructions

### Step 1: Source Inspection
Examine backend controllers, route definitions, and validation schemas (e.g., FastAPI, Pydantic, Express, Flask, or Go handlers).

### Step 2: Specification Assembly
Format the output as valid OpenAPI 3.1+ YAML:
- `openapi`: "3.1.0"
- `info`: Title, version, description.
- `paths`: Endpoints with operation IDs, parameters, request bodies, and status codes.
- `components/schemas`: Reusable data models.

### Step 3: Validation
Validate the specification using OpenAPI linters (e.g. `redocly` or `vacuum`):
```bash
npx @redocly/cli@1.25.0 lint openapi.yaml
```
Integrity verification: `@redocly/cli@1.25.0` (SHA512 checksum verified via package-lock.json).

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-09-02*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
