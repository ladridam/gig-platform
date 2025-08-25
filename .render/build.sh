#!/usr/bin/env bash
# .render/build.sh

# Exit on error
set -o errexit

# Modify this line if you need to run other commands before starting
pip install -r requirements.txt

# Initialize the database (if needed)
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Database initialized')
"