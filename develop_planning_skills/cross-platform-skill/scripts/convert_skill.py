#!/usr/bin/env python3
"""
Convert Claude Code skills/instructions to work with Codex CLI and Gemini CLI.

Usage:
    python convert_skill.py <source-file> [--output-dir <dir>] [--canonical <name>]
    
Examples:
    python convert_skill.py CLAUDE.md
    python convert_skill.py CLAUDE.md --output-dir ./dist
    python convert_skill.py my-skill/SKILL.md --output-dir ./cross-platform
"""

import argparse
import re
import sys
from pathlib import Path


# Platform-specific replacements for slash commands and references
CLAUDE_TO_CODEX = {
    r'/project:(\w+)': r'/prompts:\1',
    r'\.claude/commands/': '.codex/prompts/',
    r'\.mcp\.json': '~/.codex/config.toml (mcp_servers section)',
    r'Claude Code': 'Codex CLI',
    r'claude code': 'Codex CLI',
}

CLAUDE_TO_GEMINI = {
    r'/project:(\w+)': r'/\1',
    r'\.claude/commands/': '.gemini/commands/',
    r'\.mcp\.json': '.gemini/settings.json (mcpServers section)',
    r'Claude Code': 'Gemini CLI',
    r'claude code': 'Gemini CLI',
}


def read_file(path: Path) -> str:
    """Read file content."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(path: Path, content: str) -> None:
    """Write content to file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Created: {path}")


def extract_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter from markdown content."""
    frontmatter = {}
    body = content
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            # Parse simple YAML frontmatter
            for line in parts[1].strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip()
            body = parts[2].strip()
    
    return frontmatter, body


def apply_replacements(content: str, replacements: dict) -> str:
    """Apply regex replacements to content."""
    result = content
    for pattern, replacement in replacements.items():
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    return result


def add_platform_header(content: str, platform: str, source_name: str) -> str:
    """Add a header noting the source and platform."""
    header = f"<!-- Generated from {source_name} for {platform} -->\n"
    header += f"<!-- Keep in sync with canonical source -->\n\n"
    return header + content


def convert_to_codex(content: str, source_name: str) -> str:
    """Convert Claude instructions to Codex CLI format."""
    frontmatter, body = extract_frontmatter(content)
    
    # Apply text replacements
    converted = apply_replacements(body, CLAUDE_TO_CODEX)
    
    # Add platform-specific notes if MCP is mentioned
    if '.mcp.json' in content.lower() or 'mcp' in content.lower():
        mcp_note = """
> **Codex CLI MCP Configuration**: Configure MCP servers in `~/.codex/config.toml`:
> ```toml
> [mcp_servers.my-server]
> command = "npx"
> args = ["-y", "@my/mcp-server"]
> ```

"""
        converted = mcp_note + converted
    
    return add_platform_header(converted, "Codex CLI", source_name)


def convert_to_gemini(content: str, source_name: str) -> str:
    """Convert Claude instructions to Gemini CLI format."""
    frontmatter, body = extract_frontmatter(content)
    
    # Apply text replacements
    converted = apply_replacements(body, CLAUDE_TO_GEMINI)
    
    # Add platform-specific notes if MCP is mentioned
    if '.mcp.json' in content.lower() or 'mcp' in content.lower():
        mcp_note = """
> **Gemini CLI MCP Configuration**: Configure MCP servers in `.gemini/settings.json`:
> ```json
> {
>   "mcpServers": {
>     "my-server": {
>       "command": "npx",
>       "args": ["-y", "@my/mcp-server"]
>     }
>   }
> }
> ```

"""
        converted = mcp_note + converted
    
    # Add Gemini-specific memory tip
    memory_tip = """
> **Tip**: Use `/memory add <instruction>` to add rules to your global GEMINI.md on the fly.

"""
    converted = memory_tip + converted
    
    return add_platform_header(converted, "Gemini CLI", source_name)


def convert_skill(source_path: Path, output_dir: Path) -> dict:
    """Convert a skill file to all platform formats."""
    content = read_file(source_path)
    source_name = source_path.name
    
    results = {}
    
    # Determine output filenames based on source
    if source_path.name == 'SKILL.md':
        # It's a skill file - extract the skill name for context
        frontmatter, _ = extract_frontmatter(content)
        skill_name = frontmatter.get('name', source_path.parent.name)
        claude_name = 'CLAUDE.md'
        codex_name = 'AGENTS.md'
        gemini_name = 'GEMINI.md'
    else:
        claude_name = 'CLAUDE.md'
        codex_name = 'AGENTS.md'
        gemini_name = 'GEMINI.md'
    
    # Generate Claude version (copy or adapt)
    claude_path = output_dir / claude_name
    if source_path.name != 'CLAUDE.md':
        # Convert SKILL.md format to CLAUDE.md format
        _, body = extract_frontmatter(content)
        write_file(claude_path, body)
    else:
        write_file(claude_path, content)
    results['claude'] = claude_path
    
    # Generate Codex version
    codex_path = output_dir / codex_name
    codex_content = convert_to_codex(content, source_name)
    write_file(codex_path, codex_content)
    results['codex'] = codex_path
    
    # Generate Gemini version
    gemini_path = output_dir / gemini_name
    gemini_content = convert_to_gemini(content, source_name)
    write_file(gemini_path, gemini_content)
    results['gemini'] = gemini_path
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='Convert Claude Code skills to work with Codex CLI and Gemini CLI'
    )
    parser.add_argument(
        'source',
        type=Path,
        help='Source file (CLAUDE.md, SKILL.md, or any markdown instruction file)'
    )
    parser.add_argument(
        '--output-dir', '-o',
        type=Path,
        default=None,
        help='Output directory (default: same as source)'
    )
    
    args = parser.parse_args()
    
    if not args.source.exists():
        print(f"Error: Source file not found: {args.source}", file=sys.stderr)
        sys.exit(1)
    
    output_dir = args.output_dir or args.source.parent
    
    print(f"Converting: {args.source}")
    print(f"Output directory: {output_dir}")
    print()
    
    results = convert_skill(args.source, output_dir)
    
    print()
    print("Conversion complete!")
    print()
    print("Generated files:")
    for platform, path in results.items():
        print(f"  {platform.capitalize()}: {path}")
    
    print()
    print("Next steps:")
    print("  1. Review generated files for any manual adjustments needed")
    print("  2. Test with each platform to verify compatibility")
    print("  3. Consider setting up symlinks or sync script for ongoing maintenance")


if __name__ == '__main__':
    main()
