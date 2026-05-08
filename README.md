# General Agent

`general-agent` is a Hermes skill that runs the Codex CLI as an autonomous terminal executor. It is intended for tasks that benefit from Codex's observe-and-correct loop, especially system administration, research automation, environment setup, and workflows that need direct filesystem or shell access.

The skill can also handle image-based tasks through a vision bridge. Because Codex itself works from text, `scripts/vision_proxy.py` converts image content into a textual description before Codex reasons over it.

## Original Motivation

This skill was originally created to access GPT-5.5 from Hermes before Hermes supported selecting GPT-5.5 directly. By routing work through the Codex CLI configured with GPT-5.5, Hermes can indirectly use GPT-5.5 while still preserving an auditable terminal workflow.

## Repository Contents

```text
.
├── SKILL.md                 # Hermes skill metadata and execution rules
├── README.md                # User-facing overview and setup guide
├── AGENTS.md                # Contributor guide
└── scripts/
    └── vision_proxy.py      # Image-to-text bridge for Codex workflows
```

## Prerequisites

- Node.js and npm for installing the Codex CLI.
- `@openai/codex` installed globally or otherwise available on `PATH`.
- Git, because Codex expects to run inside a Git repository.
- Hermes vision tooling for multimodal tasks that call `scripts/vision_proxy.py`.

Install or verify Codex:

```sh
npm install -g @openai/codex
which codex
codex --version
```

## Quick Start

Run Codex from an existing Git repository:

```sh
codex exec - < prompt.txt
```

For work that does not already belong to a project, create a scratch repository first:

```sh
mkdir -p /tmp/general-agent-work
cd /tmp/general-agent-work
git init
codex exec - < prompt.txt
```

For image analysis, run the vision proxy and feed its output into the Codex prompt:

```sh
python3 scripts/vision_proxy.py /path/to/image.png
```

Treat the proxy output as the factual visual observation. Codex should reason from that text rather than assuming it can inspect the image directly.

## Recommended Workflow

1. Confirm `codex`, `git`, and any required host tools are available.
2. Write a clear `prompt.txt` with the task, constraints, expected output, and validation requirements.
3. Use `codex exec - < prompt.txt` for non-interactive execution.
4. Inspect generated files, shell output, or diffs before reporting completion.
5. Save important reports or generated artifacts to a persistent path before ending the task.

## Operational Modes

| Mode | Example | Use case |
| --- | --- | --- |
| Standard stdin | `codex exec - < prompt.txt` | Normal non-interactive runs |
| Workspace sandbox | `codex exec --sandbox workspace-write - < prompt.txt` | Routine file edits inside a project |
| Host bypass | `codex exec --dangerously-bypass-approvals-and-sandbox - < prompt.txt` | Explicitly approved host-level operations only |

## Known Trade-offs

- **Codex dependency:** The skill depends on the behavior and availability of the `@openai/codex` package.
- **Vision is indirect:** Image understanding flows through `vision_proxy.py` and may lose detail during text conversion.
- **Git requirement:** Non-project tasks need a temporary Git repository before Codex can run.
- **Nested autonomy:** Running Codex inside Hermes adds overhead, so use this skill when the autonomous terminal loop is worth that cost.
- **Safety boundary:** Host-level bypass mode removes normal sandbox protections and should be used only with explicit approval.

## Development Checks

There is no build step for this repository. Validate script changes with:

```sh
python3 -m py_compile scripts/vision_proxy.py
```

When changing behavior, test with a real local image path and confirm error messages remain clear for missing files or unavailable vision tooling.
