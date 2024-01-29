#!/bin/bash

#run from resturant app with scripts/reaload_db.sh
find . -path "*/migrations/*.py" -not -name "__init__.py" -not -path "*env*" -delete
find . -path "*/migrations/*.pyc" -not -path "*env*" -delete
# rm db.sqlite3
