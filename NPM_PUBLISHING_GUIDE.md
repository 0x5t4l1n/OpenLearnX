# NPM Publishing Instructions for v2.0.4

## Pre-Publishing Checklist

✅ Version updated to 2.0.4 in `frontend/package.json`
✅ CHANGELOG.md created with v2.0.4 entry
✅ RELEASE_NOTES_v2.0.4.md created
✅ Git tag v2.0.4 created and pushed
✅ Branch `advisory-fix-1` ready for publishing

## Step 1: Prepare for Publishing

```bash
# Navigate to the frontend directory where package.json is located
cd frontend

# Verify the version is correct
cat package.json | grep '"version"'
# Output should show: "version": "2.0.4"

# Verify npm is installed
npm --version

# Check npm registry
npm config get registry
# Should show: https://registry.npmjs.org/
```

## Step 2: Login to NPM (if not already logged in)

```bash
# Login to npm registry
npm login

# You will be prompted for:
# - Username: th30d4y
# - Password: [your npm password]
# - Email: [your registered email]
# - OTP: [if 2FA is enabled, provide the one-time password]
```

## Step 3: Publish to NPM

```bash
# From the frontend directory where package.json is located
npm publish

# Expected output:
# npm notice 
# npm notice 📦  openlearnx@2.0.4
# npm notice === Tarball Contents ===
# npm notice ...
# npm notice === Dist Files ===
# npm notice ...
# npm notice === Tarball Details ===
# npm notice name:          openlearnx
# npm notice version:       2.0.4
# npm notice filename:      openlearnx-2.0.4.tgz
# npm notice published:     [timestamp]
# npm notice public
# npm notice url:           https://www.npmjs.com/package/openlearnx
# npm notice access:        public
# npm notice...
```

## Step 4: Verify Publication

```bash
# Check the package on NPM registry
npm view openlearnx

# Check specific version
npm view openlearnx@2.0.4

# You should see:
# openlearnx@2.0.4 | ISC | deps: 39 | versions: 2
```

## Step 5: Test Installation

```bash
# Test in a clean directory
mkdir /tmp/test-openlearnx && cd /tmp/test-openlearnx
npm init -y
npm install openlearnx@2.0.4

# Verify the installation
npm list openlearnx
# Should show: openlearnx@2.0.4
```

## Alternative: Using npm ci (for CI/CD)

```bash
cd frontend
npm ci  # Install exact versions from package-lock.json
npm publish
```

## Troubleshooting

### Issue: "You must be logged in to publish"
**Solution:** Run `npm login` and verify your credentials

### Issue: "You do not have permission to publish this package"
**Solution:** 
- Verify you're logged in: `npm whoami`
- Check package name in package.json matches your npm account
- Ensure you have publish permissions for the package

### Issue: "This version has already been published"
**Solution:** 
- Use a different version number
- Use `npm unpublish openlearnx@2.0.4` (if allowed) and republish

### Issue: "npm notice... WARN"
**Solution:** These are usually non-critical warnings. Review them but the publish should still succeed.

## Post-Publishing

1. **Update the GitHub Release:**
   - Go to https://github.com/th30d4y/OpenLearnX-ghsa-223g-f5mq-gw33/releases
   - Create a new release for tag v2.0.4
   - Use the RELEASE_NOTES_v2.0.4.md content

2. **Announce the Release:**
   - Update project README with new version
   - Notify users of the security update
   - Recommend immediate upgrade

3. **Verify in Package Managers:**
   - NPM: https://www.npmjs.com/package/openlearnx
   - Check latest version shows 2.0.4

## Package Details

```
Package Name: openlearnx
Version: 2.0.4
Description: AI-powered learning platform with adaptive quizzes, coding practice, course tracking, and dashboard analytics
Repository: https://github.com/th30d4y/OpenLearnX
Registry: https://registry.npmjs.org
```

## Installation Command for Users

```bash
# Install the latest version (2.0.4)
npm install openlearnx@2.0.4

# Or install the latest
npm install openlearnx@latest
```

---

**Security Note:** This version (2.0.4) contains critical security fixes for the JWT signature verification vulnerability (GHSA-223g-f5mq-gw33). All users should upgrade immediately.
