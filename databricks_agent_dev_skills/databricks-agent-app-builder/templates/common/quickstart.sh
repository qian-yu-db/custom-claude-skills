#!/bin/bash
set -e

# Helper function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Helper function to check if Homebrew is available
has_brew() {
    command_exists brew
}

echo "==================================================================="
echo "Agent App - Quickstart Setup"
echo "==================================================================="
echo

# ===================================================================
# Section 1: Prerequisites Installation
# ===================================================================

echo "Checking and installing prerequisites..."
echo

# Check and install UV
if command_exists uv; then
    echo "✓ UV is already installed"
    uv --version
else
    echo "Installing UV..."
    if has_brew; then
        echo "Using Homebrew to install UV..."
        brew install uv
    else
        echo "Using curl to install UV..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$HOME/.cargo/bin:$PATH"
    fi
    echo "✓ UV installed successfully"
fi

# Check and install Databricks CLI
if command_exists databricks; then
    echo "✓ Databricks CLI is already installed"
    databricks --version
else
    echo "Installing Databricks CLI..."
    if has_brew; then
        echo "Using Homebrew to install Databricks CLI..."
        brew tap databricks/tap
        brew install databricks
    else
        echo "Using curl to install Databricks CLI..."
        if curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh; then
            echo "✓ Databricks CLI installed successfully"
        else
            echo "Installation failed, trying with sudo..."
            curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sudo sh
        fi
    fi
    echo "✓ Databricks CLI installed successfully"
fi
echo

# ===================================================================
# Section 2: Configuration Files Setup
# ===================================================================
echo "Setting up configuration files..."

# Copy .env.example to .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "Copying .env.example to .env.local..."
    cp .env.example .env.local
else
    echo ".env.local already exists, skipping copy..."
fi
echo

# ===================================================================
# Section 3: Databricks Authentication
# ===================================================================

echo "Setting up Databricks authentication..."

# Check if there are existing profiles
set +e
EXISTING_PROFILES=$(databricks auth profiles 2>/dev/null)
PROFILES_EXIT_CODE=$?
set -e

