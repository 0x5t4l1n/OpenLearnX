# OpenLearnX

**OpenLearnX** is a cutting-edge decentralized learning and assessment platform that revolutionizes education through adaptive testing, instant feedback, and blockchain-based certification.

The platform provides learners with a smarter, personalized, and verifiable way to build and prove skills — from code challenges to real-world learning paths, all backed by blockchain technology.

> 📚 **For detailed documentation, see [DOCUMENTATION.md](./DOCUMENTATION.md)**

---

## ✨ What Makes It Different?

- **🎯 Adaptive Learning:** Challenges that scale dynamically with your skill level using advanced algorithms
- **⚡ Instant Feedback:** Get results and detailed explanations in real-time
- **🔐 Blockchain Certificates:** Earn tamper-proof NFT certificates as verifiable proof of learning
- **📊 Skill Dashboard:** Track progress over time with comprehensive analytics and competency mapping
- **🌐 Decentralized Storage:** Own your data with IPFS-powered decentralized storage
- **💻 Multi-Language Compiler:** Execute code in 8+ programming languages with secure sandboxing
- **🤖 AI-Powered Quizzes:** Intelligent question generation and adaptive difficulty adjustment
- **👥 Peer Review System:** Collaborative learning with bias detection

---

## 📌 Use Cases

- **Coding Bootcamps:** Verify student progress with blockchain certificates
- **Professional Certification:** Issue tamper-proof credentials for completed courses
- **Corporate Training:** Track employee skill development with transparent analytics
- **Academic Assessments:** Adaptive testing that accurately measures student ability
- **Portfolio Building:** Showcase verified skills to potential employers
- **Skill Verification:** Employers can instantly verify candidate credentials on blockchain

---

## 🏗 Architecture Overview

```
Frontend (Next.js + React) → Backend (Flask + Python) → MongoDB Database
                          ↓
                    Web3 Layer (Ethereum)
                          ↓
              Smart Contracts (Solidity) → IPFS Storage
```

**Key Components:**
- **Frontend**: Next.js 14, TypeScript, TailwindCSS, MetaMask integration
- **Backend**: Flask, TensorFlow, Web3.py, JWT authentication
- **Blockchain**: Solidity smart contracts, ERC-721 NFTs, Foundry toolkit
- **Database**: MongoDB, Redis cache
- **Storage**: IPFS for decentralized metadata

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.10+
- MongoDB 6.0+
- Docker (optional)
- MetaMask browser extension

### Installation

1. **Install Foundry** (Blockchain toolkit):
```bash
curl -L https://foundry.paradigm.xyz | bash
foundryup
```

2. **Clone the repository**:
```bash
git clone https://github.com/th30d4y/OpenLearnX.git
cd OpenLearnX
```

3. **Start local blockchain** (Terminal 1):
```bash
anvil --fork-url https://eth.merkle.io
```

4. **Setup and start backend** (Terminal 2):
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Deploy smart contract
python3 scripts/deploy.py

# Start backend server
python3 main.py
```

5. **Setup and start frontend** (Terminal 3):
```bash
cd frontend
pnpm install
pnpm run dev
```

6. **Access the application**:
   - Open http://localhost:3000
   - Connect MetaMask wallet
   - Start learning!

> 📖 **For detailed setup instructions, see [DOCUMENTATION.md](./DOCUMENTATION.md#setup--installation)**

---

## 🌱 Project Status

**Current Version**: Alpha 1.0.0  
**Status**: 🟢 Active Development

This is an open-source project under active development. Core features are functional, with continuous improvements being made.

### Recent Updates
- ✅ NFT certificate minting system
- ✅ Adaptive quiz algorithm
- ✅ Multi-language code compiler
- ✅ Comprehensive dashboard analytics
- ✅ Wallet-based authentication

### Roadmap
- 🔄 AI question generation refinement
- 🔄 Peer review system enhancements
- 📅 Mobile app (React Native)
- 📅 Live proctoring for exams
- 📅 Marketplace for courses

---

## 🧪 Built With

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **TailwindCSS** - Styling
- **shadcn/ui** - Component library
- **ethers.js** - Ethereum interaction
- **MetaMask SDK** - Wallet integration

### Backend
- **Flask** - Python web framework
- **TensorFlow** - Machine learning
- **MongoDB** - Database
- **Redis** - Caching
- **Web3.py** - Blockchain interaction
- **Flask-JWT-Extended** - Authentication

### Blockchain
- **Solidity 0.8.19** - Smart contracts
- **Foundry** - Development toolkit
- **OpenZeppelin** - Secure contract libraries
- **IPFS** - Decentralized storage
- **Anvil** - Local Ethereum node

---

## 📊 Key Features

### For Students
- 🎓 Personalized adaptive learning paths
- 💯 Instant feedback on assessments
- 🏆 Blockchain-verified certificates (NFTs)
- 📈 Progress tracking and analytics
- 💻 Interactive coding challenges
- 🌟 Skill competency mapping

### For Instructors
- 📚 Course creation and management
- 👥 Student progress monitoring
- 📊 Comprehensive analytics dashboard
- ✍️ Quiz and assessment authoring
- 🔍 Bias detection in grading
- 📝 Automated and manual grading

### For Employers
- ✅ Instant credential verification
- 🔗 Blockchain-backed authenticity
- 📋 Detailed skill assessments
- 🎯 Candidate skill mapping
- 🔍 Transparent learning history

---

## 📚 Documentation

Comprehensive documentation is available in [DOCUMENTATION.md](./DOCUMENTATION.md), including:

- 📖 Detailed architecture explanation
- 🔧 Technology stack deep dive
- 📁 Project structure overview
- 📜 Smart contract documentation
- 🖥️ Backend services guide
- 🎨 Frontend components reference
- 💾 Database schema
- 🔌 API documentation
- ⚙️ Advanced configuration
- 🚀 Production deployment guide
- 🔒 Security best practices

---

## 🤝 Contributing

We welcome contributions from the community! Whether it's:

- 🐛 Bug reports and fixes
- ✨ New features
- 📚 Documentation improvements
- 🌐 Translations
- 🎨 UI/UX enhancements
- 🧪 Test coverage

**How to contribute:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read [DOCUMENTATION.md](./DOCUMENTATION.md#contributing) for detailed contribution guidelines.

---

## 📄 License

[Include your license here - e.g., MIT License]

---

## 🙏 Acknowledgments

- **OpenZeppelin** - Secure smart contract libraries
- **Foundry** - Ethereum development toolkit
- **Next.js Team** - Amazing React framework
- **TensorFlow** - Machine learning framework
- **All Contributors** - Thank you for making OpenLearnX better!

---

## 📞 Contact & Support

- 🌐 Website: [your-website.com]
- 💬 Discord: [your-discord-link]
- 🐦 Twitter: [@OpenLearnX]
- 📧 Email: [your-email]
- 📖 Docs: [DOCUMENTATION.md](./DOCUMENTATION.md)

---

## ⭐ Show Your Support

If you find OpenLearnX useful, please consider:
- ⭐ Starring this repository
- 🔄 Sharing with others
- 🐛 Reporting bugs
- ✨ Contributing code
- 💬 Joining our community

**Together, let's revolutionize education! 🚀**

---


