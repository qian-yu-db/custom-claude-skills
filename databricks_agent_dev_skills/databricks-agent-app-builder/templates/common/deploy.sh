#!/bin/bash
set -e

# =============================================================================
# Databricks App Deployment Script
# =============================================================================
#
# Usage:
#   ./scripts/deploy.sh <app-name> [options]
#
# Options:
#   --create      Create a new app and deploy
#   --update      Update an existing app
#   --dry-run     Show commands without executing
#   --profile     Databricks CLI profile to use (default: from .env.local or DEFAULT)
#   --help        Show this help message
#
# Examples:
#   ./scripts/deploy.sh my-agent-app --create
#   ./scripts/deploy.sh my-agent-app --update
#   ./scripts/deploy.sh my-agent-app --dry-run --create
#   ./scripts/deploy.sh my-agent-app --create --profile PROD
#
# =============================================================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
DRY_RUN=false
CREATE_APP=false
UPDATE_APP=false
PROFILE=""

# Parse arguments
APP_NAME=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --create)
            CREATE_APP=true
            shift
            ;;
        --update)
            UPDATE_APP=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --profile)
            PROFILE="$2"
            shift 2
            ;;
        --help)
            head -35 "$0" | tail -32
            exit 0
            ;;
        -*)
            echo -e "${RED}Error: Unknown option $1${NC}"
            exit 1
            ;;
        *)
            if [ -z "$APP_NAME" ]; then
                APP_NAME="$1"
            else
                echo -e "${RED}Error: Unexpected argument $1${NC}"
                exit 1
            fi
            shift
            ;;
    esac
done

# Validate arguments
if [ -z "$APP_NAME" ]; then
    echo -e "${RED}Error: App name is required${NC}"
    echo "Usage: ./scripts/deploy.sh <app-name> [--create|--update] [--dry-run]"
    exit 1
fi

if [ "$CREATE_APP" = false ] && [ "$UPDATE_APP" = false ]; then
    echo -e "${YELLOW}No action specified. Use --create or --update${NC}"
    echo "Usage: ./scripts/deploy.sh <app-name> [--create|--update] [--dry-run]"
    exit 1
fi

# Load profile from .env.local if not specified
if [ -z "$PROFILE" ] && [ -f ".env.local" ]; then
    PROFILE=$(grep "DATABRICKS_CONFIG_PROFILE=" .env.local | cut -d'=' -f2 | tr -d '"' | tr -d "'")
fi
PROFILE=${PROFILE:-DEFAULT}

echo "==================================================================="
echo "Databricks App Deployment"
echo "==================================================================="
echo "App Name: $APP_NAME"
echo "Profile: $PROFILE"
echo "Action: $([ "$CREATE_APP" = true ] && echo "Create" || echo "Update")"
echo "Dry Run: $DRY_RUN"
echo "==================================================================="
echo

# Function to run or display command
run_cmd() {
    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}[DRY-RUN]${NC} $*"
    else
        echo -e "${GREEN}Running:${NC} $*"
        "$@"
    fi
}

# Get Databricks username
echo "Getting Databricks username..."
if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}[DRY-RUN]${NC} databricks -p $PROFILE current-user me | jq -r .userName"
    DATABRICKS_USERNAME="<username>"
else
    DATABRICKS_USERNAME=$(databricks -p $PROFILE current-user me | jq -r .userName)
fi
echo "Username: $DATABRICKS_USERNAME"
echo

# Create app if requested
if [ "$CREATE_APP" = true ]; then
    echo "Creating Databricks App..."
    run_cmd databricks -p $PROFILE apps create "$APP_NAME"
    echo
fi

# Sync files to workspace
echo "Syncing files to workspace..."
WORKSPACE_PATH="/Users/$DATABRICKS_USERNAME/$APP_NAME"
run_cmd databricks -p $PROFILE sync . "$WORKSPACE_PATH"
echo

# Deploy app
echo "Deploying app..."
run_cmd databricks -p $PROFILE apps deploy "$APP_NAME" --source-code-path "/Workspace$WORKSPACE_PATH"
echo

echo "==================================================================="
if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}Dry run complete. No changes were made.${NC}"
else
    echo -e "${GREEN}Deployment complete!${NC}"
    echo
    echo "To get the app URL, run:"
    echo "  databricks -p $PROFILE apps get $APP_NAME"
    echo
    echo "To query the app:"
    echo "  TOKEN=\$(databricks -p $PROFILE auth token)"
    echo "  curl -X POST <app-url>/invocations \\"
    echo "    -H \"Authorization: Bearer \$TOKEN\" \\"
    echo "    -H \"Content-Type: application/json\" \\"
    echo "    -d '{\"input\": [{\"role\": \"user\", \"content\": \"hello\"}]}'"
fi
echo "==================================================================="
