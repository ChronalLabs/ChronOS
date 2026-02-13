# AI-Powered Public Complaint & RTI Generator (Frontend)

The modern, responsive web interface for the AI-Powered Public Complaint & RTI Generator system. This frontend application empowers citizens to draft professional Right to Information (RTI) requests and public grievances with the assistance of AI.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![React](https://img.shields.io/badge/react-18.x-61dafb.svg)
![Status](https://img.shields.io/badge/status-development-orange.svg)

## 📋 Overview

This application provides a user-friendly interface for interacting with the AI drafting engine. It features two primary modes of operation designed to cater to different user needs:

*   **Guided Mode:** A step-by-step wizard for users who are new to filing complaints or RTIs. It simplifies the process into manageable questions.
*   **Assisted Mode:** A professional drafting environment for advanced users, offering live AI suggestions, real-time preview, and confidence scoring.

## ✨ Key Features

*   **Dual Workflow System:** Seamless switching between Guided and Assisted modes.
*   **Live Draft Preview:** Real-time visualization of the generated document.
*   **Smart Indicators:** Confidence score notices and AI-generated suggestions.
*   **Document Export:** Download drafts in PDF, DOCX, or TXT formats.
*   **Responsive Design:** Fully optimized for desktop and mobile devices.
*   **Submission Guidance:** Context-aware instructions for filing RTIs (Physical/Online) and Grievances (CPGRAMS).

## 🎨 UI/UX Design System

The interface follows a "Trust & Clarity" design philosophy, utilizing a high-contrast color palette to ensure accessibility and professionalism.

*   **Primary Color (Blue 01 - #0f62fe):** Used for primary actions, navigation, and active states. Represents trust and stability.
*   **Secondary Color (Green 05 - #24a148):** Used for success states, secondary actions, and validation. Represents progress and resolution.
*   **Typography:** Clean sans-serif fonts for maximum readability.

## 🛠️ Tech Stack

*   **Core:** React 18, React Router DOM v6
*   **State Management:** React Hooks (`useState`, `useEffect`)
*   **HTTP Client:** Axios
*   **Styling:** Native CSS with CSS Variables (Theming), Scoped CSS Modules
*   **Notifications:** React Toastify
*   **Icons:** FontAwesome / Lucide React

## 🚀 Getting Started

### Prerequisites

*   **Node.js** (v14 or higher)
*   **npm** (v6 or higher)
*   **Backend API:** Ensure the Python FastAPI backend is running on `http://localhost:8000`.

### Installation

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Configure Environment (Optional):**
    If your backend runs on a different port, create a `.env` file in the root of the `frontend` folder:
    ```env
    REACT_APP_API_URL=http://localhost:8000/api
    ```

### Running the Application

Start the development server:

```bash
npm start
```

The application will be available at [http://localhost:3000](http://localhost:3000).

## 📂 Project Structure

```text
src/
├── components/          # Reusable UI components
│   ├── ApplicantForm/   # Personal details input form
│   ├── DraftPreview/    # Live document editor/viewer
│   └── ...
├── layouts/             # Page layout wrappers (Header/Footer)
├── pages/               # Main application views
│   ├── Home/            # Landing page & mode selection
│   ├── GuidedMode/      # Step-by-step wizard logic
│   └── AssistedMode/    # Advanced editor logic
├── services/            # API service integration
│   ├── draftService.js  # Draft generation & export
│   └── ...
├── App.js               # Main Router configuration
└── index.css            # Global styles & Design Tokens
```

## 🤝 Contributing

1.  Fork the repository
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request
