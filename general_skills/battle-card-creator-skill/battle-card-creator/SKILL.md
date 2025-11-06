---
name: battle-card-creator
description: Create comprehensive competitive battle cards for product managers performing competitive analysis. Use when user requests competitive analysis, battle cards, or product comparisons. Accepts product names and attributes/features to compare (via text or uploaded files), performs web research on each product, and generates detailed battle cards in markdown or Excel format showing how the main product compares against competitors.
---

# Battle Card Creator

Create competitive battle cards that help product managers and sales teams understand how their product stacks up against competitors.

## Overview

This skill enables systematic competitive analysis by:
1. Researching multiple products through web search
2. Comparing features, pricing, and positioning
3. Generating structured battle cards in markdown or Excel format

## Input Formats

Accept inputs in these formats:

**Text-based**: User provides product names and attributes directly in conversation

**File-based**: User uploads file with:
- List of products to compare
- Attributes/features to analyze
- Designation of "our product" (the main product)

### Required Information
- **Main product**: The product you're creating the battle card for
- **Competitor products**: 1-5 competitor products to analyze
- **Comparison attributes** (optional): Specific features or criteria to evaluate

If attributes aren't specified, use standard battle card dimensions from the template.

## Workflow

### Step 1: Understand Requirements

Parse the user's request to identify:
- Main product name
- Competitor product names (1-5 competitors recommended)
- Specific attributes/features to compare
- Output format preference (markdown or Excel)

If critical information is missing, ask the user before proceeding.

### Step 2: Conduct Research

Read `references/research_guidelines.md` for detailed methodology.

For EACH product, perform web research to gather:

**Core Information:**
- Product overview and value proposition
- Target audience and use cases
- Key features and capabilities
- Pricing model and tiers
- Company background

**Competitive Intelligence:**
- Strengths and differentiators
- Known weaknesses or limitations
- Customer reviews and sentiment
- Recent updates or developments
- Market positioning

**Research Strategy:**
Use 3-5 web searches per product minimum:
- `web_search`: "[Product] features"
- `web_search`: "[Product] pricing"
- `web_search`: "[Product] vs [Competitor]"
- `web_search`: "[Product] reviews"
- `web_fetch`: Official product pages and documentation

Prioritize authoritative sources:
- Official product websites and docs
- Review sites (G2, Capterra, TrustRadius, Gartner)
- Comparison articles
- Recent news and updates

### Step 3: Analyze and Synthesize

After gathering information:
1. Identify key differentiators across all products
2. Determine where main product has advantages
3. Acknowledge where competitors are stronger (be honest)
4. Note feature parity areas
5. Synthesize win/loss themes based on patterns

### Step 4: Generate Battle Card

Read `references/battle_card_template.md` for complete structure.

#### For Markdown Output

Create comprehensive markdown document with these sections:
1. **Executive Summary**: 2-3 sentence overview and key positioning
2. **Product Overviews**: Brief description of each product
3. **Feature Comparison Table**: Side-by-side comparison using ✓, ✗, ~
4. **Competitive Positioning**: Strengths, weaknesses, neutralization strategies
5. **Win/Loss Themes**: When you win, when you lose
6. **Pricing Comparison**: Models, starting prices, TCO considerations
7. **Key Differentiators**: Top 3-5 unique selling propositions
8. **Handling Objections**: Common objections with responses
9. **Discovery Questions**: Questions to qualify prospects
10. **Resources**: Case studies, proof points, supporting materials

