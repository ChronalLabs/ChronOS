# RTI-Gen: Architecture & Data Flow Guide

This document explains **how the project works under the hood**, detailing the journey of a user's request from the moment they click "Generate" to the moment they receive a PDF.

---

## 🔄 High-Level Data Flow

1.  **User Input** (Frontend) → **JSON Payload**
2.  **API Request** (HTTP POST) → **Backend Controller**
3.  **Service Layer** (Business Logic) → **AI Adapter**
4.  **AI Processing** (Prompt Engineering) → **Draft Text**
5.  **PDF Generation** (Apache PDFBox) → **Binary File**
6.  **Response** → **User Download**

---

## 🛠️ Step-by-Step Technical Breakdown

### 1. Frontend Layer (React + Vite)
*   **File**: `src/services/api.js`
*   **Action**: When the user clicks "Generate RTI", the `generateDraft()` function is called.
*   **Process**:
    *   Collects data from the form (Applicant Name, Issue, Address).
    *   Checking **Language Preference** (English/Hindi).
    *   Constructs a JSON object.
    *   Sends a `POST` request to `http://localhost:8091/api/v1/generate`.
    *   *Note*: If the backend is unreachable, it falls back to a **Mock Generation** logic locally in `api.js`.

### 2. Controller Layer (Spring Boot Web)
*   **File**: `src/main/java/com/rtigen/controller/RtiController.java`
*   **Role**: The "Traffic Cop".
*   **Action**:
    *   The `@PostMapping("/generate")` endpoint receives the JSON.
    *   It automatically maps the JSON to the `DraftRequest` Java object (DTO).
    *   It calls `rtiService.generateDraft(request)`.

### 3. Service Layer (Business Logic)
*   **File**: `src/main/java/com/rtigen/service/RtiService.java`
*   **Role**: The "Brain".
*   **Action**:
    *   **Orchestration**: It decides *which* AI tool to use.
    *   **AI Call**: It calls `openAiAdapter.generateContent(request)`.
    *   **PDF Call**: Once the AI returns the text, it passes that text to `pdfExportService.createPdf()`.
    *   **Return**: It returns a `byte[]` (User-downloadable file) to the Controller.

### 4. Adapter Layer (AI Integration)
*   **File**: `src/main/java/com/rtigen/adapter/ai/OpenAiAdapter.java`
*   **Role**: The "Translator".
*   **Action**:
    *   **Prompt Engineering**: It constructs a massive, detailed prompt.
        *   *Example*: "You are a Legal Expert. Convert this complaint '${issue}' into Section 6(1) format..."
    *   **Strict Rules**: It enforces rules like "No Markdown", "Hindi Translation", and "Include Accepted Suggestions".
    *   **Validation**: It cleans the raw string response from the AI (removing backticks, ensuring clean JSON/Text).

### 5. PDF Generation Layer
*   **File**: `src/main/java/com/rtigen/service/PdfExportService.java`
*   **Role**: The "Printer".
*   **Action**:
    *   Uses **Apache PDFBox** library.
    *   Creates a virtual canvas.
    *   **Drawing**: It literally draws line-by-line:
        *   Draws "To, The PIO" at specific coordinates `(x: 50, y: 700)`.
        *   Draws the "Subject" line in **Bold**.
        *   Draws the main content body.
    *   **Hindi Font**: It loads a special Unicode font (`NotoSans`) to support Devanagari characters accurately.

---

## 🧩 Visual Dependency Graph

```mermaid
graph TD
    A[Frontend (Landing.jsx)] -->|Calls| B[api.js]
    B -->|POST /generate| C[RtiController.java]
    C -->|DraftRequest| D[RtiService.java]
    D -->|Get Text| E[OpenAiAdapter.java]
    E -->|Prompt| F[(OpenAI / Mock LLM)]
    F -->|Raw Response| E
    E -->|Clean Text| D
    D -->|Text Content| G[PdfExportService.java]
    G -->|PDF Bytes| C
    C -->|Blob| B
    B -->|Download| A
```

---

## 📝 Key Services Summary

| Service Name | Responsibility | Key Libraries |
| :--- | :--- | :--- |
| **RtiController** | REST API Endpoints | Spring Web |
| **RtiService** | Core Logic & Flow Control | Spring Context |
| **OpenAiAdapter** | AI Prompts & Cleaning | Spring RestTemplate |
| **PdfExportService** | PDF Layout & Font Rendering | Apache PDFBox |
| **ValidationUtils** | Input Checking (XSS/SQLi) | Jakarta Validation |

---
*Created for RTI-Gen Developer Documentation.*
