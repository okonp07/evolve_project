@echo off
REM Setup script for Minimum Stay Recommender Repository (Windows)
REM This script creates the complete directory structure

echo ==================================
echo Minimum Stay Recommender Setup
echo ==================================
echo.

set PROJECT_NAME=minstay-recommender

REM Check if directory already exists
if exist "%PROJECT_NAME%" (
    echo Warning: Directory %PROJECT_NAME% already exists.
    set /p answer="Do you want to remove it and continue? (yes/no): "
    if /i "%answer%"=="yes" (
        rmdir /s /q "%PROJECT_NAME%"
        echo Removed existing directory.
    ) else (
        echo Setup cancelled.
        exit /b 1
    )
)

echo Creating project directory structure...

REM Create main directory
mkdir "%PROJECT_NAME%"
cd "%PROJECT_NAME%"

REM Create subdirectories
mkdir .streamlit
mkdir src
mkdir data
mkdir notebooks
mkdir tests

echo [OK] Directory structure created

REM Create empty __init__ files
type nul > src\__init__.py
type nul > tests\__init__.py

echo [OK] Created __init__.py files

REM Create main files
echo Creating main application files...

type nul > app.py
type nul > requirements.txt
type nul > README.md
type nul > .gitignore
type nul > DEPLOYMENT.md

echo [OK] Main files created

REM Create configuration file
type nul > .streamlit\config.toml

echo [OK] Configuration files created

REM Create source files
type nul > src\recommendation_engine.py
type nul > src\data_processor.py

echo [OK] Source files created

REM Create test files
type nul > tests\test_recommender.py

echo [OK] Test files created

REM Create notebook files
type nul > notebooks\eda.ipynb
type nul > notebooks\analysis.ipynb

echo [OK] Notebook files created

REM Create placeholder for data
echo # Place your minstay_experiment.csv file in this directory > data\README.md

echo [OK] Data directory initialized

REM Initialize git repository
echo Initializing git repository...
git init
git branch -M main

echo [OK] Git repository initialized

echo.
echo ==================================
echo Setup Complete!
echo ==================================
echo.
echo Next steps:
echo.
echo 1. Copy the provided code into each file
echo 2. Add your minstay_experiment.csv to the data\ directory
echo 3. Test locally:
echo    cd %PROJECT_NAME%
echo    python -m venv venv
echo    venv\Scripts\activate
echo    pip install -r requirements.txt
echo    streamlit run app.py
echo.
echo 4. Create GitHub repository and push:
echo    git add .
echo    git commit -m "Initial commit: Minimum Stay Recommender"
echo    git remote add origin https://github.com/USERNAME/minstay-recommender.git
echo    git push -u origin main
echo.
echo 5. Deploy to Streamlit Cloud:
echo    Visit: https://share.streamlit.io
echo.
echo For detailed instructions, see DEPLOYMENT.md
echo.

pause
