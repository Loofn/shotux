#!/bin/bash

# Shotux Build Script
# Creates distribution packages for easy installation

set -e

echo "📦 Building Shotux distribution packages..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Clean previous builds
echo -e "${BLUE}Cleaning previous builds...${NC}"
rm -rf build/ dist/ *.egg-info/

# Build source distribution
echo -e "${BLUE}Building source distribution...${NC}"
python3 setup.py sdist

# Build wheel distribution
echo -e "${BLUE}Building wheel distribution...${NC}"
python3 setup.py bdist_wheel

# Create installation archive
echo -e "${BLUE}Creating installation archive...${NC}"
mkdir -p dist/shotux-install
cp -r shotux data README.md LICENSE requirements.txt setup.py MANIFEST.in install.sh dist/shotux-install/
cd dist
tar -czf shotux-install.tar.gz shotux-install/
cd ..

echo ""
echo -e "${GREEN}✅ Build complete!${NC}"
echo ""
echo "Generated files:"
ls -la dist/

echo ""
echo "Installation methods:"
echo "1. From wheel: pip install dist/shotux-*.whl"
echo "2. From source: pip install dist/shotux-*.tar.gz"
echo "3. From archive: tar -xzf dist/shotux-install.tar.gz && cd shotux-install && ./install.sh"
