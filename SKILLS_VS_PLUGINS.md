# Skills vs Plugins: When to Convert

This guide helps decide when to keep a skill as standalone `SKILL.md` vs converting to a full plugin structure.

## Key Differences

| Aspect | Skill (SKILL.md) | Plugin |
|--------|------------------|--------|
| **Structure** | Single SKILL.md file | `.claude-plugin/plugin.json` + components |
| **Invocation** | `/skill-name` | `/plugin-name:command` (namespaced) |
| **Distribution** | Manual file copy | Marketplace or git submodule |
| **Components** | Single instruction file | Skills, commands, agents, hooks, MCP servers |
| **Use case** | Personal/project-specific | Team/community sharing |

## When to Convert to Plugin

**Convert when:**

1. **Sharing with team or community** via marketplace
2. **Multiple related commands** (like git-worktree with add/list/clean)
3. **Hooks needed** for automated validation or event handling
4. **MCP servers** for external service integration
5. **Versioning** required for stable releases

**Keep as standalone skill when:**

1. Personal or project-specific use
2. Single capability without multiple commands
3. Simpler invocation preferred (`/skill` vs `/plugin:skill`)
4. Still iterating on the design

## Skill Conversion Recommendations

### Strong Candidates for Plugin

| Skill | Reason |
|-------|--------|
| **git-worktree** | Already converted - reference template |
| **databricks-agent-app-builder** | Complex workflow, could have create/deploy/evaluate commands |
| **pytest-test-creator** | Could bundle hooks to auto-run tests on file changes |
| **python-code-formatter** | Could add hooks for auto-format on save |

### Keep as Standalone Skills

| Skill | Reason |
|-------|--------|
| **mermaid-diagrams-creator** | Single-purpose, works well as skill |
| **jira-epic-creator** | Single-purpose, straightforward |
| **cross-platform-skill** | Single-purpose conversion utility |
| **project-starter** | Orchestration skill that invokes other skills |
| **Databricks platform skills** | Project-specific, benefit from simpler invocation |

### Consider Case-by-Case

| Skill | Consideration |
|-------|---------------|
| **skill-creator** | Convert if sharing the skill-building workflow |
| **databricks-workspace-organizer** | Could benefit from MCP server integration |

## Plugin Structure Template

Based on git-worktree conversion:

```
skill-name/
├── .claude-plugin/
│   └── plugin.json           # Manifest only
├── commands/                  # Slash commands
│   ├── command-one.md
│   └── command-two.md
├── skills/                    # Optional: complex skills
│   └── skill-name/
│       └── SKILL.md
├── agents/                    # Optional: subagents
├── hooks/                     # Optional: event handlers
│   └── hooks.json
├── README.md
└── QUICK_REFERENCE.md         # Optional
```

### plugin.json Format

```json
{
  "name": "plugin-name",
  "description": "Brief description of what the plugin does"
}
```

### Command File Format

```markdown
---
allowed-tools: Bash(command:*), Read, Edit
description: What this command does
---

# Command Title

Instructions for the command...
```

## Conversion Checklist

When converting a skill to plugin:

1. [ ] Create `.claude-plugin/plugin.json` with name and description
2. [ ] Break SKILL.md into individual command files in `commands/`
3. [ ] Add `allowed-tools` frontmatter to each command
4. [ ] Update SKILL.md to serve as overview/index
5. [ ] Test each command works independently
6. [ ] Update README.md with new invocation syntax

## Reference Implementation

See `git_skills/git-worktree/` for a complete working example:
- `plugin.json`: Minimal manifest
- `commands/worktree-add.md`: Create worktree with auto-setup
- `commands/worktree-list.md`: List worktrees with merge status
- `commands/worktree-clean.md`: Remove merged worktrees
- `SKILL.md`: Overview and quick reference
