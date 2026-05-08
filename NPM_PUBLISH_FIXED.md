# NPM Publishing Guide - v2.0.4 (FIXED)

## 🔧 What Was Fixed

The previous `package.json` had local development links that broke public NPM publishing:
```json
// ❌ REMOVED - These break NPM publishing
"badge": "link:@/components/ui/badge",
"button": "link:@/components/ui/button",
"card": "link:@/components/ui/card",
"progress": "link:@/components/ui/progress",
"separator": "link:@/components/ui/separator"
```

These have been removed. The package.json now contains only valid NPM dependencies.

## ✅ Pre-Publishing Checklist

```bash
# Verify you're on the advisory-fix-1 branch
git status
# On branch advisory-fix-1

# Verify package.json is clean
cat frontend/package.json | grep -i "link:"
# Should return nothing (no link: dependencies)

# Verify version is set correctly
cat frontend/package.json | grep '"version"'
# Should show: "version": "2.0.4"

# Verify publishConfig is correct
cat frontend/package.json | grep -A 2 "publishConfig"
# Should show: "registry": "https://registry.npmjs.org"
```

## 🚀 Step-by-Step NPM Publishing

### Step 1: Navigate to Frontend Directory
```bash
cd frontend
pwd
# Should output: /home/w4nn4d13/Project/OpenLearnX-ghsa-223g-f5mq-gw33/frontend
```

### Step 2: Test Package Locally (Optional but Recommended)
```bash
# Create tarball to see what would be published
npm pack

# You should see:
# npm notice 
# npm notice 📦  openlearnx@2.0.4
# npm notice === Tarball Contents ===
# ...files being packaged...
# npm notice === Tarball Details ===
# ...
# openlearnx-2.0.4.tgz

# Extract and inspect
mkdir test-package
cd test-package
tar -xzf ../openlearnx-2.0.4.tgz
ls -la package/
# Verify only necessary files are included

cd ..
rm -rf test-package
rm openlearnx-2.0.4.tgz
```

### Step 3: Login to NPM
```bash
npm login
# You'll be prompted for:
# Username: [your npm username, e.g., th30d4y]
# Password: [your npm password]
# Email: [your npm account email]
# 2FA OTP (if enabled): [one-time password]

# Verify login was successful
npm whoami
# Should output your username
```

### Step 4: Publish to Public NPM Registry
```bash
# From the frontend directory
npm publish

# Expected output:
# npm notice 
# npm notice 📦  openlearnx@2.0.4
# npm notice === Tarball Contents ===
# npm notice name:          openlearnx
# npm notice version:       2.0.4
# npm notice filename:      openlearnx-2.0.4.tgz
# npm notice published:     [timestamp]
# npm notice public
# npm notice access:        public
# npm notice ...
```

### Step 5: Verify Publication
```bash
# Check on NPM registry
npm view openlearnx

# Check specific version
npm view openlearnx@2.0.4

# Check package page
# Visit: https://www.npmjs.com/package/openlearnx
```

### Step 6: Test Installation from Another Directory
```bash
# Go to a different directory
cd /tmp
mkdir openlearnx-test
cd openlearnx-test
npm init -y

# Install the published package
npm install openlearnx@2.0.4

# Verify installation
ls node_modules/openlearnx/
npm list openlearnx
# Should show: openlearnx@2.0.4
```

## 🔍 Troubleshooting

### Issue: "npm ERR! code EUNSUPPORTEDPROTOCOL - Unsupported URL Type "link:""
**Status:** ✅ FIXED in this version
**Cause:** Local development dependencies were in package.json
**Solution:** Already applied - link: dependencies removed

### Issue: "npm ERR! code E401 - 401 Unauthorized"
**Cause:** Not logged in or token issue
**Solution:** 
```bash
npm logout
npm login
# Re-enter credentials
```

### Issue: "npm ERR! 404 - Package not found"
**Cause:** Package not yet published or wrong registry
**Solution:**
```bash
# Verify publishConfig
cat package.json | grep -A 2 "publishConfig"
# Should point to: https://registry.npmjs.org

# Verify you're publishing to the right registry
npm config get registry
# Should be: https://registry.npmjs.org
```

### Issue: "You do not have permission to publish this package"
**Cause:** Package name collision or permission issue
**Solution:**
```bash
# Check if package already exists on someone else's account
npm view [package-name]

# If you need a different name, update package.json:
# "name": "openlearnx-v2"
```

## 📦 Package Contents

The published `openlearnx@2.0.4` package includes:

```
README.md
package.json
app/                    # Next.js app directory
components/             # React components
context/               # React context
hooks/                 # Custom React hooks
lib/                   # Utility libraries
public/                # Static assets
styles/                # Global styles
next.config.mjs        # Next.js configuration
postcss.config.mjs     # PostCSS configuration
tailwind.config.ts     # Tailwind CSS configuration
tsconfig.json          # TypeScript configuration
```

## 🚨 Security Note

This release (`2.0.4`) contains critical security fixes:
- ✅ JWT signature verification enabled
- ✅ Token forgery attacks prevented
- ✅ Account takeover vulnerability closed

**All users should upgrade immediately:**
```bash
npm install openlearnx@2.0.4
```

## 📝 Post-Publishing

1. **Update GitHub Release:**
   ```bash
   # Go back to repo root
   cd /home/w4nn4d13/Project/OpenLearnX-ghsa-223g-f5mq-gw33
   
   # Visit GitHub to create release
   # https://github.com/th30d4y/OpenLearnX-ghsa-223g-f5mq-gw33/releases/new?tag=v2.0.4
   # Use content from RELEASE_NOTES_v2.0.4.md
   ```

2. **Update README:**
   - Add v2.0.4 to version history
   - Link to NPM package page

3. **Announce Release:**
   - Security advisory GHSA-223g-f5mq-gw33
   - Recommend immediate upgrade
   - Document JWT signature verification fix

## 🔗 Useful Links

- **NPM Package:** https://www.npmjs.com/package/openlearnx
- **GitHub Repository:** https://github.com/th30d4y/OpenLearnX
- **Security Advisory:** https://github.com/th30d4y/OpenLearnX/security/advisories/GHSA-223g-f5mq-gw33
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)
- **Release Notes:** [RELEASE_NOTES_v2.0.4.md](RELEASE_NOTES_v2.0.4.md)

## ✨ Summary

| Item | Status |
|------|--------|
| JWT signature fix | ✅ Complete |
| Package.json cleaned | ✅ Complete |
| Version bumped to 2.0.4 | ✅ Complete |
| Changelog created | ✅ Complete |
| Release notes created | ✅ Complete |
| Git tag v2.0.4 created | ✅ Complete |
| Ready for NPM publish | ✅ YES |

Everything is ready. Follow the steps above to publish to NPM!
