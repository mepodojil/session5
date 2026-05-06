---
description: Execute instructions from the current GitHub Issue step
agent: tdd-developer
tools: [search, read, edit, execute, web, todo]
---

# Execute Step

You will execute the instructions from the current step in the GitHub Issue exercise.

## User Input

**issue-number** (optional): The GitHub issue number. If not provided, you will discover it automatically.

## Instructions

Follow these steps systematically:

### 1. Find the Exercise Issue

If the issue number was not provided:
```bash
# Find the main exercise issue (has "Exercise:" in title)
gh issue list --state open | grep "Exercise:"
```

Extract the issue number from the results.

### 2. Retrieve Issue Content

```bash
# Get the full issue including all step comments
gh issue view <issue-number> --comments
```

### 3. Parse the Current Step Instructions

- Identify the active step being worked on (usually the most recent step comment)
- Extract all `:keyboard: Activity:` sections from that step
- Note any success criteria or validation requirements

### 4. Execute Activities Systematically

For each `:keyboard: Activity:` section:

1. **Read the activity instructions carefully**
2. **Plan your approach** before implementing
3. **Execute the activity** following TDD principles:
   - Write tests FIRST for new features (RED phase)
   - Implement minimal code to pass tests (GREEN phase)
   - Refactor while keeping tests green (REFACTOR phase)
4. **Verify the change** by running relevant tests

**CRITICAL SCOPE BOUNDARIES:**

- ✅ **You SHOULD**: Implement backend functionality, add frontend components, write unit tests (Jest, React Testing Library)
- ❌ **You SHOULD NOT**: Create Playwright UI tests or run end-to-end test suites
- 🔄 **Handoff Rule**: When Playwright UI tests are needed, stop and recommend:
  - `/create-ui-tests` to create UI tests (auto-switches to `test-engineer`)
  - `/run-ui-tests` to execute UI test suite (auto-switches to `test-engineer`)

### 5. DO NOT Commit or Push

**Your responsibility ends at implementation and unit testing.**

The `/commit-and-push` prompt handles all Git operations (staging, committing, pushing).

### 6. Provide Next Actions

After completing all activities, guide the user with the appropriate next commands:

**If the step requires UI workflow (Playwright tests):**
```
✅ Step activities completed!

Next commands (in order):
1. `/create-ui-tests` - Create Playwright tests for critical journeys
2. `/run-ui-tests` - Execute and verify UI test suite
3. `/validate-step {step-number}` - Verify success criteria

Then use `/commit-and-push` to save your work.
```

**If UI workflow is NOT required:**
```
✅ Step activities completed!

Next command:
- `/validate-step {step-number}` - Verify success criteria

Then use `/commit-and-push` to save your work.
```

**IMPORTANT**: Never recommend `/validate-step` before completing required UI workflow prompts.

## Testing Scope

Follow the project testing guidelines:

- **Backend changes**: Write Jest + Supertest tests FIRST, then implement
- **Frontend component changes**: Write React Testing Library tests FIRST for component behavior, then implement
- **Critical UI journeys**: Defer to `/create-ui-tests` prompt - do NOT create Playwright tests here

## Success Indicators

You're succeeding when:
- ✅ All activity instructions have been completed
- ✅ Unit tests are written FIRST (TDD approach)
- ✅ All unit/integration tests pass
- ✅ Implementation follows project patterns
- ✅ You correctly identify when to hand off to UI workflow prompts
- ✅ You provide clear next-step guidance
- ❌ You did NOT commit or push changes
- ❌ You did NOT create Playwright UI tests

## Example Workflow

```
User: /execute-step 42

You:
1. [Runs: gh issue view 42 --comments]
2. [Parses Step 5-1 instructions]
3. [Identifies 3 activities: Add DELETE endpoint, Create delete button, Handle errors]
4. [Creates test for DELETE endpoint FIRST]
5. [Implements DELETE endpoint to pass test]
6. [Creates test for delete button behavior]
7. [Implements delete button component]
8. [Runs all tests: npm test]

Response:
"✅ Step 5-1 activities completed!

Implemented:
- DELETE /tasks/:id endpoint with tests
- Delete button component with behavior tests
- Error handling for delete operations

All unit tests passing ✅

This step requires UI workflow testing.

Next commands (in order):
1. `/create-ui-tests` - Create Playwright tests for delete journey
2. `/run-ui-tests` - Execute and verify UI test suite
3. `/validate-step 5-1` - Verify success criteria

Then use `/commit-and-push feature/delete-tasks` to save your work."
```

## Common Patterns

### Pattern: Backend API Endpoint
1. Write test describing API behavior (Jest + Supertest)
2. Watch test fail (RED)
3. Implement endpoint to pass test (GREEN)
4. Refactor for quality (REFACTOR)

### Pattern: React Component Feature
1. Write test describing component behavior (React Testing Library)
2. Watch test fail (RED)
3. Implement component logic to pass test (GREEN)
4. Refactor for readability (REFACTOR)

### Pattern: Multi-Step Activity
1. Break down into smaller incremental changes
2. Use the `todo` tool to track progress
3. Complete one change at a time
4. Verify after each change

---

**Remember**: Test first, implement second, handoff UI testing, never commit.