**Formatting:**
- Use clear headers (##, ###)
- Use tables for feature comparisons
- Bold key advantages
- Keep executive summary concise

#### For Excel Output

Create multi-sheet workbook with:
- **Summary**: Executive summary and quick reference
- **Feature Matrix**: Detailed feature-by-feature table
- **Positioning**: Strengths, weaknesses, differentiators
- **Pricing**: Pricing models and TCO analysis
- **Win/Loss**: Scenarios and themes
- **Objections**: Common objections and responses

**Implementation with openpyxl:**

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = Workbook()

# Format headers
header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
header_font = Font(color="FFFFFF", bold=True)

# Create and format each sheet
# Use checkmarks (✓), x marks (✗), or "~" for partial support
# Color coding: 
#   - Green (C6EFCE) for advantages
#   - Yellow (FFEB9C) for parity
#   - Red (FFC7CE) for disadvantages

# Auto-adjust column widths
for sheet in wb.worksheets:
    for column in sheet.columns:
        max_length = 0
        column_letter = get_column_letter(column[0].column)
        for cell in column:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        sheet.column_dimensions[column_letter].width = min(max_length + 2, 50)

wb.save('/mnt/user-data/outputs/battle-card-[product].xlsx')
```

### Step 5: Deliver Output

**Markdown:** Save to `/mnt/user-data/outputs/battle-card-[main-product].md`

**Excel:** Save to `/mnt/user-data/outputs/battle-card-[main-product].xlsx`

Provide download link using `computer://` format.

Include brief summary of key findings (2-3 sentences) but keep it concise.

## Best Practices

### Research Quality
- Prioritize recent information (last 6-12 months)
- Verify critical claims with multiple sources
- Cite sources for specific data points in battle card
- Flag missing or uncertain information clearly
- Don't speculate on unavailable data—note as "Not publicly available"

### Battle Card Effectiveness
- **Be honest** about competitor strengths (credibility matters)
- Provide actionable counter-positioning, not just complaints
- Focus on customer-relevant differentiators, not just features
- Include specific proof points and examples when available
- Make objection handling practical for sales conversations

### Output Quality
- Use scannable formatting (tables, bullets, bold for emphasis)
- Prioritize most important information in executive summary
- Keep executive summary to 3-5 sentences maximum
- Use comparison tables for easy scanning
- Bold or highlight key advantages

## Limitations and Transparency

### Information Availability
- Detailed product specs may not be publicly available
- Enterprise pricing often requires sales contact
- Internal roadmaps and strategies are confidential
- Recent product changes may not appear in search results
- Some features may be documented poorly

**Response:** Note gaps clearly rather than speculating. Use phrases like "Not publicly available" or "Requires contact with sales team."

### Information Accuracy
- Web search provides point-in-time information
- Product features change frequently
- User reviews reflect individual experiences and may not be representative
- Marketing claims may not match reality

**Response:** 
- Prioritize official sources over secondary sources
- Note information recency (e.g., "As of November 2024...")
- Flag when sources conflict
- Recommend user validate critical claims

### Scope Management
- Optimal: 1 main product vs 1-5 competitors
- More competitors reduce depth per competitor
- Deep technical comparisons may require domain expertise
- Industry-specific use cases may need user input

**Response:**
- Recommend splitting into multiple battle cards if >5 competitors
- Note when domain expertise would improve analysis
- Suggest user validate technical claims with product teams

## Output Format Selection Guide

**Use Markdown when:**
- User prefers readable document format
- Battle card for internal reference or documentation
- Single-page overview needed
- Easy sharing and printing desired
- User doesn't specify format

**Use Excel when:**
- Detailed feature matrix with many attributes required
- User needs to customize or edit data
- Multiple comparison dimensions across sheets
- Filtering and sorting capabilities needed
- User specifically requests spreadsheet format

**If user doesn't specify:** Default to markdown for simplicity, but offer Excel as alternative.

## Example Interactions

**Example 1:**
User: "Create a battle card comparing Slack (our product) against Microsoft Teams and Discord. Focus on enterprise collaboration features."

Actions:
1. Research Slack, Microsoft Teams, Discord
2. Focus research on: enterprise features, security, integrations, administration, pricing
3. Create battle card showing Slack's competitive positioning
4. Generate markdown output (default)
5. Provide download link

**Example 2:**
User uploads CSV with products: Salesforce (main), HubSpot, Zoho CRM, and attributes: Lead management, Email integration, Pricing, Mobile app

Actions:
1. Parse CSV to extract products and attributes
2. Research each CRM on specified attributes
3. Create Excel battle card with feature matrix sheet
4. Include pricing and positioning sheets
5. Provide download link

## Resources

This skill includes two reference files:

### references/battle_card_template.md
Complete structure and section definitions for battle cards. Read this file before generating output to ensure all required sections are included with appropriate depth and formatting.

### references/research_guidelines.md
Comprehensive methodology for conducting competitive research, including search strategies, source prioritization, and quality checks. Read this file at the beginning of Step 2 (Research phase) to execute thorough and systematic research.
