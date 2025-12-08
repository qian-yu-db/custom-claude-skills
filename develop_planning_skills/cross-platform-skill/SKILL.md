---
name: cross-platform-skill
description: Convert Claude Code skills to work with Codex CLI and Gemini CLI. Use when users want to make their CLAUDE.md or skill files compatible with other AI coding assistants, share skills with a wider audience, or create multi-agent instruction files. Trigger phrases include "make skill work with codex", "convert to gemini", "cross-platform skill", "multi-agent instructions", "share skill with codex/gemini users".
---

# Cross-Platform Skill Converter

Convert Claude Code skills and CLAUDE.md files to work across multiple AI coding assistants: Codex CLI (OpenAI) and Gemini CLI (Google).

## Platform Instruction File Reference

| Platform | File Name | Global Location | Project Location |
|----------|-----------|-----------------|------------------|
| Claude Code | `CLAUDE.md` | `~/.claude/CLAUDE.md` | Project root |
| Codex CLI | `AGENTS.md` | `~/.codex/AGENTS.md` | Project root |
| Gemini CLI | `GEMINI.md` | `~/.gemini/GEMINI.md` | Project root |

All three use Markdown format with similar semantics, making conversion straightforward.

## Conversion Workflow

### Step 1: Analyze Source

Read the source skill/instruction file and identify:
- Core instructions (universal, work everywhere)
- Tool-specific references (Claude Code `/commands`, MCP configs, etc.)
- Platform-specific syntax or features

### Step 2: Generate Platform Files

Run the conversion script to generate all platform variants:

```bash
python scripts/convert_skill.py <source-file> --output-dir <target-dir>
```

This creates:
- `CLAUDE.md` - Original or adapted for Claude Code
- `AGENTS.md` - Adapted for Codex CLI  
- `GEMINI.md` - Adapted for Gemini CLI

### Step 3: Handle Platform-Specific Features

Some features need adaptation:

**Claude Code → Codex CLI:**
- `/project:command` → Custom prompts in `~/.codex/prompts/`
- `.claude/commands/` → `.codex/prompts/`
- MCP in `.mcp.json` → MCP in `~/.codex/config.toml`

**Claude Code → Gemini CLI:**
- `/project:command` → Custom commands in `.gemini/commands/`
- `.claude/commands/` → `.gemini/extensions/`
- MCP in `.mcp.json` → MCP in `.gemini/settings.json`

### Step 4: Choose Sync Strategy

**Option A: Symlinks (recommended for personal use)**
```bash
python scripts/setup_symlinks.py <canonical-file>
```

**Option B: Copy with sync script (recommended for repos)**
```bash
python scripts/create_sync_script.py <source-file> --output sync-instructions.sh
```

**Option C: Git hook (auto-sync on commit)**
```bash
python scripts/install_git_hook.py
```

## Output Formats

### Unified Skill Package

For distributing skills that work everywhere, create a package structure:

```
my-skill/
├── CLAUDE.md          # Claude Code version
├── AGENTS.md          # Codex CLI version  
├── GEMINI.md          # Gemini CLI version
├── instructions.md    # Canonical source (optional)
├── scripts/           # Shared scripts (work with all)
├── references/        # Shared reference docs
└── sync.sh           # Keeps files in sync
```

### Repo-Level Instructions

For project repositories, add all three files at root:
```
my-project/
├── CLAUDE.md
├── AGENTS.md
├── GEMINI.md
└── ... (project files)
```

## Compatibility Notes

### Fully Compatible Features
- Markdown formatting and structure
- Code style guidelines
- Build/test commands
- Project structure documentation
- Coding conventions
- General workflow instructions

### Platform-Specific Adaptations Needed
- Slash commands (different syntax per platform)
- MCP server configuration (different config files)
- Tool references (different built-in tools)
- Memory/context commands

### Script Compatibility

Python and bash scripts in `scripts/` directories generally work across all platforms since they execute in the shell. Only the instruction file format differs.

## Quick Start Examples

### Convert a CLAUDE.md to all platforms:
```bash
python scripts/convert_skill.py ./CLAUDE.md --output-dir ./
```

### Set up symlinks from CLAUDE.md as canonical:
```bash
python scripts/setup_symlinks.py ./CLAUDE.md
```

### Create a complete cross-platform skill package:
```bash
python scripts/package_cross_platform.py ./my-skill/ --output ./dist/
```
