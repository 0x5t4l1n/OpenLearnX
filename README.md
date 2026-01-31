# OpenLearnX

**OpenLearnX** is a cutting-edge decentralized learning and assessment platform that revolutionizes education through adaptive testing, instant feedback, and blockchain-based certification.

The platform provides learners with a smarter, personalized, and verifiable way to build and prove skills — from code challenges to real-world learning paths, all backed by blockchain technology.

> 📚 **Documentation**: [DOCS_INDEX.md](./DOCS_INDEX.md) | [DOCUMENTATION.md](./DOCUMENTATION.md) | [QUICK_START.md](./QUICK_START.md)

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




