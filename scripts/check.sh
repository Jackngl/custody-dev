#!/bin/bash
set -e

echo "🚀 Running local checks (mirroring CI)..."

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Determine the python binary to use
if [ -d ".venv" ]; then
  VENV_PYTHON="./.venv/bin/python3"
  echo "ℹ️  Using virtual environment: $VENV_PYTHON"
else
  VENV_PYTHON="python3"
  echo "⚠️  Warning: No .venv found, using system python."
fi

# Inject mock Home Assistant for local tests if real one is not available
export PYTHONPATH="$PYTHONPATH:$(pwd)/tests/mock_ha"
echo "ℹ️  PYTHONPATH updated to include local mocks."

echo "--- 🧼 Formatting (Black & Isort) ---"
# --force-exclude ensures these are skipped even if black finds them
$VENV_PYTHON -m black --quiet --force-exclude "/\.(venv|git|gemini|pytest_cache|DS_Store|pycache)/|brain/|tests/mock_ha/" custom_components/custody_schedule tests
$VENV_PYTHON -m isort --quiet --skip-glob "**/__pycache__/*" --skip-glob "**/.DS_Store" --skip=tests/mock_ha custom_components/custody_schedule tests

echo "--- 🔍 Linting (Flake8) ---"
# Using --exclude to bypass restricted files
$VENV_PYTHON -m flake8 custom_components/custody_schedule tests --exclude=tests/mock_ha,**/__pycache__,.DS_Store,.venv,.git,.gemini,brain --count --select=E9,F63,F7,F82 --show-source --statistics
$VENV_PYTHON -m flake8 custom_components/custody_schedule tests --exclude=tests/mock_ha,**/__pycache__,.DS_Store,.venv,.git,.gemini,brain --count --max-complexity=10 --max-line-length=127 --statistics

echo "--- 🧪 Unit Tests (Pytest) ---"
# -c /dev/null: ignore local pytest.ini that might have broken paths
# -p no:cacheprovider: disable .pytest_cache (fixes PermissionError in sandbox)
# --ignore: skip system/temp files
if $VENV_PYTHON -m pytest tests \
    -c /dev/null \
    -p no:cacheprovider \
    --ignore=.DS_Store \
    --ignore=.git \
    --ignore=.gemini \
    --ignore=brain \
    --cov=custom_components/custody_schedule \
    --cov-report=term-missing; then
  echo -e "${GREEN}✅ All checks passed! You can safely push.${NC}"
else
  echo -e "${RED}❌ Tests failed or dependencies missing.${NC}"
  echo "💡 Tip: Make sure to 'pip install -r requirements_test.txt' in your .venv"
  exit 1
fi
