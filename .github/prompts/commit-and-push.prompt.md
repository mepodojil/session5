---
description: Analyze changes, generate commit message, and push to feature branch
tools: [read, execute, todo]
---

# Commit and Push

You will analyze the current changes, generate a conventional commit message, and push to a feature branch.

## User Input

**branch-name** (REQUIRED): The name of the feature branch to commit to (e.g., `feature/add-delete-endpoint`, `fix/toggle-bug`)

If no branch name is provided, ask the user for it before proceeding.

## Instructions

Follow this systematic workflow:

### 1. Check for UI Test Requirements

If the current step includes required UI workflow:
- Verify that `/run-ui-tests` has been successfully executed in the current chat session, OR
- Run UI tests now: `npm run test:ui --workspace=frontend`

**Do not proceed with commit if required UI tests have not passed.**

### 2. Analyze Changes

```bash
# View current changes
git status

# See detailed diff
git diff

# Check staged vs unstaged
git diff --cached
```

Review the changes to understand:
- What files were modified
- What functionality was added or changed
- What tests were added or updated

### 3. Generate Conventional Commit Message

Create a commit message following the conventional commit format:

**Format**: `<type>: <description>`

**Types**:
- `feat`: New features
- `fix`: Bug fixes
- `test`: Adding or updating tests
- `refactor`: Code refactoring without behavior changes
- `chore`: Maintenance tasks (dependencies, config)
- `docs`: Documentation changes
- `style`: Formatting and style changes

**Examples**:
```
feat: add DELETE /tasks/:id endpoint
fix: resolve null reference in task list
test: add integration tests for task API
refactor: extract task validation to helper
chore: update dependencies to latest versions
```

**Guidelines**:
- Keep description concise but descriptive
- Use imperative mood ("add" not "added")
- No period at the end
- Describe WHAT changed, not HOW

### 4. Create or Switch to Branch

```bash
# Check if branch exists
git show-ref --verify --quiet refs/heads/<branch-name>

# If branch doesn't exist, create it
git checkout -b <branch-name>

# If branch exists, switch to it
git checkout <branch-name>
```

**CRITICAL**: Never commit directly to `main` or any branch other than the user-specified branch.

### 5. Stage All Changes

```bash
# Stage all modified, new, and deleted files
git add .
```

### 6. Commit with Generated Message

```bash
# Commit with the conventional commit message
git commit -m "<type>: <description>"
```

### 7. Push to Feature Branch

```bash
# Push to the specified feature branch
git push origin <branch-name>
```

If this is the first push for the branch:
```bash
# Set upstream and push
git push -u origin <branch-name>
```

### 8. Provide Summary

Report what was done:

```
✅ Changes committed and pushed!

Branch: feature/add-delete-endpoint
Commit: feat: add DELETE /tasks/:id endpoint
Files changed: 3
- packages/backend/src/app.js
- packages/backend/__tests__/app.test.js
- packages/frontend/src/App.js

Pushed to: origin/feature/add-delete-endpoint

Next steps:
- Continue with next step, or
- Create pull request: gh pr create
```

## Safety Checks

Before committing, verify:

1. ✅ All tests pass (unit, integration, and UI if required)
2. ✅ No compilation errors
3. ✅ Branch name is provided and is NOT `main`
4. ✅ Changes are intentional and complete

If any safety check fails, stop and report the issue instead of committing.

## Common Scenarios

### Scenario: First Commit on New Branch

```bash
git checkout -b feature/add-delete-endpoint
git add .
git commit -m "feat: add DELETE /tasks/:id endpoint"
git push -u origin feature/add-delete-endpoint
```

### Scenario: Additional Commit on Existing Branch

```bash
git checkout feature/add-delete-endpoint
git add .
git commit -m "test: add delete endpoint integration tests"
git push origin feature/add-delete-endpoint
```

### Scenario: Multiple Types of Changes

If changes span multiple types, either:
- Make separate commits for each logical change type, OR
- Use the most significant type in the commit message

```bash
# Option 1: Separate commits (preferred)
git add packages/backend/
git commit -m "feat: add DELETE endpoint"
git add packages/backend/__tests__/
git commit -m "test: add DELETE endpoint tests"

# Option 2: Combined commit
git add .
git commit -m "feat: add DELETE endpoint with tests"
```

## Example Workflow

```
User: /commit-and-push feature/task-deletion

You:
1. [Checks: UI tests passed in previous /run-ui-tests]
2. [Runs: git status]
   - Modified: packages/backend/src/app.js
   - Modified: packages/backend/__tests__/app.test.js
   - Modified: packages/frontend/src/App.js
   - Modified: packages/frontend/src/__tests__/App.test.js
   
3. [Analyzes changes: DELETE endpoint + UI delete button]
4. [Generates message: "feat: add task deletion functionality"]
5. [Runs: git checkout -b feature/task-deletion]
6. [Runs: git add .]
7. [Runs: git commit -m "feat: add task deletion functionality"]
8. [Runs: git push -u origin feature/task-deletion]

Response:
"✅ Changes committed and pushed!

Branch: feature/task-deletion
Commit: feat: add task deletion functionality
Files changed: 4 files
- Backend: DELETE endpoint with tests
- Frontend: Delete button with tests

Pushed to: origin/feature/task-deletion

Next steps:
- Continue to next exercise step, or
- Create pull request: gh pr create --fill"
```

## Error Handling

### If No Branch Name Provided

```
❌ Branch name is required.

Please provide a feature branch name:
Usage: /commit-and-push <branch-name>

Examples:
- /commit-and-push feature/add-delete-endpoint
- /commit-and-push fix/toggle-bug
```

### If Trying to Commit to Main

```
❌ Cannot commit directly to main branch.

Please provide a feature branch name instead:
Usage: /commit-and-push <branch-name>

Example: /commit-and-push feature/my-changes
```

### If Tests Fail

```
❌ Cannot commit: tests are failing.

Please fix failing tests before committing:
- Run: npm test
- Fix any failing tests
- Try /commit-and-push again
```

---

**Remember**: Analyze, message, branch, stage, commit, push - in that order.
