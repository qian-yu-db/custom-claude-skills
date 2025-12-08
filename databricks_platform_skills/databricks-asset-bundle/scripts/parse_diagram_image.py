#!/usr/bin/env python3
"""
Parse workflow diagram from image using AI vision capabilities.

This script analyzes workflow diagram images to extract:
- Task names
- Dependencies between tasks
- Execution order

Supports various diagram formats:
- Flowcharts
- Sequence diagrams
- Architecture diagrams
- Hand-drawn sketches
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path
from typing import Dict, List

# Check if anthropic is available
try:
    import anthropic
except ImportError:
    print("❌ Error: anthropic package not installed", file=sys.stderr)
    print("Install with: pip install anthropic", file=sys.stderr)
    sys.exit(1)


def encode_image(image_path: str) -> tuple[str, str]:
    """
    Encode image to base64 and detect media type.

    Args:
        image_path: Path to image file

    Returns:
        Tuple of (base64_data, media_type)
    """
    with open(image_path, 'rb') as f:
        image_data = f.read()

    # Detect media type from extension
    ext = Path(image_path).suffix.lower()
    media_type_map = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.webp': 'image/webp'
    }
    media_type = media_type_map.get(ext, 'image/png')

    return base64.standard_b64encode(image_data).decode('utf-8'), media_type


def parse_diagram_with_ai(image_path: str, api_key: str = None) -> List[Dict]:
    """
    Parse workflow diagram using Claude's vision API.

    Args:
        image_path: Path to diagram image file
        api_key: Anthropic API key (or use ANTHROPIC_API_KEY env var)

    Returns:
        List of task dictionaries with name, path, and dependencies
    """
    if api_key is None:
        api_key = os.environ.get('ANTHROPIC_API_KEY')

    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set", file=sys.stderr)
        print("Set with: export ANTHROPIC_API_KEY=your-api-key", file=sys.stderr)
        sys.exit(1)

    # Encode image
    image_data, media_type = encode_image(image_path)

    # Create Anthropic client
    client = anthropic.Anthropic(api_key=api_key)

    # Prepare prompt
    prompt = """Analyze this workflow diagram and extract the following information:

1. Identify all tasks/nodes in the workflow
2. Determine the dependencies between tasks (which tasks depend on which others)
3. Extract the execution order

Return a JSON array of tasks in this exact format:
[
  {
    "name": "task_name",
    "path": "src/task_name.py",
    "dependencies": ["dependency1", "dependency2"]
  }
]

Rules:
- Task names should be lowercase with underscores (e.g., "extract_data")
- If a task has no dependencies, use an empty array []
- Dependencies should reference the exact task names as they appear in the list
- Include all tasks shown in the diagram

Return ONLY the JSON array, no additional text or explanation."""

    # Call Claude API with vision
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )

    # Extract JSON from response
    response_text = message.content[0].text

    # Try to parse JSON
    try:
        # Remove markdown code blocks if present
        if response_text.strip().startswith('```'):
            lines = response_text.strip().split('\n')
            response_text = '\n'.join(lines[1:-1])  # Remove first and last line

        tasks = json.loads(response_text)
        return tasks
    except json.JSONDecodeError as e:
        print(f"❌ Error: Failed to parse AI response as JSON: {e}", file=sys.stderr)
        print(f"Response: {response_text}", file=sys.stderr)
        sys.exit(1)


def save_task_description(tasks: List[Dict], output_path: str) -> None:
    """
    Save tasks in the text description format for generate_dab.py.

    Args:
        tasks: List of task dictionaries
        output_path: Path to save the description file
    """
    lines = []
    for task in tasks:
        line = f"{task['name']}: {task['path']}"
        if task.get('dependencies'):
            deps = ', '.join(task['dependencies'])
            line += f" [depends_on: {deps}]"
        lines.append(line)

    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))

    print(f"✅ Saved task description to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Parse workflow diagram from image using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:

1. Parse diagram and print JSON:
   scripts/parse_diagram_image.py workflow.png

2. Parse and save as text description:
   scripts/parse_diagram_image.py workflow.png -o tasks.txt

3. Use with generate_dab.py:
   scripts/parse_diagram_image.py workflow.png -o tasks.txt
   scripts/generate_dab.py my_pipeline -d "$(cat tasks.txt)"

Environment variables:
  ANTHROPIC_API_KEY: Required for AI vision analysis
        """
    )

    parser.add_argument(
        "image_path",
        help="Path to workflow diagram image (PNG, JPG, GIF, WebP)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output path for task description file (optional)"
    )
    parser.add_argument(
        "--api-key",
        help="Anthropic API key (or use ANTHROPIC_API_KEY env var)"
    )

    args = parser.parse_args()

    # Check if image exists
    if not Path(args.image_path).exists():
        print(f"❌ Error: Image file not found: {args.image_path}", file=sys.stderr)
        sys.exit(1)

    print(f"🔍 Analyzing workflow diagram: {args.image_path}")

    # Parse diagram
    tasks = parse_diagram_with_ai(args.image_path, args.api_key)

    if not tasks:
        print("❌ Error: No tasks found in diagram", file=sys.stderr)
        sys.exit(1)

    print(f"✅ Found {len(tasks)} tasks in diagram:")
    for task in tasks:
        deps = task.get('dependencies', [])
        dep_str = f" (depends on: {', '.join(deps)})" if deps else ""
        print(f"   - {task['name']}{dep_str}")

    # Save or print
    if args.output:
        save_task_description(tasks, args.output)
        print(f"\n💡 Use with generate_dab.py:")
        print(f"   scripts/generate_dab.py my_bundle -d \"$(cat {args.output})\"")
    else:
        print(f"\n📄 Task description format:")
        for task in tasks:
            line = f"{task['name']}: {task['path']}"
            if task.get('dependencies'):
                deps = ', '.join(task['dependencies'])
                line += f" [depends_on: {deps}]"
            print(f"   {line}")


if __name__ == "__main__":
    main()
