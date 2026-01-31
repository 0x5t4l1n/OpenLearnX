# OpenLearnX - Architecture Diagram

## System Architecture

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                           USER INTERFACE LAYER                       ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                                    │
            ┌───────────────────────┼───────────────────────┐
            │                       │                       │
    ┌───────▼───────┐      ┌───────▼───────┐      ┌───────▼───────┐
    │   Web Browser │      │ Mobile App    │      │  MetaMask     │
    │   (Next.js)   │      │  (Planned)    │      │   Wallet      │
    └───────┬───────┘      └───────┬───────┘      └───────┬───────┘
            │                      │                       │
            └──────────────────────┴───────────────────────┘
                                   │
                         HTTPS / WebSocket
                                   │
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━▼━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                        BACKEND API LAYER (Flask)                     ┃
┃                                                                       ┃
┃  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              ┃
┃  │ Auth Service │  │ Quiz Service │  │ Cert Service │              ┃
┃  │              │  │              │  │              │              ┃
┃  │ - JWT Auth   │  │ - MCQ        │  │ - NFT Mint  │              ┃
┃  │ - Wallet     │  │ - Adaptive   │  │ - IPFS      │              ┃
┃  │ - Nonce      │  │ - Grading    │  │ - Verify    │              ┃
┃  └──────────────┘  └──────────────┘  └──────────────┘              ┃
┃                                                                       ┃
┃  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              ┃
┃  │ Compiler Svc │  │ Dashboard Svc│  │ Adaptive AI  │              ┃
┃  │              │  │              │  │              │              ┃
┃  │ - Python     │  │ - Analytics  │  │ - IRT        │              ┃
┃  │ - JavaScript │  │ - Progress   │  │ - ML Models  │              ┃
┃  │ - C++/Java   │  │ - Competency │  │ - Question   │              ┃
┃  │ - Docker     │  │ - Reports    │  │   Selection  │              ┃
┃  └──────────────┘  └──────────────┘  └──────────────┘              ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┬━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         │                         │                         │
┏━━━━━━━━▼━━━━━━━━┓   ┏━━━━━━━━━━▼━━━━━━━━━┓   ┏━━━━━━━━━▼━━━━━━━┓
┃  Data Storage   ┃   ┃    Cache Layer     ┃   ┃  ML Services    ┃
┃                 ┃   ┃                    ┃   ┃                 ┃
┃  ┌───────────┐  ┃   ┃  ┌──────────────┐ ┃   ┃  ┌───────────┐  ┃
┃  │  MongoDB  │  ┃   ┃  │    Redis     │ ┃   ┃  │TensorFlow │  ┃
┃  │           │  ┃   ┃  │              │ ┃   ┃  │           │  ┃
┃  │ - Users   │  ┃   ┃  │ - Sessions   │ ┃   ┃  │ - Models  │  ┃
┃  │ - Courses │  ┃   ┃  │ - Cache      │ ┃   ┃  │ - Training│  ┃
┃  │ - Quizzes │  ┃   ┃  │ - Rate Limit │ ┃   ┃  │ - Predict │  ┃
┃  │ - Certs   │  ┃   ┃  └──────────────┘ ┃   ┃  └───────────┘  ┃
┃  └───────────┘  ┃   ┗━━━━━━━━━━━━━━━━━━━┛   ┗━━━━━━━━━━━━━━━━━┛
┗━━━━━━━━━━━━━━━━━┛
         │
┏━━━━━━━━▼━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                     BLOCKCHAIN LAYER (Ethereum)                      ┃
┃                                                                       ┃
┃  ┌────────────────────────────────────────────────────────────────┐ ┃
┃  │            CertificateNFT Smart Contract (Solidity)            │ ┃
┃  │                                                                │ ┃
┃  │  Functions:                      Data Structures:             │ ┃
┃  │  • mintCertificate()            • ERC-721 NFT                 │ ┃
┃  │  • mintCertificateWithDetails() • Certificate struct          │ ┃
┃  │  • getCertificate()             • userCertificates mapping    │ ┃
┃  │  • verifyCertificate()          • certificates mapping        │ ┃
┃  │  • getUserCertificates()                                      │ ┃
┃  └────────────────────────────────────────────────────────────────┘ ┃
┃                                                                       ┃
┃  Deployed on:                                                         ┃
┃  • Local: Anvil (Development)                                         ┃
┃  • Production: Ethereum Mainnet / L2 (Polygon, Arbitrum)              ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┬━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                                   │
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━▼━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃               DECENTRALIZED STORAGE LAYER (IPFS)                     ┃
┃                                                                       ┃
┃  Certificate Metadata:                                                ┃
┃  • Student name, subject, score                                       ┃
┃  • Issue date, institution                                            ┃
┃  • Certificate image/PDF                                              ┃
┃  • Immutable and permanent storage                                    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

## Component Interactions

### 1. Authentication Flow
```
User → MetaMask → Nonce Request → Backend
                      ↓
                Sign Nonce
                      ↓
Backend → Verify Signature → Issue JWT → User
```

### 2. Quiz Taking Flow
```
User → Start Quiz → Backend (Select Questions)
                         ↓
              Adaptive Algorithm (AI)
                         ↓
         Questions → User → Submit Answers
                         ↓
              Auto-Grade → Feedback
                         ↓
              Update Progress → Dashboard
```

### 3. Certificate Minting Flow
```
User Completes Quiz
       ↓
Backend Validates Score
       ↓
Generate Metadata
       ↓
Upload to IPFS
       ↓
Call Smart Contract
       ↓
Mint NFT on Blockchain
       ↓
Store Transaction Hash in MongoDB
       ↓
Certificate Available in User Wallet
```

