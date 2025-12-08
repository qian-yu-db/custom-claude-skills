# Platform Comparison Reference

Detailed comparison of instruction file features across Claude Code, Codex CLI, and Gemini CLI.

## File Locations

### Claude Code

| Scope | Location |
|-------|----------|
| Global | `~/.claude/CLAUDE.md` |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` |
| Subdirectory | Any `CLAUDE.md` in subdirectories |

### Codex CLI

| Scope | Location |
|-------|----------|
| Global | `~/.codex/AGENTS.md` |
| Project | `./AGENTS.md` |
| Override | `AGENTS.override.md` (takes precedence) |
| Fallback | Configurable via `project_doc_fallback_filenames` |

### Gemini CLI

| Scope | Location |
|-------|----------|
| Global | `~/.gemini/GEMINI.md` |
| Project | `./GEMINI.md` (searches up to `.git` root) |
| Subdirectory | Any `GEMINI.md` in subdirectories |
| Imports | `@./path/to/file.md` syntax supported |

## Custom Commands

### Claude Code
```
.claude/commands/
├── review.md
├── test.md
└── deploy.md
```
Invoked as `/project:review`, `/project:test`, etc.

### Codex CLI
```
~/.codex/prompts/
├── review.md
├── test.md
└── deploy.md
```
Invoked as `/prompts:review`, `/prompts:test`, etc.

Frontmatter format:
```yaml
---
description: Run code review
argument-hint: [FILES=<paths>]
---
```

### Gemini CLI
```
.gemini/commands/
├── review.toml
├── test.toml
└── deploy.toml
```

TOML format:
```toml
description = "Run code review"
prompt = """
Review the following code...
"""
```

## MCP Configuration

### Claude Code
File: `.mcp.json` or project config
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-filesystem"]
    }
  }
}
```

### Codex CLI
File: `~/.codex/config.toml`
```toml
[mcp_servers.filesystem]
command = "npx"
args = ["-y", "@anthropic/mcp-filesystem"]
```

### Gemini CLI
File: `.gemini/settings.json`
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-filesystem"]
    }
  }
}
```

Or via extensions in `.gemini/extensions/my-ext/gemini-extension.json`.

## Memory/Context Commands

### Claude Code
- `#` key to add to CLAUDE.md on the fly
- `/init` to generate initial CLAUDE.md
- No built-in memory commands

### Codex CLI
- `/init` creates AGENTS.md
- `/status` shows loaded instruction files
- No runtime memory addition

### Gemini CLI
- `/memory add <text>` - Add to global GEMINI.md
- `/memory show` - Display loaded context
- `/memory refresh` - Reload from files
- `/memory list` - List active files
- `/init` generates GEMINI.md

## Built-in Tools

### Claude Code
- File read/write/edit
- Bash command execution
- Web search (if enabled)
- MCP tool access

### Codex CLI
- File operations
- Shell commands (sandboxed)
- Git operations
- MCP tool access

### Gemini CLI
- ReadFile, ReadManyFiles
- ReadFolder (ls)
- FindFiles (glob)
- SearchText (grep)
- Shell commands
- MCP tool access

## Instruction Priority

### Claude Code
1. System prompt
2. CLAUDE.md (immutable rules)
3. User prompts (flexible requests)

### Codex CLI
1. Global AGENTS.md or AGENTS.override.md
2. Walk from repo root down to CWD
3. One file per directory (override > regular > fallback)

### Gemini CLI
1. Global ~/.gemini/GEMINI.md
2. Project root to CWD (upward search)
3. Subdirectory files (downward scan)
4. More specific overrides general

## Feature Compatibility Matrix

| Feature | Claude Code | Codex CLI | Gemini CLI |
|---------|-------------|-----------|------------|
| Markdown format | ✅ | ✅ | ✅ |
| YAML frontmatter | ✅ | ❌ | ❌ |
| Hierarchical loading | ✅ | ✅ | ✅ |
| File imports | ❌ | ❌ | ✅ (`@file.md`) |
| Override files | ❌ | ✅ (`.override.md`) | ❌ |
| Runtime memory add | ❌ | ❌ | ✅ |
| Custom commands | ✅ | ✅ | ✅ |
| MCP support | ✅ | ✅ | ✅ |
| Sandboxing | ❌ | ✅ | ✅ |

## Conversion Tips

### Universal Content (works everywhere)
- Project structure documentation
- Build and test commands
- Code style guidelines
- Workflow descriptions
- Architecture overviews

### Needs Adaptation
- Slash command references
- MCP configuration
- Tool-specific syntax
- Memory management commands

### Platform-Specific (keep separate)
- Claude: YAML frontmatter for skills
- Codex: Sandbox and approval policies
- Gemini: Import statements, extensions