if [ $PROFILES_EXIT_CODE -eq 0 ] && [ -n "$EXISTING_PROFILES" ]; then
    echo "Found existing Databricks profiles:"
    echo

    PROFILE_ARRAY=()
    PROFILE_NAMES=()
    LINE_NUM=0
    while IFS= read -r line; do
        if [ -n "$line" ]; then
            if [ $LINE_NUM -eq 0 ]; then
                echo "$line"
            else
                PROFILE_ARRAY+=("$line")
                PROFILE_NAME_ONLY=$(echo "$line" | awk '{print $1}')
                PROFILE_NAMES+=("$PROFILE_NAME_ONLY")
            fi
            LINE_NUM=$((LINE_NUM + 1))
        fi
    done <<< "$EXISTING_PROFILES"
    echo

    for i in "${!PROFILE_ARRAY[@]}"; do
        echo "$((i+1))) ${PROFILE_ARRAY[$i]}"
    done
    echo

    echo "Enter the number of the profile you want to use:"
    read -r PROFILE_CHOICE

    if [ -z "$PROFILE_CHOICE" ]; then
        echo "Error: Profile selection is required"
        exit 1
    fi

    if ! [[ "$PROFILE_CHOICE" =~ ^[0-9]+$ ]]; then
        echo "Error: Please enter a valid number"
        exit 1
    fi

    PROFILE_INDEX=$((PROFILE_CHOICE - 1))

    if [ $PROFILE_INDEX -lt 0 ] || [ $PROFILE_INDEX -ge ${#PROFILE_NAMES[@]} ]; then
        echo "Error: Invalid selection"
        exit 1
    fi

    PROFILE_NAME="${PROFILE_NAMES[$PROFILE_INDEX]}"
    echo "Selected profile: $PROFILE_NAME"

    set +e
    DATABRICKS_CONFIG_PROFILE="$PROFILE_NAME" databricks current-user me >/dev/null 2>&1
    PROFILE_TEST=$?
    set -e

    if [ $PROFILE_TEST -eq 0 ]; then
        echo "✓ Successfully validated profile '$PROFILE_NAME'"
    else
        echo "Profile '$PROFILE_NAME' is not authenticated."
        echo "Authenticating..."
        databricks auth login --profile "$PROFILE_NAME"
        echo "✓ Successfully authenticated profile '$PROFILE_NAME'"
    fi

    if grep -q "DATABRICKS_CONFIG_PROFILE=" .env.local; then
        sed -i '' "s/DATABRICKS_CONFIG_PROFILE=.*/DATABRICKS_CONFIG_PROFILE=$PROFILE_NAME/" .env.local
    else
        echo "DATABRICKS_CONFIG_PROFILE=$PROFILE_NAME" >> .env.local
    fi
    echo "✓ Databricks profile '$PROFILE_NAME' saved to .env.local"
else
    echo "No existing profiles found. Setting up Databricks authentication..."
    echo "Please enter your Databricks host URL (e.g., https://your-workspace.cloud.databricks.com):"
    read -r DATABRICKS_HOST

    if [ -z "$DATABRICKS_HOST" ]; then
        echo "Error: Databricks host is required"
        exit 1
    fi

    echo "Authenticating with Databricks..."
    databricks auth login --host "$DATABRICKS_HOST"

    PROFILE_NAME="DEFAULT"
    if grep -q "DATABRICKS_CONFIG_PROFILE=" .env.local; then
        sed -i '' "s/DATABRICKS_CONFIG_PROFILE=.*/DATABRICKS_CONFIG_PROFILE=$PROFILE_NAME/" .env.local
    else
        echo "DATABRICKS_CONFIG_PROFILE=$PROFILE_NAME" >> .env.local
    fi
    echo "✓ Databricks profile '$PROFILE_NAME' saved to .env.local"
fi
echo

# ===================================================================
# Section 4: MLflow Experiment Setup
# ===================================================================

echo "Getting Databricks username..."
DATABRICKS_USERNAME=$(databricks -p $PROFILE_NAME current-user me | jq -r .userName)
echo "Username: $DATABRICKS_USERNAME"
echo

echo "Creating MLflow experiment..."
EXPERIMENT_NAME="/Users/$DATABRICKS_USERNAME/agent-app"

if EXPERIMENT_RESPONSE=$(databricks -p $PROFILE_NAME experiments create-experiment $EXPERIMENT_NAME 2>/dev/null); then
    EXPERIMENT_ID=$(echo $EXPERIMENT_RESPONSE | jq -r .experiment_id)
    echo "Created experiment '$EXPERIMENT_NAME' with ID: $EXPERIMENT_ID"
else
    echo "Experiment name already exists, creating with random suffix..."
    RANDOM_SUFFIX=$(openssl rand -hex 4)
    EXPERIMENT_NAME="/Users/$DATABRICKS_USERNAME/agent-app-$RANDOM_SUFFIX"
    EXPERIMENT_RESPONSE=$(databricks -p $PROFILE_NAME experiments create-experiment $EXPERIMENT_NAME)
    EXPERIMENT_ID=$(echo $EXPERIMENT_RESPONSE | jq -r .experiment_id)
    echo "Created experiment '$EXPERIMENT_NAME' with ID: $EXPERIMENT_ID"
fi
echo

echo "Updating .env.local with experiment ID..."
sed -i '' "s/MLFLOW_EXPERIMENT_ID=.*/MLFLOW_EXPERIMENT_ID=$EXPERIMENT_ID/" .env.local
echo

echo "==================================================================="
echo "Setup Complete!"
echo "==================================================================="
echo "✓ Prerequisites installed (UV, Databricks CLI)"
echo "✓ Databricks authenticated with profile: $PROFILE_NAME"
echo "✓ Configuration files created (.env.local)"
echo "✓ MLflow experiment created: $EXPERIMENT_NAME"
echo "✓ Experiment ID: $EXPERIMENT_ID"
echo "==================================================================="
echo
echo "To start the server, run:"
echo "  uv run start-server"
echo
