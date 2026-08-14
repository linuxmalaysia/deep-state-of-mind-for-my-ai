---
okf_version: 0.1
type: documentation
title: "Reference: dsom_token_auditor.py"
timestamp: "2026-08-13T12:00:00Z"
topics: ["dsom", "reference", "tokens", "audit"]
---
# dsom_token_auditor.py reference

Tiktoken-based token efficiency and context load calculation script.

## Description

The `dsom_token_auditor.py` script compares non-DSOM "Bloated" context loads against optimised DSOM configurations (which utilise episodic resumes and progressive disclosures). It calculates savings percentages.

## Script path

`tools/dsom_token_auditor.py`

## CLI signature

```bash
uv run --with tiktoken python tools/dsom_token_auditor.py
```

## Outputs

Prints an analysis report:
- Token counts for bloated scenario structures.
- Token counts for progressive disclosure scenario structures.
- Percentage and absolute token savings achieved per execution turn.

## Dependencies

- **tiktoken:** Fast BPE tokenization library.

## Internal Python API

### `count_tokens(text, model="gpt-4")`

Counts tokens for a given string using optimised tokenisation with the specified model's encoder.
- **Arguments:** `text` (raw string), `model` (defaults to `"gpt-4"`).
- **Returns:** Integer representation of token count.

### `generate_bloated_context()`

Generates a raw string simulating chat history and massive file loads.

### `generate_dsom_context()`

Generates a raw string simulating episodic records and relative link references.
