---
name: general-agent
description: \"A general-purpose autonomous agent wrapper around Codex CLI for non-coding tasks, system administration, and complex terminal workflows, now with multimodal vision capabilities.\"
version: 1.3.1
author: Yadan Fan
license: MIT
metadata:
  hermes:
    tags: [General-Agent, Autonomous-Executor, Codex, System-Admin, Automation, Multimodal]
    related_skills: [codex, super-router, subagent-driven-development]
---

# General Agent (via Codex)

The General Agent leverages the iterative loop and file-system capabilities of the Codex CLI to solve complex non-coding problems. While Codex is optimized for code, its ability to observe shell output and correct its actions makes it a powerful generalist for any task solvable via a terminal.

## Original Motivation

This skill was originally created to let Hermes users indirectly use GPT-5.5 before Hermes supported selecting GPT-5.5 directly. The intended path is Hermes -> Codex CLI -> GPT-5.5, with Codex handling the terminal execution loop.

## When to Use

Use this skill when a task requires an autonomous loop (Try -> Observe -> Correct) but is not strictly focused on software development.

**CRITICAL:** When the user explicitly requests the General Agent to execute a task through Codex CLI, you MUST NOT simulate the behavior via standard `delegate_task` subagents. You MUST invoke the actual Codex CLI via the Hermes `terminal` tool, or the host environment's equivalent shell-execution tool. 

- **System Administration:** Auditing logs, cleaning up disk space, managing Docker/K8s clusters.
- **Multimodal Research:** Analyzing images/documents (e.g., medical reports, screenshots) and synthesizing data into reports.
- **Research Automation:** Performing live web research using CLI-based browsers, synthesizing market reports.
- **Environment Setup:** Installing complex toolchains, bootstrapping dev environments.

## Prerequisites

- **Codex CLI installed:** `npm install -g @openai/codex`
- **Git Repository:** Codex MUST run inside a git repository.
- **Vision Proxy:** `scripts/vision_proxy.py` must be available to bridge Codex to the vision system using `google-gemini-cli/gemini-3-pro-preview`.
- **Super-Router (Recommended):** While not a hard dependency, having the `super-router` skill deployed is highly recommended for complex tasks to provide the high-level decomposition needed before General Agent execution.

## Core Workflows

### 1. Pre-Flight Validation (Mandatory)
Before executing any Codex command, verify tools:
`terminal(command=\"which codex || npm list -g @openai/codex\")`

Confirm execution context:
- `codex --version` and `codex exec --help`.
- `git rev-parse --show-toplevel` or `git init`.

### 2. Multimodal Perception (The Vision Bridge)
Codex is text-only. To analyze images, use the **Perceive -> Reason -> Act** pattern:
1. **Perceive:** Use the `vision_proxy.py` script to convert an image to text.
   `python3 scripts/vision_proxy.py <image_path>`
2. **Reason:** Instruct Codex to read the output of this script as the \"ground truth\" for the image content.
3. **Act:** Perform terminal-based operations based on the vision analysis.

### 3. Prompt Handling (Mandatory)
Write prompt text to a temporary file. Pass it to Codex via stdin:
`codex exec [verified-flags] - < prompt.txt`
**CRITICAL:** Use `<< prompt prompt.txt` for standard shell redirection.

### 4. The \"Scratchpad\" Execution (Standard)
For tasks without an existing project:
1. Create a scratch Git repo: `mktemp -d && git init`.
2. Write `prompt.txt` with detailed instructions, including the requirement to use `scripts/vision_proxy.py` for any encountered images.
3. Execute via `codex exec - < prompt.txt`.

### 5. The \"Super-Generalist\" Combo (Planning -> Execution)
Combine **Super-Router** (high-level decomposition) and **General Agent** (low-level execution).
1. **Plan:** `super-router \"Your complex goal\"`.
2. **Execute:** Run Codex for each subtask, pivoting to `vision_proxy.py` when visual evidence is required.

## Result Validation Requirements
Treat Codex output as a draft. Validation MUST rely on concrete evidence:
- **For Vision Tasks:** Cross-reference the textual output of `vision_proxy.py` with the final summary. Preserve exact values from the vision analysis.
- **For Filesystem Tasks:** Inspect diffs or generated files before reporting success.

## Operational Modes
| Mode | Current flag examples | Recommended Use |
|------|-----------------------|-----------------|
| Stdin prompt | `codex exec - < prompt.txt` | Non-interactive sessions |
| Workspace sandbox | `--sandbox workspace-write` | Routine automation |
| Host-level bypass | `--dangerously-bypass-approvals-and-sandbox` | Explicitly approved host writes |

## Pitfalls & Workarounds
- **Binary Data Blindness:** Codex cannot \"see\" images. **Workaround:** Always use `scripts/vision_proxy.py` $\rightarrow$ Text $\rightarrow$ Codex.
- **Sandbox Network Isolation:** Use host's native `terminal()` if Codex hits `ProxyError`.
- **Timeout Management:** Use `timeout=600` in `terminal()` for intensive research loops.
- **Mandatory Persistent Delivery:** Save all generated files (reports, logs) to a permanent location (e.g., `~/`) before completing.
- **Dual-Output Strategy:** Instruct Codex to save to a file AND print the final content to stdout.
