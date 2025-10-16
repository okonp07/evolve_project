#!/bin/bash

# Setup script for Minimum Stay Recommender Repository
# This script creates the complete directory structure and initializes git

set -e  # Exit on error

echo "=================================="
echo "Minimum Stay Recommender Setup"
echo "=================================="
echo ""

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Project name
PROJECT_NAME="minstay-recommender"

# Check if directory already exists
if [ -d "$PROJECT_NAME" ]; then
    echo -e "${YELLOW}Warning: Directory $PROJECT_NAME already exists.${NC}"
    read -p "Do you want to remove it and continue? (yes/no): " answer
    if [ "$answer" = "yes" ]; then
        rm -rf "$PROJECT_NAME"
        echo "Removed existing directory."
    else
        echo "Setup cancelled."
        exit 1
    fi
fi

echo -e "${BLUE}Creating project directory structure...${NC}"

# Create main directory
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

# Create subdirectories
mkdir -p .streamlit
mkdir -p src
mkdir -p data
mkdir -p notebooks
mkdir -p tests

echo -e "${GREEN}✓${NC} Directory structure created"

# Create empty __init__ files
touch src/__init__.py
touch tests/__init__.py

echo -e "${GREEN}✓${NC} Created __init__.py files"

# Create main files
echo -e "${BLUE}Creating main application files...${NC}"

touch app.py
touch requirements.txt
touch README.md
touch .gitignore
touch DEPLOYMENT.md

echo -e "${GREEN}✓${NC} Main files created"

# Create configuration file
touch .streamlit/config.toml

echo -e "${GREEN}✓${NC} Configuration files created"

# Create source files
touch src/recommendation_engine.py
touch src/data_processor.py

echo -e "${GREEN}✓${NC} Source files created"

# Create test files
touch tests/test_recommender.py

echo -e "${GREEN}✓${NC} Test files created"

# Create notebook files
touch notebooks/eda.ipynb
touch notebooks/analysis.ipynb

echo -e "${GREEN}✓${NC} Notebook files created"

# Create placeholder for data
echo "# Place your minstay_experiment.csv file in this directory" > data/README.md

echo -e "${GREEN}✓${NC} Data directory initialized"

# Initialize git repository
echo -e "${BLUE}Initializing git repository...${NC}"
git init
git branch -M main

echo -e "${GREEN}✓${NC} Git repository initialized"

# Create .gitattributes for consistent line endings
cat > .gitattributes << 'EOF'
# Auto detect text files and perform LF normalization
* text=auto

# Python files
*.py text eol=lf

# Documentation
*.md text eol=lf
*.txt text eol=lf

# Configuration
*.toml text eol=lf
*.yaml text eol=lf
*.yml text eol=lf

# Notebooks
*.ipynb text eol=lf

# Shell scripts
*.sh text eol=lf
EOF

echo -e "${GREEN}✓${NC} Git attributes configured"

# Display directory structure
echo ""
echo -e "${BLUE}Repository structure created:${NC}"
echo ""

tree -L 2 -a 2>/dev/null || find . -maxdepth 2 -print | sed 's|^\./||' | sort

echo ""
echo -e "${GREEN}=================================="
echo "Setup Complete! ✓"
echo "==================================${NC}"
echo ""
echo "Next steps:"
echo ""
echo "1. Copy the provided code into each file"
echo "2. Add your minstay_experiment.csv to the data/ directory"
echo "3. Test locally:"
echo -e "   ${YELLOW}cd $PROJECT_NAME${NC}"
echo -e "   ${YELLOW}python -m venv venv${NC}"
echo -e "   ${YELLOW}source venv/bin/activate${NC}  # On Windows: venv\\Scripts\\activate"
echo -e "   ${YELLOW}pip install -r requirements.txt${NC}"
echo -e "   ${YELLOW}streamlit run app.py${NC}"
echo ""
echo "4. Create GitHub repository and push:"
echo -e "   ${YELLOW}git add .${NC}"
echo -e "   ${YELLOW}git commit -m 'Initial commit: Minimum Stay Recommender'${NC}"
echo -e "   ${YELLOW}git remote add origin https://github.com/USERNAME/minstay-recommender.git${NC}"
echo -e "   ${YELLOW}git push -u origin main${NC}"
echo ""
echo "5. Deploy to Streamlit Cloud:"
echo "   Visit: https://share.streamlit.io"
echo ""
echo "For detailed instructions, see DEPLOYMENT.md"
echo ""
