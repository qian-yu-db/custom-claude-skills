#!/usr/bin/env python3
"""
Analyze a document and extract key information for Jira epic creation.

This script helps identify problem statements, solutions, and other
epic components from uploaded documents.
"""

import sys
import re
from pathlib import Path


def extract_sections(text: str) -> dict:
    """
    Extract potential epic sections from document text
    
    Returns dict with keys:
    - problem_indicators: List of sentences that might describe problems
    - solution_indicators: List of sentences that might describe solutions
    - metrics: List of numbers/percentages found
    - stakeholders: List of mentioned roles/teams
    - existing_solutions: Mentions of current state or alternatives
    """
    
    result = {
        'problem_indicators': [],
        'solution_indicators': [],
        'metrics': [],
        'stakeholders': [],
        'existing_solutions': [],
        'deliverables': [],
        'impacts': []
    }
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    
    # Problem indicators
    problem_keywords = [
        'problem', 'issue', 'challenge', 'difficulty', 'struggle',
        'pain point', 'bottleneck', 'frustration', 'complaint',
        'unable to', 'cannot', 'difficult to', 'hard to'
    ]
    
    # Solution indicators
    solution_keywords = [
        'solution', 'propose', 'implement', 'build', 'create',
        'develop', 'introduce', 'add', 'improve', 'enable',
        'will allow', 'will provide', 'by implementing'
    ]
    
    # Existing solution indicators
    existing_keywords = [
        'currently', 'today', 'existing', 'workaround', 'manual',
        'right now', 'at present', 'alternative'
    ]
    
    # Deliverable indicators
    deliverable_keywords = [
        'deliverable', 'output', 'feature', 'functionality',
        'capability', 'will deliver', 'will provide'
    ]
    
    # Impact indicators
    impact_keywords = [
        'impact', 'benefit', 'result', 'outcome', 'reduce',
        'increase', 'improve', 'save', 'achieve'
    ]
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        sentence_lower = sentence.lower()
        
        # Check for problem indicators
        if any(keyword in sentence_lower for keyword in problem_keywords):
            result['problem_indicators'].append(sentence)
        
        # Check for solution indicators
        if any(keyword in sentence_lower for keyword in solution_keywords):
            result['solution_indicators'].append(sentence)
        
        # Check for existing solutions
        if any(keyword in sentence_lower for keyword in existing_keywords):
            result['existing_solutions'].append(sentence)
        
        # Check for deliverables
        if any(keyword in sentence_lower for keyword in deliverable_keywords):
            result['deliverables'].append(sentence)
        
        # Check for impacts
        if any(keyword in sentence_lower for keyword in impact_keywords):
            result['impacts'].append(sentence)
    
    # Extract metrics (numbers, percentages, currency)
    metric_patterns = [
        r'\d+%',  # Percentages
        r'\$\d+[,\d]*(?:\.\d+)?[KMB]?',  # Currency
        r'\d+[,\d]*\s*(?:hours?|days?|weeks?|users?|tickets?|points?)',  # Quantities
        r'\d+x',  # Multipliers
    ]
    
    for pattern in metric_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        result['metrics'].extend(matches)
    
    # Extract stakeholder mentions
    stakeholder_patterns = [
        r'\b(?:users?|customers?|team|engineer|developer|designer|PM|product manager|stakeholder)s?\b'
    ]
    
    for pattern in stakeholder_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        result['stakeholders'].extend(set(matches))
    
    return result


def generate_epic_outline(sections: dict) -> str:
    """Generate an epic outline based on extracted information"""
    
    outline = """# Jira Epic Outline

## Extracted Information Analysis

### Potential Problem Statement Content
"""
    if sections['problem_indicators']:
        for item in sections['problem_indicators'][:5]:  # Top 5
            outline += f"- {item}\n"
    else:
        outline += "- [No problem indicators found - needs manual input]\n"
    
    outline += "\n### Potential Solution Content\n"
    if sections['solution_indicators']:
        for item in sections['solution_indicators'][:5]:
            outline += f"- {item}\n"
    else:
        outline += "- [No solution indicators found - needs manual input]\n"
    
    outline += "\n### Existing Solutions Mentioned\n"
    if sections['existing_solutions']:
        for item in sections['existing_solutions'][:5]:
            outline += f"- {item}\n"
    else:
        outline += "- [No existing solution mentions found - needs manual input]\n"
    
    outline += "\n### Potential Deliverables\n"
    if sections['deliverables']:
        for item in sections['deliverables'][:5]:
            outline += f"- {item}\n"
    else:
        outline += "- [No deliverable indicators found - needs manual input]\n"
    
    outline += "\n### Impact Indicators\n"
    if sections['impacts']:
        for item in sections['impacts'][:5]:
            outline += f"- {item}\n"
    else:
        outline += "- [No impact indicators found - needs manual input]\n"
    
    outline += "\n### Metrics Found\n"
    if sections['metrics']:
        for metric in set(sections['metrics'])[:10]:
            outline += f"- {metric}\n"
    else:
        outline += "- [No metrics found - consider adding quantifiable goals]\n"
    
    outline += "\n### Stakeholders Mentioned\n"
    if sections['stakeholders']:
        for stakeholder in set(sections['stakeholders'])[:10]:
            outline += f"- {stakeholder}\n"
    else:
        outline += "- [No stakeholders explicitly mentioned]\n"
    
    outline += """

## Next Steps

1. Review the extracted information above
2. Use this to fill in the epic template sections
3. Add missing context and details
4. Ensure all 5 required sections are complete
5. Break down into user stories

## Epic Template Sections Required

1. Problem Statement or Opportunity Statement
2. Proposed Solution
3. What solutions exist today to address the problem / opportunity statement
4. What does the final deliverable / impact for this project look like?
5. Additional Information for Support Requested
"""
    
    return outline


def main():
    if len(sys.argv) < 2:
        print("Usage: analyze_doc.py <document_text_or_file>")
        print("\nThis script analyzes document content and extracts key information")
        print("for creating Jira epics.")
        sys.exit(1)
    
    input_arg = sys.argv[1]
    
    # Check if it's a file path
    if Path(input_arg).is_file():
        with open(input_arg, 'r', encoding='utf-8') as f:
            text = f.read()
        print(f"📄 Analyzing file: {input_arg}\n")
    else:
        text = input_arg
        print("📄 Analyzing provided text\n")
    
    # Extract sections
    sections = extract_sections(text)
    
    # Generate outline
    outline = generate_epic_outline(sections)
    
    print(outline)
    
    # Optionally save to file
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(outline)
        print(f"\n💾 Saved analysis to: {output_file}")


if __name__ == "__main__":
    main()
