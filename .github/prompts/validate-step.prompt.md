---
description: Validate that all success criteria for the current step are met
agent: code-reviewer
tools: [search, read, execute, web, todo]
---

# Validate Step

You will verify that all success criteria for the specified step have been met.

## User Input

**step-number** (REQUIRED): The step number to validate (e.g., "5-0", "5-1", "5-2")

If no step number is provided, ask the user for it.

## Instructions

Follow this systematic validation workflow:

### 1. Find the Exercise Issue

```bash
# Find the main exercise issue (has "Exercise:" in title)
gh issue list --state open | grep "Exercise:"
```

Extract the issue number from the results.

### 2. Retrieve Issue with Comments

```bash
# Get the full issue including all step comments
gh issue view <issue-number> --comments
```

### 3. Locate the Target Step

Search through the issue content for the exact step:

```
# Look for this pattern:
# Step {step-number}:
```

For example, if validating step "5-1", find:
```
# Step 5-1: <step title>
```

### 4. Extract Success Criteria

Within the step comment, locate the "Success Criteria" section. It typically looks like:

```markdown
## Success Criteria

- [ ] Backend DELETE endpoint implemented
- [ ] Delete button added to UI
- [ ] Confirmation dialog appears before deletion
- [ ] Task is removed from list after deletion
- [ ] All tests pass
```

Extract all criteria items from this section.

### 5. Check Each Criterion

For each criterion, verify against the current workspace state:

#### Code Implementation Checks
```bash
# Check if files exist
ls -la <file-path>

# Search for specific implementations
grep -r "pattern" <directory>

# Verify API endpoints
cat packages/backend/src/app.js | grep "DELETE"
```

#### Test Coverage Checks
```bash
# Verify test files exist
ls -la packages/backend/__tests__/
ls -la packages/frontend/src/__tests__/

# Search for specific test cases
grep -r "should delete task" packages/
```

#### Running Tests
```bash
# Run backend tests
npm test --workspace=backend

# Run frontend tests
npm test --workspace=frontend

# Run UI tests (if required)
npm run test:ui --workspace=frontend
```

#### Build and Lint Checks
```bash
# Check for compilation errors
npm run build

# Check for linting issues (informational, not blocking)
npm run lint
```

### 6. Report Validation Results

Provide a clear, structured report:

**Format**:

```
## Step {step-number} Validation

✅ PASSED: <criterion description>
✅ PASSED: <criterion description>
⚠️  PARTIAL: <criterion description>
   - <specific issue or gap>
❌ FAILED: <criterion description>
   - <specific issue or what's missing>

### Summary

Completed: X / Y criteria
Status: [READY | NEEDS WORK]

### Next Steps

[If READY]
All success criteria met! ✅
You can now:
- /commit-and-push <branch-name>

[If NEEDS WORK]
Address the following before moving on:
1. <specific action needed>
2. <specific action needed>
```

### 7. Provide Specific Guidance

For each failed or partial criterion, provide actionable guidance:

**Good**:
```
❌ FAILED: Delete button added to UI
   - File packages/frontend/src/App.js exists but does not contain delete button
   - Action: Add a delete button with onClick handler in TaskItem component
```

**Bad**:
```
❌ FAILED: Delete button
   - Missing
```

## Validation Categories

### Implementation Validation

Check for:
- Required files exist
- Expected functions/methods are defined
- API endpoints are implemented
- UI components render expected elements

### Test Coverage Validation

Check for:
- Test files exist for new functionality
- Test cases cover success and error paths
- All test suites pass
- No skipped or pending tests

### Quality Validation

Check for:
- No compilation errors (blocking)
- Linting issues (informational, not blocking for validation)
- Code follows project patterns
- Error handling is implemented

### Integration Validation

Check for:
- Backend and frontend integration works
- API responses match frontend expectations
- UI updates reflect backend state changes

## Edge Cases

### If Step Not Found

```
❌ Could not find Step {step-number} in the exercise issue.

Available steps in issue #{issue-number}:
- Step 5-0: Setup
- Step 5-1: Add delete endpoint
- Step 5-2: Add error handling

Please check the step number and try again.
```

### If Success Criteria Section Missing

```
⚠️  No "Success Criteria" section found for Step {step-number}.

Performing general validation:
- ✅ Code changes present
- ✅ Tests exist
- ✅ All tests passing

Manual review recommended for completeness.
```

### If Tests Fail

```
❌ FAILED: All tests pass
   
Test failures detected:
Backend: 2 tests failing
Frontend: All passing
UI: Not run

Failing tests:
- DELETE /tasks/:id should return 404 for non-existent task
- DELETE /tasks/:id should require authentication

Action: Fix failing tests before validation passes.
```

## Example Workflow

```
User: /validate-step 5-1

You:
1. [Runs: gh issue list --state open | grep "Exercise:"]
   Found: Issue #42 "Exercise: Build TODO App"

2. [Runs: gh issue view 42 --comments]
   [Parses content, finds Step 5-1]

3. [Extracts Success Criteria]:
   - Backend DELETE endpoint implemented
   - Delete button added to UI
   - Task removed from list after deletion
   - All tests pass

4. [Checks backend]:
   ✅ Found DELETE /tasks/:id in app.js
   ✅ Test file has DELETE endpoint tests

5. [Checks frontend]:
   ✅ Delete button present in App.js
   ✅ Test file has delete button tests

6. [Runs tests]:
   ✅ Backend tests: 15/15 passing
   ✅ Frontend tests: 8/8 passing
   ✅ UI tests: 5/5 passing

Response:
"## Step 5-1 Validation

✅ PASSED: Backend DELETE endpoint implemented
   - Endpoint defined at DELETE /tasks/:id
   - Returns 204 on success, 404 on not found
   
✅ PASSED: Delete button added to UI
   - Button present in TaskItem component
   - Click handler calls delete API
   
✅ PASSED: Task removed from list after deletion
   - UI updates after successful delete
   - Verified in UI tests
   
✅ PASSED: All tests pass
   - Backend: 15/15 passing
   - Frontend: 8/8 passing
   - UI: 5/5 passing

### Summary

Completed: 4 / 4 criteria
Status: READY ✅

All success criteria met! You can now commit and push:
- /commit-and-push feature/task-deletion"
```

## Success Indicators

You're succeeding when:
- ✅ You correctly locate the target step in the issue
- ✅ You extract all success criteria accurately
- ✅ You verify each criterion against workspace state
- ✅ You provide clear PASS/FAIL status with specifics
- ✅ You give actionable guidance for incomplete items
- ✅ Your report is concise and easy to understand

## Common Patterns

### Pattern: All Criteria Met

```
Status: READY ✅
All success criteria met!
Next: /commit-and-push <branch-name>
```

### Pattern: Some Criteria Incomplete

```
Status: NEEDS WORK ⚠️
Completed: 3 / 5 criteria

Actions needed:
1. Add error handling for network failures
2. Add UI test for delete confirmation dialog

After addressing these, run /validate-step {step-number} again.
```

### Pattern: Major Issues

```
Status: NEEDS WORK ❌
Completed: 1 / 5 criteria

Critical issues:
- DELETE endpoint not implemented
- Tests failing due to missing endpoint

Action: Complete the /execute-step activities before validation.
```

---

**Remember**: Systematic validation, clear reporting, actionable guidance.
