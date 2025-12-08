#!/usr/bin/env python3
"""
Set up symlinks so one canonical instruction file works for all platforms.

Usage:
    python setup_symlinks.py <canonical-file> [--global] [--dry-run]
    
Examples:
    # Project-level symlinks (in current directory)
    python setup_symlinks.py CLAUDE.md
    
    # Global symlinks (in home config directories)
    python setup_symlinks.py ~/.claude/CLAUDE.md --global
    
    # Preview what would be created
    python setup_symlinks.py CLAUDE.md --dry-run
"""

import argparse
import os
import sys
from pathlib import Path


# Mapping of canonical file to platform symlinks
PLATFORM_FILES = {
    'CLAUDE.md': ['AGENTS.md', 'GEMINI.md'],
    'AGENTS.md': ['CLAUDE.md', 'GEMINI.md'],
    'GEMINI.md': ['CLAUDE.md', 'AGENTS.md'],
}

# Global config directories
GLOBAL_DIRS = {
    'CLAUDE.md': Path.home() / '.claude',
    'AGENTS.md': Path.home() / '.codex',
    'GEMINI.md': Path.home() / '.gemini',
}


def create_symlink(target: Path, link: Path, dry_run: bool = False) -> bool:
    """Create a symlink, handling existing files."""
    if link.exists() or link.is_symlink():
        if link.is_symlink():
            current_target = link.resolve()
            if current_target == target.resolve():
                print(f"  [skip] {link} -> already points to {target}")
                return True
            else:
                if dry_run:
                    print(f"  [would update] {link} -> {target} (currently -> {current_target})")
                    return True
                print(f"  [update] {link} -> {target} (was -> {current_target})")
                link.unlink()
        else:
            print(f"  [warning] {link} exists and is not a symlink. Skipping.")
            print(f"            Remove it manually if you want to create a symlink.")
            return False
    else:
        if dry_run:
            print(f"  [would create] {link} -> {target}")
            return True
    
    if not dry_run:
        # Create relative symlink if in same directory, absolute otherwise
        if link.parent == target.parent:
            link.symlink_to(target.name)
        else:
            link.symlink_to(target.resolve())
        print(f"  [created] {link} -> {target}")
    
    return True


def setup_project_symlinks(canonical: Path, dry_run: bool = False) -> None:
    """Set up symlinks in the project directory."""
    canonical = canonical.resolve()
    canonical_name = canonical.name
    
    if canonical_name not in PLATFORM_FILES:
        print(f"Warning: {canonical_name} is not a recognized platform file.")
        print(f"Expected one of: {', '.join(PLATFORM_FILES.keys())}")
        print("Proceeding anyway...")
        # Default to creating both other platform files
        targets = ['CLAUDE.md', 'AGENTS.md', 'GEMINI.md']
        targets = [t for t in targets if t != canonical_name]
    else:
        targets = PLATFORM_FILES[canonical_name]
    
    print(f"\nSetting up project symlinks:")
    print(f"  Canonical: {canonical}")
    
    for target_name in targets:
        link_path = canonical.parent / target_name
        create_symlink(canonical, link_path, dry_run)


def setup_global_symlinks(canonical: Path, dry_run: bool = False) -> None:
    """Set up symlinks in global config directories."""
    canonical = canonical.resolve()
    canonical_name = canonical.name
    
    if canonical_name not in GLOBAL_DIRS:
        print(f"Error: {canonical_name} must be one of: {', '.join(GLOBAL_DIRS.keys())}")
        sys.exit(1)
    
    print(f"\nSetting up global symlinks:")
    print(f"  Canonical: {canonical}")
    
    for platform_file, config_dir in GLOBAL_DIRS.items():
        if platform_file == canonical_name:
            continue
        
        # Ensure config directory exists
        if not config_dir.exists():
            if dry_run:
                print(f"  [would create dir] {config_dir}")
            else:
                config_dir.mkdir(parents=True, exist_ok=True)
                print(f"  [created dir] {config_dir}")
        
        link_path = config_dir / platform_file
        create_symlink(canonical, link_path, dry_run)


def main():
    parser = argparse.ArgumentParser(
        description='Set up symlinks for cross-platform instruction files'
    )
    parser.add_argument(
        'canonical',
        type=Path,
        help='The canonical instruction file to link from'
    )
    parser.add_argument(
        '--global', '-g',
        dest='is_global',
        action='store_true',
        help='Set up global symlinks in home config directories'
    )
    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help='Show what would be done without making changes'
    )
    
    args = parser.parse_args()
    
    if not args.canonical.exists():
        print(f"Error: Canonical file not found: {args.canonical}", file=sys.stderr)
        sys.exit(1)
    
    if args.dry_run:
        print("=== DRY RUN - No changes will be made ===\n")
    
    if args.is_global:
        setup_global_symlinks(args.canonical, args.dry_run)
    else:
        setup_project_symlinks(args.canonical, args.dry_run)
    
    print()
    if args.dry_run:
        print("Run without --dry-run to apply changes.")
    else:
        print("Done! All platforms will now use the same instruction file.")
        print()
        print("Remember: Edit only the canonical file. Symlinks will reflect changes automatically.")


if __name__ == '__main__':
    main()
