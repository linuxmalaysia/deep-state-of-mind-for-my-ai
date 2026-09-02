---
okf_version: 0.1
type: agent_skill
title: "🐍 Docstring & Function Reference Skill"
timestamp: "2026-09-02T12:00:00Z"
description: "Provides a structured approach for writing precise, maintainer-focussed Python docstrings and inline function documentation following standard Sphinx/reStructuredText and Google conventions."
topics: ["python", "docstring", "api-reference", "code-documentation", "dsom"]
name: docstring
---
# 🐍 Docstring & Function Reference Skill (`docstring`)

## Purpose

The `docstring` skill provides a structured approach to writing clear, accurate, and consistent docstrings for functions, classes, and modules. It ensures code documentation serves future maintainers and API consumers by explaining intent, contracts, side effects, failure modes, and edge cases rather than merely restating implementation line by line.

---

## Core Guidelines

1. **Focus on Intent and Contracts**:
   - Explain *what* a function accepts, *what* it returns, *what* exceptions it raises, and *when* it should or should not be used.
   - Do not restate implementation details that will become stale when code is refactored.
2. **LaTeX and Special Character Safety**:
   - Always use raw strings (`r"""..."""`) when docstrings include LaTeX mathematical notation, backslashes, or escape sequences.
3. **Structured Format**:
   - Follow Sphinx / reStructuredText or Google-style docstring conventions.
   - Standard sections include: Function summary, Parameters, Returns, Raises, Mathematical Formulas (if applicable), Notes, Warnings, and Examples.

---

## Docstring Structure Template

```python
def example_function(param_a: int, param_b: str = "default") -> bool:
    r"""Short one-line summary describing the function intent.

    A longer description providing additional context regarding side effects,
    threading guarantees, or underlying algorithms.

    Parameters
    ----------
    param_a : int
        Description of param_a and valid numerical ranges.
    param_b : str, optional
        Description of param_b, by default "default".

    Returns
    -------
    bool
        True if operation succeeds, False otherwise.

    Raises
    ------
    ValueError
        If param_a is negative.

    Notes
    -----
    Mathematical formula in LaTeX formatting:
    .. math:: f(x) = \sigma(W x + b)

    Examples
    --------
    >>> example_function(10, "test")
    True
    """
```

---

## Quality Rules

- **Provide Realistic Examples**: Executable doctest-style examples accelerate developer onboarding.
- **Document Edge Cases & Side Effects**: Explicitly state if a function mutates inputs in-place, performs network I/O, or requires specific environment variables.
- **Maintain UK English Standard**: Use UK English spelling in explanatory prose (e.g. `optimisation`, `initialise`).

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-09-02*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
