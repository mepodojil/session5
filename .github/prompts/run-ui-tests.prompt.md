---
description: Run UI tests and summarize failures
agent: test-engineer
tools: [read, execute, todo]
---

# Run UI Tests

You will execute the Playwright UI test suite and provide clear failure summaries with root cause classification.

## User Input

None required - this prompt runs the full UI test suite.

## CRITICAL PREREQUISITE: Playwright Installation

**REQUIRED FIRST STEP** (especially in Ubuntu/Linux environments):

```bash
# Install Playwright browsers with system dependencies
npm run test:ui:install --workspace=frontend
```

**When to run installation**:
- ✅ First time running UI tests in this container
- ✅ After container rebuild or recreation
- ✅ After Playwright version updates
- ✅ If you see errors like "Browser not found" or "chromium: not found"

**What `test:ui:install` does**:
1. Runs `playwright install --with-deps chromium`
2. Includes automatic bounded Ubuntu repo remediation for common Yarn GPG key issues
3. Performs one retry if the initial install fails
4. Reports clear blocker if install still fails after retry

**IMPORTANT**: Do NOT perform ad-hoc package hunting or broad OS troubleshooting beyond the automated remediation. If install fails after the automated retry, stop immediately and report an environment blocker.

**Do not continue to run Playwright tests after a failed dependency install.**

## Instructions

Follow this systematic test execution workflow:

### 1. Verify Installation (First Run)

Check if browsers are installed:

```bash
# Check Playwright installation status
npx playwright --version

# If browsers not found, install them
npm run test:ui:install --workspace=frontend
```

### 2. Ensure Backend and Frontend Are Running

UI tests require both services to be running:

```bash
# From repository root
npm start

# This should start both:
# - Backend on http://localhost:5000
# - Frontend on http://localhost:3000
```

**Verify services are running**:
```bash
# Check backend
curl http://localhost:5000/api/tasks

# Check frontend
curl http://localhost:3000
```

If services are not running, start them before proceeding.

### 3. Run UI Test Suite

```bash
# Run all Playwright tests
cd packages/frontend
npx playwright test

# Alternative: Run with more visibility
npx playwright test --reporter=list

# For debugging: Run headed (see browser)
npx playwright test --headed
```

### 4. Capture Test Results

Collect key information:
- Total tests run
- Tests passed
- Tests failed
- Test skipped
- Total duration
- Failed test details (name, file, error)

### 5. Summarize Results Clearly

Provide a structured summary:

```
## UI Test Results

✅ PASSED: X tests
❌ FAILED: Y tests
⏭️  SKIPPED: Z tests

Duration: MM:SS

[If all passed]
All UI tests passing! ✅

[If failures]
Failures:
1. Test: "should delete task"
   File: task-management.spec.js:42
   Error: Timeout waiting for selector "button[name='Delete']"

2. Test: "should show error for empty title"
   File: task-management.spec.js:58
   Error: Expected error message to be visible
```

### 6. Classify Failures by Root Cause

For each failed test, determine the likely root cause:

#### 🐛 Application Defect
**Indicators**:
- Feature doesn't work as expected
- API returns wrong status/data
- UI element behaves incorrectly
- Business logic error

**Example**:
```
🐛 Application Defect
Test: "should delete task"
Issue: Delete button click doesn't remove task from list
Likely cause: API endpoint not implemented or not updating state
Action: Verify DELETE /tasks/:id endpoint and state management
```

#### 🧪 Test Defect
**Indicators**:
- Selector doesn't match actual DOM
- Test logic is incorrect
- Assertions expect wrong values
- Test setup is incomplete

**Example**:
```
🧪 Test Defect
Test: "should delete task"
Issue: Timeout waiting for selector "button[name='Delete']"
Likely cause: Selector is outdated or incorrect
Action: Inspect DOM and update selector to match actual button
```

#### 🌍 Environment Issue
**Indicators**:
- Timing issues (intermittent failures)
- Network timeouts
- Missing dependencies
- Port conflicts
- Service not running

**Example**:
```
🌍 Environment Issue
Test: "should create task"
Issue: Network request timeout to http://localhost:5000/api/tasks
Likely cause: Backend service not running or port conflict
Action: Ensure backend is running: npm start
```

### 7. Generate Detailed Failure Report

For each failure category:

```
## Failure Analysis

### Application Defects (2 failures)

1. Delete functionality broken
   - Test: task-management.spec.js - "should delete task"
   - Expected: Task removed from list
   - Actual: Task remains in list after delete
   - Root cause: DELETE endpoint returns 200 but doesn't update database
   - Action: Fix backend DELETE handler in app.js

2. Error validation missing
   - Test: task-management.spec.js - "should reject empty title"
   - Expected: Error message displayed
   - Actual: Task created with empty title
   - Root cause: Frontend validation not implemented
   - Action: Add validation in task creation handler

### Test Defects (1 failure)

1. Outdated selector
   - Test: task-management.spec.js - "should toggle completion"
   - Expected: Find checkbox by selector
   - Actual: Selector returns no matches
   - Root cause: Checkbox selector changed from class to role
   - Action: Update selector to getByRole('checkbox')

### Environment Issues (0 failures)

No environment issues detected.
```

