# RTI-Gen: AI-Powered Right to Information (RTI) Generator
> *Bridging the gap between citizen intent and legal action.*

![Status](https://img.shields.io/badge/Status-Active_Development-success)
![Stack](https://img.shields.io/badge/Stack-Spring_Boot_%7C_React-blue)
![License](https://img.shields.io/badge/License-MIT-green)

**RTI-Gen** is a civic-tech platform designed to empower Indian citizens to exercise their **Right to Information (RTI) Act, 2005**. By leveraging Large Language Models (LLMs), it transforms simple, plain-language queries (e.g., *"My road is broken"*) into legally compliant, Section 6(1) formatted RTI applications ready for submission.

---

## 🌟 Key Features

### 🤖 AI Drafting Engine
- **Smart Expansion**: Converts vague complaints into technical, fact-based questions.
- **Legal Compliance**: Automatically formats drafts effectively invoking Section 6(1) of the RTI Act.
- **Modes**: 
  - **AI Mode**: Generates questions from scratch based on a topic.
  - **Assisted Mode**: Polishes user-provided questions for grammar and tone.

### 🇮🇳 First-Class Hindi Support
- **Full Localization**: The entire drafting interface works in Hindi.
- **Transliteration**: Automatically converts English names and addresses to Hindi (Devanagari) to ensure the application is accepted by local PIOs.
- **Dual-Output**: Generates drafts in both English and Hindi.

### 📄 Professional Export
- **PDF Generation**: Uses `Apache PDFBox` to generate print-ready PDFs with proper margins and headers.
- **Strict Formatting**: Ensures the "To, The Public Information Officer" block is always correctly placed.

---

## 🛠️ Technology Stack

### Backend (The Core)
- **Framework**: Java Spring Boot 3.2.2
- **Language**: Java 17
- **AI Integration**: OpenAI API (GPT-3.5/4) + Custom Prompt Engineering
- **PDF Engine**: Apache PDFBox
- **Build Tool**: Maven

### Frontend (The Interface)
- **Framework**: React.js (Vite)
- **Styling**: TailwindCSS v4
- **Animations**: Framer Motion (for smooth, 3D interactions)
- **State Management**: React Context

---

## 🚀 Getting Started

Follow these instructions to run the project locally.

### Prerequisites
- **Java JDK 17** or higher
- **Node.js v18** or higher
- **Maven**
- **Git**

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/rti-gen.git
    cd rti-gen
    ```

2.  **Backend Setup**
    Navigate to the backend folder and run the Spring Boot application.
    ```bash
    cd backend
    mvn spring-boot:run
    # The server will start on Port 8091 (http://localhost:8091)
    ```
    *Note: If you encounter port conflicts, the app is configured to fail gracefully or you can override via `server.port=8092`.*

3.  **Frontend Setup**
    Open a new terminal, navigate to the frontend folder, and start the dev server.
    ```bash
    cd frontend
    npm install
    npm run dev
    # Access the app at http://localhost:5173
    ```

---

## 📖 Usage Guide

1.  **Landing Page**: Browse features and understand the 3-step process.
2.  **Generate Draft**: Click "Generate RTI".
3.  **Input Details**:
    - Select **Language** (English/Hindi).
    - Enter **Applicant Details** (Name, Address).
    - Describe the **Issue** (e.g., "Scholarship money not received").
4.  **Review**: The AI will generate a draft. You can edit questions or add new ones.
5.  **Download**: Click "Download PDF" to get the final file.

---

## 🤝 Contribution API
We welcome contributions! Please see our `CONTRIBUTORS_INDEX` on the [Community Page](/community) or check `gsoc_documentation.md` for project ideas.

**Strict Contribution Rules:**
- **No Analytics**: We do not track users. Do not add Google Analytics.
- **Civic Aesthetic**: UI must remain clean, professional, and free of "marketing" fluff.
- **Attribution**: The footer credit is strictly fixed.

---

## 📜 License
This project is open-sourced under the MIT License.

---
*Built for public infrastructure. Made by Yogesh Sanodiya.*
