SCRIPT_DIR=$(dirname "$(realpath "$0")")

cd $SCRIPT_DIR

source .venv/bin/activate

python3 app.py run