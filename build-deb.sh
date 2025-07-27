#!/bin/bash

# Create Debian package for Shotux
# Usage: ./build-deb.sh

set -e

PACKAGE_NAME="shotux"
VERSION="1.0.0"
ARCHITECTURE="all"
MAINTAINER="Shotux Developer <developer@example.com>"
DESCRIPTION="Screenshot tool for Linux with GUI support"

echo "📦 Building Debian package for Shotux..."

# Create package directory structure
DEB_DIR="build/${PACKAGE_NAME}_${VERSION}_${ARCHITECTURE}"
mkdir -p "$DEB_DIR/DEBIAN"
mkdir -p "$DEB_DIR/usr/lib/python3/dist-packages"
mkdir -p "$DEB_DIR/usr/bin"
mkdir -p "$DEB_DIR/usr/share/applications"
mkdir -p "$DEB_DIR/usr/share/pixmaps"
mkdir -p "$DEB_DIR/usr/share/doc/$PACKAGE_NAME"

# Create control file
cat > "$DEB_DIR/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Architecture: $ARCHITECTURE
Maintainer: $MAINTAINER
Depends: python3 (>= 3.8), python3-pil, python3-tk, scrot, xclip
Recommends: xbindkeys
Section: graphics
Priority: optional
Homepage: https://github.com/yourusername/shotux
Description: $DESCRIPTION
 Shotux is a comprehensive screenshot application for Linux that provides
 both GUI and command-line interfaces. It supports multiple capture modes
 including full screen, window, and region selection.
 .
 Features:
  * Multiple screenshot modes
  * Configurable capture delay
  * Auto-save functionality
  * Clipboard integration
  * Global hotkey support
  * Clean and intuitive GUI
EOF

# Create postinst script
cat > "$DEB_DIR/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# Update desktop database
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database -q
fi

# Update mime database
if command -v update-mime-database >/dev/null 2>&1; then
    update-mime-database /usr/share/mime >/dev/null 2>&1
fi

echo "Shotux installed successfully!"
echo "You can now run 'shotux-gui' or find it in your applications menu."
EOF

chmod 755 "$DEB_DIR/DEBIAN/postinst"

# Create postrm script
cat > "$DEB_DIR/DEBIAN/postrm" << 'EOF'
#!/bin/bash
set -e

if [ "$1" = "remove" ]; then
    # Update desktop database
    if command -v update-desktop-database >/dev/null 2>&1; then
        update-desktop-database -q
    fi
fi
EOF

chmod 755 "$DEB_DIR/DEBIAN/postrm"

# Copy package files
cp -r shotux "$DEB_DIR/usr/lib/python3/dist-packages/"
cp data/shotux.desktop "$DEB_DIR/usr/share/applications/"
cp data/shotux.png "$DEB_DIR/usr/share/pixmaps/" 2>/dev/null || true
cp README.md LICENSE "$DEB_DIR/usr/share/doc/$PACKAGE_NAME/"

# Create executable scripts
cat > "$DEB_DIR/usr/bin/shotux-gui" << 'EOF'
#!/usr/bin/python3
import sys
import os
sys.path.insert(0, '/usr/lib/python3/dist-packages')
from shotux.main import main
if __name__ == "__main__":
    main()
EOF

cat > "$DEB_DIR/usr/bin/shotux-cli" << 'EOF'
#!/usr/bin/python3
import sys
import os
sys.path.insert(0, '/usr/lib/python3/dist-packages')
from shotux.cli import main
if __name__ == "__main__":
    main()
EOF

cat > "$DEB_DIR/usr/bin/shotux" << 'EOF'
#!/usr/bin/python3
import sys
import os
sys.path.insert(0, '/usr/lib/python3/dist-packages')
from shotux.main import main
if __name__ == "__main__":
    main()
EOF

chmod 755 "$DEB_DIR/usr/bin/"*

# Build the package
echo "Building package..."
dpkg-deb --build "$DEB_DIR"

# Move to dist directory
mkdir -p dist
mv "${DEB_DIR}.deb" "dist/"

echo "✅ Debian package created: dist/${PACKAGE_NAME}_${VERSION}_${ARCHITECTURE}.deb"
echo ""
echo "To install: sudo dpkg -i dist/${PACKAGE_NAME}_${VERSION}_${ARCHITECTURE}.deb"
echo "To remove:  sudo dpkg -r $PACKAGE_NAME"
