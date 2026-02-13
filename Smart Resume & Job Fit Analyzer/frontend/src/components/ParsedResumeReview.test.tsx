
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import ParsedResumeReview from '../pages/ParsedResumeReview';
import type { ParsedResume } from '../services/types';
// React is imported via plugin

// Mock resume data with CORRECT structure
const mockResume: ParsedResume = {
    contact_info: {
        name: "Test User",
        email: "test@example.com",
        phone: "123-456-7890",
    },
    skills: [
        { name: "React", canonical_name: "React", category: "frameworks", confidence: "high", source_text: "React" },
        { name: "Redux", canonical_name: "Redux", category: "frameworks", confidence: "high", source_text: "Redux" },
        { name: "Python", canonical_name: "Python", category: "programming_languages", confidence: "high", source_text: "Python" }
    ],
    experience: [
        {
            title: "Developer",
            company: "Tech Corp",
            start_date: "2020",
            end_date: "Present",
            responsibilities: ["Coding"],
            description: "Coding stuff",
            source_text: "..."
        }
    ],
    education: [],
    projects: [],
    parsing_warnings: [],
    raw_text: ""
};

describe('ParsedResumeReview Editor', () => {
    it('renders the V1 split layout correctly', () => {
        render(
            <ParsedResumeReview
                resume={mockResume}
                sessionId="test-session"
                onContinue={vi.fn()}
            />
        );

        // Header check
        expect(screen.getByText(/Review how we interpreted your resume/i)).toBeInTheDocument();

        // "Run Analysis" button should be visible immediately
        expect(screen.getByRole('button', { name: /Run Analysis/i })).toBeInTheDocument();

        // Navigation Sidebar items
        expect(screen.getByText("Personal Info")).toBeInTheDocument();
        expect(screen.getByText("Experience")).toBeInTheDocument();
        expect(screen.getByText("Skills")).toBeInTheDocument();
    });

    it('navigates between sections', () => {
        render(
            <ParsedResumeReview
                resume={mockResume}
                sessionId="test-session"
                onContinue={vi.fn()}
            />
        );

        const experienceTab = screen.getByRole('button', { name: /Experience/i });
        fireEvent.click(experienceTab);
        expect(screen.getByRole('heading', { name: /Experience Details/i })).toBeInTheDocument();

        fireEvent.click(screen.getByRole('button', { name: /Skills/i }));
        expect(screen.getByRole('heading', { name: /Skills Details/i })).toBeInTheDocument();
        expect(screen.getByText("React")).toBeInTheDocument();
        expect(screen.getByText("Python")).toBeInTheDocument();
    });

    it('allows editing fields', () => {
        render(
            <ParsedResumeReview
                resume={mockResume}
                sessionId="test-session"
                onContinue={vi.fn()}
            />
        );

        fireEvent.click(screen.getByRole('button', { name: /Personal Info/i }));

        const nameInput = screen.getByDisplayValue("Test User");
        fireEvent.change(nameInput, { target: { value: "Updated Name" } });

        expect(screen.getByDisplayValue("Updated Name")).toBeInTheDocument();
        expect(screen.getByText(/Currently editing - changes will be applied on analysis/i)).toBeInTheDocument();
    });

    it('calls onContinue when Run Analysis is clicked', async () => {
        const handleContinue = vi.fn();
        render(
            <ParsedResumeReview
                resume={mockResume}
                sessionId="test-session"
                onContinue={handleContinue}
            />
        );

        const analyzeBtn = screen.getByRole('button', { name: /Run Analysis/i });
        fireEvent.click(analyzeBtn);

        expect(handleContinue).toHaveBeenCalled();
    });
});
