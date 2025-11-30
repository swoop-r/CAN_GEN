#!/bin/ksh

echo "========================================="
echo " CAN_GEN OpenBSD Environment Installer"
echo "========================================="

# --- SAFETY CHECK ---
if [ "$(id -u)" -ne 0 ]; then
    echo "[!] Run this script as root."
    exit 1
fi

# --- STEP 1: Disable PF (temp workaround for package fetch issues) ---
echo "[*] Disabling pf temporarily..."
pfctl -d
sleep 1

# --- STEP 2: Sync packages + install Python ---
echo "[*] Installing Python 3 and related packages..."
pkg_add python%3.12 py3-pipx py3-virtualenv

# NOTE:
#   py3-pip  (the actual pip package) does not exist on OpenBSD; pipx or venv are recommended.
#   venv gets installed as part of python3.

# --- STEP 3: Create project venv ---
PROJECT_DIR="/root/can_project"
VENV_DIR="$PROJECT_DIR/can_env"

echo "[*] Creating project directory at $PROJECT_DIR..."
mkdir -p "$PROJECT_DIR"

echo "[*] Creating Python virtual environment..."
python3 -m venv "$VENV_DIR"

# --- STEP 4: Activate venv & install Python deps ---
echo "[*] Activating venv and installing CAN tools..."
. "$VENV_DIR/bin/activate"

pip install --upgrade pip
pip install cantools python-can

# --- STEP 5: Deactivate environment ---
deactivate

# --- STEP 6: Re-enable PF ---
echo "[*] Re-enabling pf..."
pfctl -e

echo "========================================="
echo " Installation complete!"
echo "========================================="
echo ""
echo "To start working:"
echo "    . $VENV_DIR/bin/activate"
echo ""
echo "Your Python CAN environment is ready."
