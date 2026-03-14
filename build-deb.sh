#!/bin/bash
# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.
#
# Build a Debian package for Lyric.
# Usage: ./build-deb.sh [-i] [-h] [version]
#   -i          Build and install the package
#   -h          Show this help message
#   version     Override version (defaults to lyric/__init__.py)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

INSTALL=false

# Parse flags
while getopts "ih" opt; do
    case "$opt" in
        i) INSTALL=true ;;
        h)
            echo "Usage: ./build-deb.sh [-i] [-h] [version]"
            echo ""
            echo "Options:"
            echo "  -i    Build and install the package (runs sudo dpkg -i)"
            echo "  -h    Show this help message"
            echo ""
            echo "Arguments:"
            echo "  version   Override version (defaults to value in lyric/__init__.py)"
            exit 0
            ;;
        *) exit 1 ;;
    esac
done
shift $((OPTIND - 1))

# Extract version from source if not provided
VERSION="${1:-$(grep -oP '__version__\s*=\s*"\K[^"]+' lyric/__init__.py)}"
PKGNAME="python3-lyric-lang"
ARCH="all"  # pure Python, architecture-independent
PKG_DIR="build/${PKGNAME}_${VERSION}_${ARCH}"
DEB_FILE="dist/${PKGNAME}_${VERSION}_${ARCH}.deb"

echo "Building ${PKGNAME} ${VERSION} for ${ARCH}..."

# Clean previous build
rm -rf "$PKG_DIR"

# --- Directory structure ---
# Python package goes under /usr/lib/lyric
# Executable wrapper goes to /usr/bin/lyric
# Stdlib .ly files are included inside the package
INSTALL_DIR="${PKG_DIR}/usr/lib/lyric"
BIN_DIR="${PKG_DIR}/usr/bin"
DOC_DIR="${PKG_DIR}/usr/share/doc/${PKGNAME}"

mkdir -p "$INSTALL_DIR" "$BIN_DIR" "$DOC_DIR" "${PKG_DIR}/DEBIAN"

# --- Copy Python package ---
cp -r lyric/ "$INSTALL_DIR/lyric"

# Remove test files, __pycache__, .pyc from the package
find "$INSTALL_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$INSTALL_DIR" -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true
find "$INSTALL_DIR" -name "*.pyc" -delete 2>/dev/null || true

# --- Create executable wrapper ---
cat > "${BIN_DIR}/lyric" << 'WRAPPER'
#!/usr/bin/env python3
import sys
sys.path.insert(0, "/usr/lib/lyric")
from lyric.cli import main
main()
WRAPPER
chmod 755 "${BIN_DIR}/lyric"

# --- Documentation ---
cp LICENSE "$DOC_DIR/copyright"
if [ -f README.md ]; then
    cp README.md "$DOC_DIR/README.md"
fi

# --- Determine Python dependency ---
# Lyric requires Python >= 3.10
PYTHON_DEP="python3 (>= 3.10)"

# --- DEBIAN/control ---
cat > "${PKG_DIR}/DEBIAN/control" << EOF
Package: ${PKGNAME}
Version: ${VERSION}
Section: devel
Priority: optional
Architecture: ${ARCH}
Depends: ${PYTHON_DEP}
Maintainer: MiraNova Studios <aeonath@miranova.studio>
Homepage: https://lyric-lang.org
Description: Lyric programming language transpiler and interpreter
 Lyric is an experimental programming language that transpiles to
 Python bytecode, developed by MiraNova Studios. This package
 provides the lyric transpiler, interpreter, and standard library.
EOF

# --- Build the .deb ---
mkdir -p dist/
dpkg-deb --build "$PKG_DIR" "$DEB_FILE"

echo ""
echo "Package built: ${DEB_FILE}"

if [ "$INSTALL" = true ]; then
    echo ""
    echo "Installing..."
    sudo dpkg -i "$DEB_FILE"
    echo ""
    echo "Installed. Run 'lyric --version' to verify."
    lyric --version
else
    echo ""
    echo "Install with:"
    echo "  sudo dpkg -i ${DEB_FILE}"
    echo "  or: ./build-deb.sh -i"
    echo ""
    echo "Uninstall with:"
    echo "  sudo dpkg -r ${PKGNAME}"
fi
