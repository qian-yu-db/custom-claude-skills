# Battle Card Creator Skill

## Overview

The **battle-card-creator** skill enables you to perform comprehensive competitive analysis and generate professional battle cards that help product managers and sales teams understand how your product compares against competitors.

## What It Does

This skill:
- ✅ Researches multiple products through web search
- ✅ Compares features, pricing, positioning, and capabilities
- ✅ Generates structured battle cards in **markdown** or **Excel** format
- ✅ Provides honest competitive analysis with actionable insights
- ✅ Includes win/loss themes and objection handling

## How to Use It

### Installation

1. Download the `battle-card-creator.skill` file
2. In Claude.ai or Claude Desktop, go to your Skills settings
3. Click "Add Skill" and upload the `.skill` file
4. The skill is now available for use

### Basic Usage

Simply ask Claude to create a battle card by providing:

**Required:**
- Your main product name
- Competitor product names (1-5 recommended)

**Optional:**
- Specific features/attributes to compare
- Preferred output format (markdown or Excel)

### Example Requests

#### Example 1: Simple Request
```
Create a battle card for Slack (our product) vs Microsoft Teams and Discord
```

#### Example 2: With Specific Focus
```
Create a battle card comparing Salesforce against HubSpot and Zoho CRM. 
Focus on: lead management, email integration, pricing, and mobile apps.
I'd like the output in Excel format.
```

#### Example 3: File Upload
Upload a CSV file with this structure:
```csv
Product,Type
Notion,Main
Confluence,Competitor
Microsoft OneNote,Competitor

Attributes
Real-time collaboration
Template library
Pricing
Mobile experience
```

Then ask:
```
Use this file to create a battle card for Notion
```

## What You'll Get

### Markdown Output
A comprehensive document with:
- Executive summary
- Product overviews
- Feature comparison table
- Competitive positioning (strengths & weaknesses)
- Win/loss themes
- Pricing comparison
- Key differentiators
- Objection handling strategies
- Discovery questions for sales
- Resources and proof points

### Excel Output
A multi-sheet workbook with:
- **Summary** sheet: Executive overview
- **Feature Matrix** sheet: Detailed side-by-side comparison
- **Positioning** sheet: Strengths, weaknesses, differentiators
- **Pricing** sheet: Pricing models and TCO analysis
- **Win/Loss** sheet: When you win vs when you lose
- **Objections** sheet: Common objections with responses

## Skill Capabilities

### Research Depth
- Performs 3-5+ web searches per product
- Fetches official documentation and product pages
- Reviews customer sentiment from G2, Capterra, TrustRadius
- Analyzes comparison articles and user discussions
- Synthesizes information from multiple authoritative sources

### Competitive Analysis
- Identifies key differentiators
- Highlights your competitive advantages
- Honestly acknowledges competitor strengths
- Provides counter-positioning strategies
- Synthesizes win/loss patterns

### Output Quality
- Professional, scannable formatting
- Actionable insights for sales teams
- Evidence-based claims with citations
- Clear comparison tables
- Honest and credible analysis

## Limitations

**Information Availability:**
- Some product details may not be publicly available
- Enterprise pricing often requires sales contact
- Internal roadmaps are confidential
- Recent changes may not appear in search results

**Accuracy:**
- Information is point-in-time (products change frequently)
- User reviews reflect individual experiences
- Always validate critical claims with internal knowledge

**Scope:**
- Optimal for 1 main product vs 1-5 competitors
- More competitors = less depth per competitor
- Deep technical comparisons may require domain expertise

## Best Practices

1. **Be Specific**: Provide clear product names and specific features to compare
2. **Validate**: Review the battle card and validate critical claims with your product team
3. **Update Regularly**: Competitive landscape changes—refresh battle cards quarterly
4. **Focus**: Limit to 1-5 competitors for depth; split into multiple cards if needed
5. **Customize**: Use the generated battle card as a starting point and add internal intelligence

## Support

If you encounter issues or have suggestions for improvement:
- The skill uses Claude's web search to find public information
- For proprietary data, you'll need to provide it separately
- Contact Anthropic support for technical issues with the skill system

## Version

Version 1.0 - November 2025

---

**Ready to create your first battle card?** Just ask Claude to create one and provide your product names!
