#!/data/data/com.termux/files/usr/bin/bash
set -e

# FOZO Toolkit installer for Termux
if [ -z "${PREFIX:-}" ] || [ ! -d "$PREFIX" ] || [[ "$PREFIX" != *com.termux* ]]; then
  echo "This installer is intended for Termux on Android."
  echo "Open Termux and run: bash install.sh"
  exit 1
fi

APP_DIR="$HOME/.fozo-toolkit"
BIN_DIR="$PREFIX/bin"
mkdir -p "$APP_DIR"

echo "==> Checking dependencies..."
pkg update -y
pkg install -y python git

echo "==> Installing FOZO Toolkit..."
cp -r "$(cd "$(dirname "$0")" && pwd)/fozo_toolkit/." "$APP_DIR/"
cat > "$BIN_DIR/fozo" <<'LAUNCHER'
#!/data/data/com.termux/files/usr/bin/bash
exec python "$HOME/.fozo-toolkit/main.py" "$@"
LAUNCHER
chmod +x "$BIN_DIR/fozo"

echo
echo "Installation complete!"
echo "Run the toolkit with: fozo"
echo "To update later, download the new repo and run: bash install.sh"
