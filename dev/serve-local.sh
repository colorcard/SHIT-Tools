#!/bin/bash
set -e

# 切换到项目根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

echo "🚀 Starting local deployment..."

# Validate source files
if [ ! -f "docs/shitjournal_downloader.html" ]; then
    echo "❌ Error: docs/shitjournal_downloader.html not found"
    exit 1
fi

if [ ! -f "docs/analysis.html" ]; then
    echo "❌ Error: docs/analysis.html not found"
    exit 1
fi

if [ ! -f "data/scraped_articles.json" ]; then
    echo "❌ Error: data/scraped_articles.json not found"
    exit 1
fi

# Clean and create site directory
echo "📁 Creating site directory..."
rm -rf site
mkdir site

# Compress articles
echo "🗜️ Compressing articles..."
python3 src/compress_articles.py

# Copy files (matching GitHub workflow)
echo "📋 Copying files..."
cp docs/shitjournal_downloader.html site/index.html
cp docs/analysis.html site/analysis.html

echo "✅ Site built successfully!"
echo ""
echo "🌐 Starting local server at http://localhost:8000"
echo "📖 Press Ctrl+C to stop"
echo ""

# Open browser
open http://localhost:8000

# Start server
cd site && python3 -m http.server 8000
