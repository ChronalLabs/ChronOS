# Contributing to RTI-Gen

Thank you for your interest in contributing to RTI-Gen! We are building a tool to empower citizens, and your help makes a difference.

## 🛠️ Development Setup

### Prerequisites
- Node.js v18+
- Java JDK 17+
- MongoDB (running locally or via Docker)

### 1. Fork & Clone
```bash
git clone https://github.com/YOUR_USERNAME/rti-gen.git
cd rti-gen
```

### 2. Backend Setup
```bash
cd backend
# Copy example env
cp .env.example .env
# Run
mvn spring-boot:run
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 🧪 Testing Guidelines
- **Frontend:** Run `npm test` (Jest). Ensure new components have Storybook stories.
- **Backend:** Run `mvn test`. We use Testcontainers for integration tests.
- **Accessibility:** All UI changes MUST pass WCAG AA contrast checks.

## 📝 Code Style
- **Java:** Follow Google Java Style Guide.
- **JS/TS:** ESLint + Prettier.

## ⚖️ License
By contributing, you agree that your contributions will be licensed under its MIT License.
