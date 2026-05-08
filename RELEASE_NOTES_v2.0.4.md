# Release v2.0.4 - Security Patch

**Release Date:** May 8, 2026

## 🔒 Security Update

### Fixed
- **CRITICAL**: JWT Signature Verification Vulnerability (GHSA-223g-f5mq-gw33)
  - Fixed JWT signature verification that was disabled in authentication middleware
  - Prevents JWT forgery attacks and unauthorized account takeover
  - All JWT tokens now properly verified with server secret key

### What Was Fixed
The application was disabling JWT signature verification with `options={"verify_signature": False}`, which allowed attackers to forge authentication tokens without the server checking the signature.

**Files Updated:**
- `backend/routes/dashboard.py` - Enabled JWT signature verification
- `backend/main.py` - Enabled JWT signature verification
- `backend/activity_logger.py` - Enabled JWT signature verification

**Changes:**
```python
# Before (Vulnerable)
decoded = jwt.decode(token, options={"verify_signature": False}, ...)

# After (Fixed)
decoded = jwt.decode(token, jwt_secret_key, algorithms=["HS256", "RS256"])
```

### Security Impact
- ✅ Tokens without valid signatures are now properly rejected
- ✅ Attackers can no longer forge authentication tokens
- ✅ Account takeover vulnerability is closed
- ✅ Server validates token authenticity using cryptographic signature

## 📦 Installation

### NPM
```bash
npm install @th30d4y/openlearnx@2.0.4
```

### Yarn
```bash
yarn add @th30d4y/openlearnx@2.0.4
```

### PNPM
```bash
pnpm add @th30d4y/openlearnx@2.0.4
```

## 📝 Changelog

- Updated package version to 2.0.4
- Created CHANGELOG.md with version history
- Security patch for JWT vulnerability (GHSA-223g-f5mq-gw33)

## 🔗 References

- **Security Advisory:** GHSA-223g-f5mq-gw33
- **CWE:** CWE-287 (Improper Authentication), CWE-347 (Improper Verification of Cryptographic Signature)
- **Severity:** Moderate (High impact, limited exposure in development configurations)

## 👥 Credits

- **Reporter:** @krrazee
- **Remediation Developer:** @0x5t4l1n

## ⚠️ Important Notes

- This is a security release and should be deployed immediately
- The JWT_SECRET_KEY environment variable must be set (already handled in app configuration)
- Previous versions (2.0.3 and earlier) are affected and should be updated

## 🚀 Next Steps

1. Install the latest version: `npm install @th30d4y/openlearnx@2.0.4`
2. Deploy to your environment
3. Verify JWT authentication is working correctly
4. Monitor for any authentication-related issues

---

For more information, visit: https://github.com/th30d4y/OpenLearnX
