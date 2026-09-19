#!/bin/bash
set -e

echo "🚀 Setting up Database Co-Pilot..."

# 1. Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created."
fi

# 2. Activate virtual environment
source venv/bin/activate

# 3. Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Initialize and seed databases
echo "🗄️ Initializing SQLite datasets..."
python setup_dbs.py

# 5. Run test suite
echo "🧪 Running Pytest suite..."
pytest test_db_explorer.py -v

echo "🎉 Setup complete! Server is ready."