### 4. Code Compilation Flow
```
User Writes Code → Frontend
                      ↓
               Backend Receives Code
                      ↓
            Create Docker Container
                      ↓
          Write Code, Compile, Execute
                      ↓
           Capture Output (with limits)
                      ↓
              Destroy Container
                      ↓
           Return Results → User
```

## Data Flow Diagram

```
┌─────────────┐
│    User     │
│  (Student/  │
│ Instructor) │
└──────┬──────┘
       │
       ├─── Authentication ──────────┐
       │                             │
       │                     ┌───────▼────────┐
       │                     │  JWT Token     │
       │                     │  Generation    │
       │                     └───────┬────────┘
       │                             │
       ├─── Take Quiz ───────────────┤
       │                             │
       │                     ┌───────▼────────┐
       │                     │  Question      │
       │                     │  Selection     │
       │                     │  (Adaptive AI) │
       │                     └───────┬────────┘
       │                             │
       ├─── Submit Answers ──────────┤
       │                             │
       │                     ┌───────▼────────┐
       │                     │  Grading       │
       │                     │  Engine        │
       │                     └───────┬────────┘
       │                             │
       ├─── View Results ────────────┤
       │                             │
       │                     ┌───────▼────────┐
       │                     │  Dashboard     │
       │                     │  Analytics     │
       │                     └───────┬────────┘
       │                             │
       └─── Request Certificate ─────┤
                                     │
                             ┌───────▼────────┐
                             │  Blockchain    │
                             │  NFT Minting   │
                             └───────┬────────┘
                                     │
                             ┌───────▼────────┐
                             │  IPFS Upload   │
                             └────────────────┘
```

## Technology Stack Map

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Stack                        │
├─────────────────────────────────────────────────────────────┤
│ • Next.js 14          → React Framework                     │
│ • TypeScript          → Type Safety                         │
│ • TailwindCSS         → Styling                            │
│ • shadcn/ui           → Component Library                   │
│ • ethers.js           → Blockchain Interaction              │
│ • Axios               → HTTP Client                         │
│ • React Hook Form     → Form Management                     │
│ • Chart.js            → Data Visualization                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                         Backend Stack                        │
├─────────────────────────────────────────────────────────────┤
│ • Flask 2.3           → Web Framework                       │
│ • Python 3.10+        → Programming Language                │
│ • TensorFlow 2.17     → Machine Learning                    │
│ • Motor/PyMongo       → MongoDB Driver                      │
│ • Flask-JWT-Extended  → Authentication                      │
│ • Web3.py             → Blockchain Interaction              │
│ • Docker              → Code Sandboxing                     │
│ • Redis               → Caching & Sessions                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                       Blockchain Stack                       │
├─────────────────────────────────────────────────────────────┤
│ • Solidity 0.8.19     → Smart Contract Language             │
│ • Foundry             → Development Toolkit                 │
│   - forge             → Testing & Building                  │
│   - anvil             → Local Ethereum Node                 │
│   - cast              → CLI Tools                           │
│ • OpenZeppelin        → Secure Contract Libraries           │
│ • IPFS                → Decentralized Storage               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                         Database Stack                       │
├─────────────────────────────────────────────────────────────┤
│ • MongoDB 6.0+        → Primary Database                    │
│ • Redis 7             → Cache & Sessions                    │
│ • PostgreSQL          → Future Relational Data (Planned)    │
└─────────────────────────────────────────────────────────────┘
```

## Security Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      Security Layers                          │
└──────────────────────────────────────────────────────────────┘

1. Authentication Layer
   ├── Wallet-based auth (MetaMask)
   ├── Cryptographic signatures
   ├── JWT tokens with expiration
   └── Nonce-based replay protection

2. Authorization Layer
   ├── Role-based access control (RBAC)
   ├── Resource ownership validation
   ├── JWT claims verification
   └── API route protection

3. Data Layer
   ├── AES encryption for sensitive data
   ├── HTTPS/TLS in production
   ├── Encrypted database connections
   └── Input sanitization

4. Execution Layer
   ├── Docker sandboxing
   ├── Resource limits (CPU, memory, time)
   ├── Network isolation
   └── Read-only file systems

5. Blockchain Layer
   ├── Smart contract access control
   ├── OpenZeppelin security standards
   ├── On-chain verification
   └── Immutable records

6. Application Layer
   ├── CORS configuration
   ├── Rate limiting
   ├── Error handling
   └── Audit logging
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Production Environment                    │
└─────────────────────────────────────────────────────────────┘

                    ┌──────────────┐
                    │  CloudFlare  │
                    │     CDN      │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  Load        │
                    │  Balancer    │
                    └──────┬───────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
  ┌─────▼─────┐     ┌─────▼─────┐     ┌─────▼─────┐
  │  App      │     │  App      │     │  App      │
  │  Server 1 │     │  Server 2 │     │  Server 3 │
  └─────┬─────┘     └─────┬─────┘     └─────┬─────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
  ┌─────▼─────┐     ┌─────▼─────┐     ┌─────▼─────┐
  │  MongoDB  │     │   Redis   │     │ Ethereum  │
  │  Cluster  │     │  Cluster  │     │    Node   │
  └───────────┘     └───────────┘     └───────────┘
```

---

For detailed implementation, see [DOCUMENTATION.md](./DOCUMENTATION.md)
