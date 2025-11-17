#!/bin/bash

##############################################################################
# Test Databricks Model Serving Endpoint
#
# Usage: ./test_endpoint.sh [ENDPOINT_NAME] [PROFILE] [QUERY]
#
# Arguments:
#   ENDPOINT_NAME - Name of the serving endpoint
#   PROFILE       - Databricks CLI profile (default: DEFAULT)
#   QUERY         - Test query (default: "Hello, how are you?")
#
# Examples:
#   ./test_endpoint.sh my-agent-dev
#   ./test_endpoint.sh my-agent-prod my-profile
#   ./test_endpoint.sh my-agent-dev DEFAULT "What is Databricks?"
##############################################################################

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Arguments
ENDPOINT_NAME="$1"
PROFILE="${2:-DEFAULT}"
QUERY="${3:-Hello, how are you?}"

if [ -z "$ENDPOINT_NAME" ]; then
    echo -e "${RED}Error: Endpoint name required${NC}"
    echo "Usage: $0 ENDPOINT_NAME [PROFILE] [QUERY]"
    exit 1
fi

echo -e "${GREEN}=== Testing Model Serving Endpoint ===${NC}"
echo "Endpoint: $ENDPOINT_NAME"
echo "Profile: $PROFILE"
echo "Query: $QUERY"
echo ""

# Check if endpoint exists and get status
echo -e "${YELLOW}Checking endpoint status...${NC}"
if ! databricks serving-endpoints get --name "$ENDPOINT_NAME" --profile "$PROFILE" > /dev/null 2>&1; then
    echo -e "${RED}Error: Endpoint '$ENDPOINT_NAME' not found${NC}"
    exit 1
fi

STATUS=$(databricks serving-endpoints get --name "$ENDPOINT_NAME" --profile "$PROFILE" | grep -o '"ready":"[^"]*"' | cut -d'"' -f4 || echo "UNKNOWN")

echo "Status: $STATUS"

if [ "$STATUS" != "READY" ]; then
    echo -e "${YELLOW}Warning: Endpoint is not ready yet${NC}"
    echo "Current status: $STATUS"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

# Prepare query JSON
QUERY_JSON=$(cat <<EOF
{
  "messages": [
    {
      "role": "user",
      "content": "$QUERY"
    }
  ]
}
EOF
)

# Query endpoint
echo ""
echo -e "${YELLOW}Sending query to endpoint...${NC}"
echo ""

RESPONSE=$(databricks serving-endpoints query-endpoint \
    --name "$ENDPOINT_NAME" \
    --profile "$PROFILE" \
    --json "$QUERY_JSON" 2>&1)

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ Response received:${NC}"
    echo ""
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
    echo ""
    echo -e "${GREEN}=== Test Successful ===${NC}"
else
    echo -e "${RED}✗ Error querying endpoint:${NC}"
    echo "$RESPONSE"
    exit 1
fi

# Show additional info
echo ""
echo "To query the endpoint programmatically:"
echo ""
echo "Python:"
echo "  from databricks.sdk import WorkspaceClient"
echo "  from databricks.sdk.service.serving import ChatMessage, ChatMessageRole"
echo ""
echo "  w = WorkspaceClient(profile='$PROFILE')"
echo "  response = w.serving_endpoints.query("
echo "      name='$ENDPOINT_NAME',"
echo "      messages=[ChatMessage(role=ChatMessageRole.USER, content='$QUERY')]"
echo "  )"
echo ""
echo "cURL:"
echo "  curl -X POST \\"
echo "    \${DATABRICKS_HOST}/serving-endpoints/$ENDPOINT_NAME/invocations \\"
echo "    -H 'Authorization: Bearer \${DATABRICKS_TOKEN}' \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '$QUERY_JSON'"