### 8. Provide Actionable Next Steps

Based on failure analysis:

```
## Recommended Actions

Priority: Fix application defects first, then test defects

1. Fix DELETE endpoint (app defect)
   - File: packages/backend/src/app.js
   - Issue: DELETE /tasks/:id doesn't update database
   - Handoff: Use /execute-step or tdd-developer agent

2. Add frontend validation (app defect)
   - File: packages/frontend/src/App.js
   - Issue: Empty title validation missing
   - Handoff: Use /execute-step or tdd-developer agent

3. Update checkbox selector (test defect)
   - File: packages/frontend/tests/ui/task-management.spec.js
   - Issue: Selector needs update to use accessibility role
   - Action: In test file, change to getByRole('checkbox')

After fixes:
- Rerun: /run-ui-tests
- Validate: /validate-step <step-number>
- Commit: /commit-and-push <branch-name>
```

## Debugging Tools

### Playwright Trace Viewer

For persistent failures:

```bash
# Run with trace on
npx playwright test --trace on

# View trace for debugging
npx playwright show-trace trace.zip
```

Trace includes:
- Step-by-step test execution
- Screenshots at each step
- Network requests
- Console logs
- DOM snapshots

### UI Mode (Interactive Debugging)

```bash
# Run tests in UI mode
npx playwright test --ui

# Features:
# - Watch tests execute in real-time
# - Pause and inspect at any step
# - Time-travel through test execution
# - See network activity
```

### Screenshots on Failure

Playwright automatically captures screenshots on failure:

```bash
# Screenshots saved to:
packages/frontend/test-results/
```

Reference screenshots in failure reports.

## Common Failure Patterns

### Pattern: Selector Not Found

```
❌ TimeoutError: Waiting for selector "button.delete" failed

Classification: 🧪 Test Defect (likely)
Diagnosis:
1. Check if element exists in DOM
2. Verify selector syntax matches actual element
3. Consider timing - element may appear late

Fix: Update selector or add proper wait
```

### Pattern: Assertion Failure

```
❌ Expected taskCount to be 1, received 0

Classification: 🐛 Application Defect (likely)
Diagnosis:
1. Task creation API may be failing
2. State update may not be triggering
3. UI may not be subscribing to state changes

Fix: Debug task creation flow, check API and state management
```

### Pattern: Network Timeout

```
❌ Request to http://localhost:5000/api/tasks timed out

Classification: 🌍 Environment Issue (likely)
Diagnosis:
1. Backend service may not be running
2. Port may be blocked or conflicting
3. Network connectivity issue

Fix: Ensure backend is running: npm start
```

### Pattern: Intermittent Failure

```
❌ Test passes sometimes, fails others

Classification: 🌍 Environment Issue (likely)
Diagnosis:
1. Race condition - test doesn't wait for async operation
2. Timing-dependent logic
3. Shared state between tests

Fix: Add proper state-based waits, ensure test isolation
```

## Success Indicators

You're succeeding when:
- ✅ Test results are summarized clearly
- ✅ Failures are classified into one of three categories
- ✅ Root causes are explained with context
- ✅ Actionable next steps are provided
- ✅ You distinguish between app bugs, test bugs, and environment issues
- ✅ You recommend appropriate handoffs (tdd-developer for app fixes)

## Example Workflow

```
User: /run-ui-tests

You:
1. [Checks: Playwright installed]
   ✅ Playwright v1.40.0 installed

2. [Verifies: Services running]
   ✅ Backend running on http://localhost:5000
   ✅ Frontend running on http://localhost:3000

3. [Runs: npx playwright test]
   
   Running 5 tests...
   ✅ should create task (1.2s)
   ✅ should toggle completion (0.9s)
   ❌ should delete task (30.0s)
   ❌ should show error for empty title (2.3s)
   ✅ should handle network error (1.5s)

4. [Analyzes failures]
   
5. [Generates report]

Response:
"## UI Test Results

✅ PASSED: 3 tests
❌ FAILED: 2 tests

Duration: 36.9s

Failures:
1. task-management.spec.js - "should delete task"
2. task-management.spec.js - "should show error for empty title"

## Failure Analysis

### Application Defects (2 failures)

1. 🐛 Delete functionality not working
   Test: "should delete task"
   Issue: Task remains in list after delete button click
   Root cause: DELETE endpoint likely not implemented or state not updating
   Action: Implement DELETE /tasks/:id endpoint (use tdd-developer)

2. 🐛 Input validation missing
   Test: "should show error for empty title"
   Issue: Error message doesn't appear for empty input
   Root cause: Frontend validation not implemented
   Action: Add validation for empty title (use tdd-developer)

## Recommended Actions

Both failures are APPLICATION DEFECTS requiring code fixes:

1. Implement DELETE endpoint
   - Handoff: /execute-step or use tdd-developer agent
   - Location: packages/backend/src/app.js

2. Add frontend validation
   - Handoff: /execute-step or use tdd-developer agent  
   - Location: packages/frontend/src/App.js

After fixes:
- Rerun: /run-ui-tests
- Validate: /validate-step <step-number>
- Commit: /commit-and-push <branch-name>"
```

---

**Remember**: Install first, run systematically, classify accurately, guide clearly.
