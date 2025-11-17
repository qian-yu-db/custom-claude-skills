#!/bin/bash

##############################################################################
# Deploy Agent to Databricks Model Serving using Asset Bundles
#
# Usage: ./deploy.sh [TARGET] [PROFILE] [OPTIONS]
#
# Arguments:
#   TARGET   - Deployment target (dev, staging, prod). Default: dev
#   PROFILE  - Databricks CLI profile name. Default: DEFAULT
#
# Options:
#   --auto-approve    - Skip confirmation prompts
#   --force           - Force re-deployment
#   --debug           - Enable debug output
#
# Examples:
#   ./deploy.sh dev my-profile
#   ./deploy.sh prod my-profile --auto-approve
##############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
TARGET="${1:-dev}"
PROFILE="${2:-DEFAULT}"
AUTO_APPROVE=""
FORCE=""
DEBUG=""

# Parse additional arguments
shift 2 2>/dev/null || true
while [[ $# -gt 0 ]]; do
    case $1 in
        --auto-approve)
            AUTO_APPROVE="--auto-approve"
            shift
            ;;
        --force)
            FORCE="--force"
            shift
            ;;
        --debug)
            DEBUG="--debug"
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

echo -e "${GREEN}=== Databricks Agent Deployment ===${NC}"
echo "Target: $TARGET"
echo "Profile: $PROFILE"
echo ""

# Check if databricks CLI is installed
if ! command -v databricks &> /dev/null; then
    echo -e "${RED}Error: Databricks CLI not found${NC}"
    echo "Install with: pip install databricks-cli"
    exit 1
fi

# Check if databricks.yml exists
if [ ! -f "databricks.yml" ]; then
    echo -e "${RED}Error: databricks.yml not found${NC}"
    echo "Are you in the correct directory?"
    exit 1
fi

# Step 1: Validate bundle
echo -e "${YELLOW}Step 1: Validating bundle...${NC}"
if ! databricks bundle validate -t "$TARGET" --var="databricks_profile=$PROFILE" $DEBUG; then
    echo -e "${RED}Bundle validation failed!${NC}"
    echo "Please fix the errors above and try again."
    exit 1
fi
echo -e "${GREEN}✓ Bundle validation passed${NC}"
echo ""

# Step 2: Show deployment plan
echo -e "${YELLOW}Step 2: Deployment plan${NC}"
databricks bundle plan -t "$TARGET" --var="databricks_profile=$PROFILE" $DEBUG
echo ""

# Step 3: Confirm deployment (unless auto-approve)
if [ -z "$AUTO_APPROVE" ]; then
    read -p "Continue with deployment? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Deployment cancelled${NC}"
        exit 0
    fi
fi

# Step 4: Deploy
echo -e "${YELLOW}Step 3: Deploying bundle...${NC}"
if databricks bundle deploy -t "$TARGET" --var="databricks_profile=$PROFILE" $AUTO_APPROVE $FORCE $DEBUG; then
    echo -e "${GREEN}✓ Deployment successful!${NC}"
else
    echo -e "${RED}✗ Deployment failed${NC}"
    exit 1
fi
echo ""

# Step 5: Get endpoint information
echo -e "${YELLOW}Step 4: Retrieving endpoint information...${NC}"

# Extract endpoint name from databricks.yml (assuming it's in variables)
ENDPOINT_NAME=$(grep -A 10 "^targets:" databricks.yml | grep -A 5 "$TARGET:" | grep "endpoint_name:" | head -1 | awk '{print $2}' | tr -d '"')

if [ -z "$ENDPOINT_NAME" ]; then
    echo -e "${YELLOW}Could not determine endpoint name automatically${NC}"
    echo "Use: databricks serving-endpoints list"
else
    echo "Endpoint name: $ENDPOINT_NAME"
    echo ""

    # Wait for endpoint to be ready
    echo "Waiting for endpoint to be ready..."
    MAX_WAIT=300  # 5 minutes
    WAIT_TIME=0
    SLEEP_INTERVAL=10

    while [ $WAIT_TIME -lt $MAX_WAIT ]; do
        STATUS=$(databricks serving-endpoints get --name "$ENDPOINT_NAME" --profile "$PROFILE" 2>/dev/null | grep -o '"ready":"[^"]*"' | cut -d'"' -f4 || echo "UNKNOWN")

        if [ "$STATUS" = "READY" ]; then
            echo -e "${GREEN}✓ Endpoint is ready!${NC}"
            break
        elif [ "$STATUS" = "UPDATE_FAILED" ] || [ "$STATUS" = "CREATION_FAILED" ]; then
            echo -e "${RED}✗ Endpoint deployment failed${NC}"
            exit 1
        else
            echo "Endpoint status: $STATUS (waiting...)"
            sleep $SLEEP_INTERVAL
            WAIT_TIME=$((WAIT_TIME + SLEEP_INTERVAL))
        fi
    done

    if [ $WAIT_TIME -ge $MAX_WAIT ]; then
        echo -e "${YELLOW}Endpoint is still deploying (check status manually)${NC}"
    fi

    echo ""
    echo -e "${GREEN}=== Deployment Complete ===${NC}"
    echo ""
    echo "Endpoint: $ENDPOINT_NAME"
    echo ""
    echo "Test your endpoint with:"
    echo "  ./scripts/test_endpoint.sh $ENDPOINT_NAME $PROFILE"
    echo ""
    echo "Or manually:"
    echo "  databricks serving-endpoints query-endpoint \\"
    echo "    --name $ENDPOINT_NAME \\"
    echo "    --profile $PROFILE \\"
    echo "    --json '{\"messages\": [{\"role\": \"user\", \"content\": \"Hello\"}]}'"
fi
