# Memory System Workflow Guide

This guide explains how to use the `.github/memory/` system during TDD and development workflows.

## 📁 Directory Structure

```
.github/memory/
├── README.md                    # System documentation
├── session-notes.md             # ✅ Committed - Historical session summaries
├── patterns-discovered.md       # ✅ Committed - Validated code patterns
├── workflow-notes.md            # ✅ This guide
└── scratch/
    ├── .gitignore              # Ignores everything in scratch/
    └── working-notes.md        # ❌ Not committed - Active session notes
```

## 📝 Three Memory Files

### 1. **session-notes.md** (Committed)
**What it is**: Historical record of completed work

**Contains**:
- What was accomplished in past sessions
- Key findings and decisions made
- Outcomes (test results, quality improvements)
- Next steps identified

**When to update**: At the **end** of each significant development session

### 2. **patterns-discovered.md** (Committed)  
**What it is**: Reusable solutions and conventions

**Contains**:
- Code patterns that solve specific problems
- Better approaches discovered through refactoring
- Conventions to follow consistently
- Examples with context

**When to update**: When you validate a pattern through successful testing

### 3. **scratch/working-notes.md** (NOT Committed)
**What it is**: Your active scratch space

**Contains**:
- Current task description
- Testing approach and hypothesis
- What you're trying and what results you're seeing
- Decisions made during implementation
- Blockers and questions
- Next immediate steps

**When to update**: **Continuously** during active development

---

## 🔄 Using Memory During TDD Workflows

### **Phase 1: Before Writing Tests**

1. **Review existing patterns**:
   - Open `patterns-discovered.md`
   - Look for relevant testing patterns, initialization patterns, etc.

2. **Check recent session notes**:
   - Review `session-notes.md`
   - See what was recently worked on and any notes about this area

3. **Start your working notes** in `scratch/working-notes.md`:
   ```markdown
   ## Current Task
   Implement task completion API endpoint
   
   ## Approach
   - Write failing test first (RED)
   - Implement minimal code to pass (GREEN)
   - Refactor while keeping tests green (REFACTOR)
   ```

### **Phase 2: RED - Write Failing Test**

**In `scratch/working-notes.md`**, document:
```markdown
## Key Findings
- Writing test for PUT /api/tasks/:id/complete
- Expecting 200 status and updated task object
- Test currently FAILS (as expected) - endpoint doesn't exist yet
```

### **Phase 3: GREEN - Make Test Pass**

**Continue in `scratch/working-notes.md`**:
```markdown
## Decisions Made
- Using Express route handler pattern from existing routes
- Updating task completion status in memory (no DB yet)
- Returning full task object with updated status

## Notes
- Ran: npm test -- app.test.js
- Test now PASSES ✅
```

### **Phase 4: REFACTOR - Improve Code**

**Track in `scratch/working-notes.md`**:
```markdown
## Key Findings
- Noticed duplicate validation logic across endpoints
- Extracted validateTaskId helper function
- All tests still passing after refactor ✅
```

### **Phase 5: Session End**

**1. Extract validated patterns** to `patterns-discovered.md`:
```markdown
### Express Route Validation Pattern

**Context**: When validating request parameters in Express routes

**Problem**: Duplicate validation logic across multiple endpoints

**Solution**: Extract validation to reusable helper functions

**Example**:
\`\`\`javascript
const validateTaskId = (req, res, next) => {
  if (!req.params.id) {
    return res.status(400).json({ error: 'Task ID required' });
  }
  next();
};

// Use in routes
app.put('/api/tasks/:id', validateTaskId, completeTask);
\`\`\`
```

**2. Summarize session** in `session-notes.md`:
```markdown
## Task Completion API - May 5, 2026

### What Was Accomplished
- Implemented PUT /api/tasks/:id/complete endpoint
- Followed TDD cycle: RED → GREEN → REFACTOR
- Extracted reusable validation helper

### Key Findings and Decisions
- **Pattern identified**: Validation logic was duplicating across routes
- **Decision**: Created validateTaskId helper for reusability
- **TDD success**: Test-first approach caught edge case with missing ID

### Outcomes
- All tests passing (12/12) ✅
- Code coverage increased to 95%
- Validation pattern ready for reuse on other endpoints

**Next Steps**: Apply validation pattern to remaining endpoints
```

---

## 💡 Quick Reference: Which File to Use When

| **During TDD** | **Use This** | **Action** |
|---|---|---|
| Before starting | `patterns-discovered.md` | Read - find relevant patterns |
| Writing tests | `scratch/working-notes.md` | Write - track your approach |
| RED phase | `scratch/working-notes.md` | Document expected failure |
| GREEN phase | `scratch/working-notes.md` | Record what made it pass |
| REFACTOR phase | `scratch/working-notes.md` | Note improvements made |
| Found new pattern | `patterns-discovered.md` | Add validated pattern |
| End of session | `session-notes.md` | Summarize outcomes |

---

## ✅ Benefits for TDD

1. **Continuity**: Resume TDD cycles exactly where you left off
2. **Pattern Library**: Build reusable test patterns over time
3. **Decision Trail**: Remember why you chose specific test approaches
4. **Failure Analysis**: Track which test strategies work in your codebase
5. **AI Context**: Copilot learns your testing patterns and suggests consistent code

---

## 🎯 Key Insight

**Working notes are your live scratch pad during TDD, while session notes and patterns are your knowledge base for future work.**

- **`scratch/working-notes.md`**: Active development, constantly updated, not committed
- **`patterns-discovered.md`**: Validated solutions, committed for reuse
- **`session-notes.md`**: Historical record, committed for continuity

---

## 📋 Example TDD Session Flow

```
1. Read patterns-discovered.md (learn from past)
   ↓
2. Open scratch/working-notes.md (start fresh)
   ↓
3. Write failing test → Document in working notes
   ↓
4. Implement code → Document approach in working notes
   ↓
5. Test passes → Note success in working notes
   ↓
6. Refactor → Track changes in working notes
   ↓
7. Session end:
   - Extract pattern → patterns-discovered.md
   - Summarize session → session-notes.md
   - Clear/reset → scratch/working-notes.md
```

---

## 🚀 Getting Started

**For your next TDD task**:

1. Open `scratch/working-notes.md`
2. Fill in "Current Task" and "Approach"
3. Start your RED-GREEN-REFACTOR cycle
4. Update working notes as you progress
5. At session end, distill insights into `patterns-discovered.md` and `session-notes.md`

The memory system works best when you use it consistently. Start with `scratch/working-notes.md` for every development session!
