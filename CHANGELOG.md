# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.4] - 2026-05-08

### Security
- **CRITICAL**: Fixed JWT signature verification vulnerability (GHSA-223g-f5mq-gw33)
  - Enabled proper JWT signature verification in `backend/routes/dashboard.py`
  - Enabled proper JWT signature verification in `backend/main.py`
  - Enabled proper JWT signature verification in `backend/activity_logger.py`
  - Replaced `verify_signature=False` with cryptographic verification using `JWT_SECRET_KEY`
  - Prevents JWT forgery attacks and unauthorized account takeover
  - CVE: Pending

### Changed
- JWT tokens are now verified with the server's secret key
- Forged tokens will be properly rejected with authentication errors

## [2.0.3] - 2026-04-15

### Added
- Initial release with adaptive quizzes
- AI-powered course recommendations
- Code compilation and practice features
- Dashboard analytics
- MetaMask wallet integration
- Certificate NFT generation

