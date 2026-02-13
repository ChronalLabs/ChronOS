# Frontend-Backend Integration Testing Checklist

## Prerequisites
✅ Backend running: http://localhost:8000
✅ Frontend running: http://localhost:5173

## Manual Testing Steps

### Step 1: Landing Page
1. Open http://localhost:5173 in your browser
2. **Verify**: Page loads without errors
3. **Verify**: "Get Started" or mode selection is visible

### Step 2: Mode Selection
1. Click "Get Started" or select "Job Fit Analysis" mode
2. **Verify**: Navigates to input page

### Step 3: Resume Upload
1. Drag and drop a PDF/DOCX resume OR click to upload
2. **Verify**: File name appears after upload
3. **Verify**: No console errors (F12 > Console)
4. **Verify**: Loading indicator shows during processing

### Step 4: Review Parsed Resume
1. After upload, should navigate to "Review" step
2. **Check these sections**:
   - [ ] Personal Info - Name, email, phone displayed
   - [ ] Skills - List of extracted skills with count (e.g., "11 skills")
   - [ ] Experience - Work history entries with company, title, dates
   - [ ] Education - Degree, institution, dates
   - [ ] Projects - If present in resume

### Step 5: Job Description Input
1. Paste a job description (minimum 50 characters)
2. **Verify**: Character count updates
3. **Verify**: "Analyze" button enables when valid

### Step 6: Analysis Results
1. Click "Run Analysis" or "Analyze Match"
2. **Verify**: Loading/progress animation
3. **Verify**: Results dashboard shows:
   - [ ] Job Fit Score (0-100)
   - [ ] Extraction Insight panel (Skills/Exp/Edu counts)
   - [ ] Gap Analysis (Matched/Partial/Missing skills)
   - [ ] Action Plan suggestions

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| "0 Experience" | Section headers not detected | Check resume formatting |
| "0 Skills" | Skills not in our taxonomy | Add skills to skill list |
| 500 Error | Backend crash | Check terminal for errors |
| Button disabled | Validation failed | Check min 50 chars for JD |

## Quick API Health Check
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy","service":"smart-resume-analyzer"}
```
