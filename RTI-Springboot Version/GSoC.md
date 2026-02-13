# Google Summer of Code (GSoC) 2026 - RTI-Gen

## 🚀 Project Overview
**RTI-Gen** is an AI-powered civic tech platform that empowers citizens to file high-quality Right to Information (RTI) applications. By bridging the gap between plain language intent and legal drafting, we aim to increase government transparency and accountability.

**Mentors:**
- [Your Name] (Maintainer)

**Tech Stack:** 
- React 19 + Vite + Tailwind CSS v4
- Spring Boot 3 + MongoDB + Redis
- AI Adapters (OpenAI / Local LLM)

## 🎯 Project Ideas & Tasks

### 1. Multi-Language Support (Priority: High)
- **Goal:** Implement full localization (English <-> Hindi <-> Regional).
- **Description:** Implement the `TranslationService` in the backend and UI toggles. Ensure generated PDFs respect unicode fonts.
- **Difficulty:** Medium
- **Skills:** Java, React, i18n

### 2. Appeal Generation Module (Priority: Medium)
- **Goal:** Allow users to generate First Appeals for rejected RTIs.
- **Description:** Create a flow where users input the rejection reason, and the system drafts a legal appeal.
- **Difficulty:** Medium
- **Skills:** AI Prompts, PDFBox

### 3. Voice-to-RTI (Priority: Hard)
- **Goal:** Allow users to speak their grievance.
- **Description:** Integrate browser Speech-to-Text APIS or OpenAI Whisper to fill the intent box.
- **Difficulty:** Hard
- **Skills:** Audio Processing, React

## 📅 Roadmap / Milestones
- **Phase 1 (Current):** Core Generator, Templates, Dashboard (Completed).
- **Phase 2 (GSoC):** Localization, Appeals, Advanced Analytics.
- **Phase 3:** Mobile App (React Native).

## 🤝 How to Contribute
See [CONTRIBUTING.md](./CONTRIBUTING.md) for setup instructions. We look for quality code, tests, and empathy for the user.
