# System Architecture

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │   Home   │  │  Guided  │  │ Assisted │  │  DownloadPanel   │ │
│  │   Page   │  │   Mode   │  │   Mode   │  │  (PDF/DOCX/XLSX) │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘ │
│                              │                                   │
│                    ┌─────────▼─────────┐                        │
│                    │  Service Layer    │                        │
│                    │ (Axios API Calls) │                        │
│                    └─────────┬─────────┘                        │
└──────────────────────────────┼──────────────────────────────────┘
                               │ HTTP/REST
┌──────────────────────────────▼──────────────────────────────────┐
│                        BACKEND (FastAPI)                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                      API Layer                          │    │
│  │  /infer  │  /draft  │  /authority  │  /download         │    │
│  └─────────────────────────┬───────────────────────────────┘    │
│                            │                                    │
│  ┌─────────────────────────▼───────────────────────────────┐    │
│  │                   SERVICE LAYER                         │    │
│  │  ┌──────────────┐    ┌──────────────┐                   │    │
│  │  │ Rule Engine  │───▶│   NLP Layer  │                   │    │
│  │  │  (PRIMARY)   │    │  (SECONDARY) │                   │    │
│  │  └──────────────┘    └──────────────┘                   │    │
│  │         │                    │                          │    │
│  │         ▼                    ▼                          │    │
│  │  ┌──────────────────────────────────────────────────┐   │    │
│  │  │              Draft Assembler                     │   │    │
│  │  │         (Templates + Extracted Data)             │   │    │
│  │  └──────────────────────────────────────────────────┘   │    │
│  │                          │                              │    │
│  │                          ▼                              │    │
│  │  ┌──────────────────────────────────────────────────┐   │    │
│  │  │           Document Generator                     │   │    │
│  │  │         (PDF / DOCX / XLSX)                      │   │    │
│  │  └──────────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Decision Flow

```
User Input
    │
    ▼
┌───────────────┐
│  Rule Engine  │ ─────── Rules Match? ─── YES ──▶ Use Rule Result
│   (Primary)   │                │
└───────────────┘                │ NO
                                 ▼
                    ┌───────────────────────┐
                    │   NLP Analysis        │
                    │ (spaCy + DistilBERT)  │
                    └───────────────────────┘
                                 │
                                 ▼
                    ┌───────────────────────┐
                    │  Confidence > 70%?    │
                    └───────────────────────┘
                           │           │
                          YES          NO
                           │           │
                           ▼           ▼
                    Use NLP Result   Ask User to Confirm
```

## Key Principles

1. **Stateless Backend** - No database, no user data storage
2. **Rule-First** - AI only assists, never decides alone
3. **Privacy-First** - All processing happens per-request
4. **Transparent** - Users see confidence and can override
