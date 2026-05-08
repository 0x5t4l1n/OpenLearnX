#!/bin/bash

# OpenLearnX v2.0.4 NPM Publishing Test Script
# This script validates the package before publishing to NPM

set -e

echo "🚀 OpenLearnX v2.0.4 - NPM Publishing Test"
echo "==========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
pass() {
    echo -e "${GREEN}✅ $1${NC}"
}

fail() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Test 1: Check if we're in the right directory
echo "📁 Test 1: Checking directory structure..."
if [ -f "frontend/package.json" ]; then
    pass "Found frontend/package.json"
else
    fail "Not in correct directory. Run from project root."
fi

# Test 2: Verify package.json structure
echo ""
echo "📦 Test 2: Validating package.json..."
cd frontend

if [ ! -f "package.json" ]; then
    fail "package.json not found in frontend/"
fi

# Check for required fields
if grep -q '"name": "@th30d4y/openlearnx"' package.json; then
    pass "Package name is correct: @th30d4y/openlearnx"
else
    fail "Package name is incorrect or missing"
fi

if grep -q '"version": "2.0.4"' package.json; then
    pass "Version is correct: 2.0.4"
else
    fail "Version is not 2.0.4"
fi

if grep -q '"private": false' package.json; then
    pass "Package is public (private: false)"
else
    fail "Package is marked as private"
fi

if grep -q 'https://registry.npmjs.org' package.json; then
    pass "Publishing to correct registry: npmjs.org"
else
    fail "Publishing registry not configured correctly"
fi

# Test 3: Check for link: dependencies
echo ""
echo "🔗 Test 3: Checking for local link: dependencies..."
if grep -q 'link:' package.json; then
    fail "Found link: dependencies that break NPM publishing. Package has been fixed."
else
    pass "No link: dependencies found ✅"
fi

# Test 4: Validate JSON
echo ""
echo "🔍 Test 4: Validating JSON syntax..."
if node -e "JSON.parse(require('fs').readFileSync('package.json', 'utf8'))" 2>/dev/null; then
    pass "package.json has valid JSON syntax"
else
    fail "package.json has invalid JSON syntax"
fi

# Test 5: Check npm is installed
echo ""
echo "📋 Test 5: Checking NPM installation..."
if command -v npm &> /dev/null; then
    npm_version=$(npm --version)
    pass "npm is installed (version: $npm_version)"
else
    fail "npm is not installed"
fi

# Test 6: Verify npm registry access
echo ""
echo "🌐 Test 6: Checking npm registry access..."
if npm ping --registry https://registry.npmjs.org 2>/dev/null; then
    pass "Connected to NPM registry"
else
    warn "Could not reach NPM registry (might need internet)"
fi

# Test 7: Check npm login status
echo ""
echo "🔐 Test 7: Checking npm authentication..."
if npm whoami 2>/dev/null > /dev/null; then
    logged_in_user=$(npm whoami 2>/dev/null)
    pass "Logged in as: $logged_in_user"
else
    warn "Not logged in to npm. You'll need to run: npm login"
fi

# Test 8: Dry run of package creation
echo ""
echo "📦 Test 8: Testing package creation (dry run)..."
if npm pack --dry-run 2>&1 | grep -q "@th30d4y/openlearnx@2.0.4"; then
    pass "Package would be created successfully"
else
    fail "Package creation test failed"
fi

echo ""
echo "==========================================="
echo -e "${GREEN}✅ All tests passed!${NC}"
echo ""
echo "🚀 Ready to publish:"
echo "   npm publish"
echo ""
echo "Or test locally first:"
echo "   npm pack && tar -tzf th30d4y-openlearnx-2.0.4.tgz | head -20"
echo ""
