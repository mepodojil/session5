# GitHub Copilot Instructions

## Project Context

This is a full-stack TODO application with:
- **Frontend**: React-based UI for task management
- **Backend**: Express.js REST API for data operations
- **Development Approach**: Iterative, feedback-driven development with continuous validation
- **Current Phase**: Backend stabilization and frontend feature completion

The project emphasizes test-driven development (TDD) with comprehensive coverage at multiple levels: unit, integration, and end-to-end UI testing.

## Documentation References

Reference these documents to understand project conventions and patterns:

- [docs/project-overview.md](../docs/project-overview.md) - Architecture, tech stack, and project structure
- [docs/testing-guidelines.md](../docs/testing-guidelines.md) - Test patterns and standards
- [docs/workflow-patterns.md](../docs/workflow-patterns.md) - Development workflow guidance

When working on features or fixes, consult these documents first to align with established patterns.

## Development Principles

Follow these core principles throughout development:

- **Test-Driven Development**: Write tests FIRST, then implement code to pass them (RED-GREEN-REFACTOR)
- **Incremental Changes**: Make small, testable modifications rather than large sweeping changes
- **Systematic Debugging**: Use test failures as guides to identify and fix issues methodically
- **Validation Before Commit**: Ensure all tests pass and no lint errors exist before committing code

## Testing Scope

This project uses multiple testing layers for comprehensive quality assurance:

### Testing Levels

- **Backend**: Jest + Supertest for API unit and integration testing
- **Frontend**: React Testing Library for component unit and integration tests
- **UI Testing**: Playwright for critical user journey automation
- **Manual Testing**: Browser-based exploratory validation and visual checks

### Why Multiple Testing Levels?

Combine fast feedback loops (unit/integration tests) with end-to-end quality confidence (UI tests). This balanced approach catches issues early while validating complete user workflows.

### Testing Approach by Context

- **Backend API changes**: 
  - Write Jest tests FIRST for the expected API behavior
  - Run tests and watch them FAIL (RED)
  - Implement the API functionality to make tests pass (GREEN)
  - Refactor for quality while keeping tests green (REFACTOR)

- **Frontend component features**: 
  - Write React Testing Library tests FIRST for component behavior
  - Run tests and watch them FAIL (RED)
  - Implement the component logic to make tests pass (GREEN)
  - Refactor the component while keeping tests green (REFACTOR)
  - Follow with manual browser testing for full UI flows and visual validation

**This is true TDD**: Test first, then code to pass the test, then refactor.

## Workflow Patterns

Follow these established workflows for consistent development:

### 1. TDD Workflow (Primary Development Pattern)
1. Write a failing test that describes the desired behavior
2. Run the test suite and confirm the new test fails (RED)
3. Implement minimal code to make the test pass
4. Run tests again and confirm they pass (GREEN)
5. Refactor code for quality while keeping tests passing (REFACTOR)
6. Commit changes with passing tests

### 2. Code Quality Workflow
1. Run lint checks (`npm run lint` or equivalent)
2. Categorize issues by type (unused vars, formatting, logic issues)
3. Fix issues systematically, one category at a time
4. Re-run lint after each fix batch
5. Validate all tests still pass after quality improvements

### 3. Integration Workflow
1. Identify the integration issue or missing connection
2. Debug by isolating components and checking data flow
3. Write integration tests that cover the full interaction
4. Fix the integration issues to make tests pass
5. Verify end-to-end functionality manually or with UI tests

### 4. UI Testing Workflow
1. Define critical user journeys (happy paths and key error cases)
2. Create Playwright tests for these journeys
3. Run tests and analyze failures
4. Debug failures: application defect vs. test defect vs. environment issue
5. Validate test coverage matches critical business workflows

## Agent Usage

This project supports specialized agent modes for different workflows:

### tdd-developer
**Purpose**: Implement features and fixes using test-driven development

**Use for**:
- Writing unit and integration tests
- Implementing backend API endpoints with Jest tests
- Building frontend components with React Testing Library tests
- Following RED-GREEN-REFACTOR cycles

**Do NOT use for**:
- Creating or running Playwright UI tests (use test-engineer instead)
- Code review or lint fixes (use code-reviewer instead)

### code-reviewer
**Purpose**: Improve code quality and address technical debt

**Use for**:
- Fixing lint errors and warnings
- Improving code readability and maintainability
- Refactoring for better patterns
- Addressing code smell issues

### test-engineer
**Purpose**: Own all Playwright UI test creation, execution, and maintenance

**Use for**:
- Creating new Playwright UI tests for critical user journeys
- Running and debugging Playwright test failures
- Triaging test failures (application defect, test defect, or environment issue)
- Validating UI test isolation and stability
- Generating failure reports with screenshots and traces

**Do NOT use for**:
- Unit or integration test development (use tdd-developer instead)

## Memory System

This project uses a dual-memory approach to maintain context and accumulated knowledge:

### Persistent Memory
**Location**: This file (`.github/copilot-instructions.md`)

Contains foundational principles and workflows that remain stable across sessions. This includes core development principles, testing strategies, workflow patterns, and agent usage guidelines.

### Working Memory
**Location**: `.github/memory/` directory

Contains discoveries, patterns, and session-specific insights that emerge during development:

- **session-notes.md** (committed): Historical record of completed development sessions. At the end of each significant session, summarize what was accomplished, key findings, and outcomes here.

- **patterns-discovered.md** (committed): Document recurring code patterns and validated solutions as they emerge. Include context, problem, solution, and concrete examples for each pattern.

- **scratch/working-notes.md** (not committed): Active session notes for work in progress. Update continuously during development to track approach, findings, decisions, and blockers. This file is ephemeral scratch space.

### Memory Workflow

During active development:
1. Take notes in `.github/memory/scratch/working-notes.md` as you work
2. Track findings, decisions, and blockers in real-time
3. At session end, extract key insights into `session-notes.md`
4. Document validated patterns in `patterns-discovered.md`

When providing suggestions:
- Reference `session-notes.md` for recent development context
- Apply patterns from `patterns-discovered.md` for consistency
- Check `scratch/working-notes.md` for current session context

For complete memory system documentation, see [.github/memory/README.md](memory/README.md).

## Workflow Utilities

Use GitHub CLI commands for workflow automation (available in all agent modes):

### Issue Management
```bash
# List all open issues
gh issue list --state open

# View specific issue details
gh issue view <issue-number>

# View issue with all comments
gh issue view <issue-number> --comments
```

### Exercise Workflow
- The main exercise issue will have "Exercise:" in the title
- Individual steps are posted as comments on the main issue
- Use `/execute-step` prompts to work on a specific step
- Use `/validate-step` prompts to verify step completion

### Example Usage
```bash
# Find the exercise issue
gh issue list --state open | grep "Exercise:"

# View step-by-step instructions
gh issue view 1 --comments
```

## Git Workflow

Follow conventional commit practices and branching strategies:

### Conventional Commits
Use standardized commit message prefixes:
- `feat:` New features
- `fix:` Bug fixes
- `test:` Adding or updating tests
- `chore:` Maintenance tasks (dependencies, config)
- `docs:` Documentation changes
- `refactor:` Code refactoring without behavior changes
- `style:` Formatting and style changes

**Examples**:
```bash
git commit -m "feat: add task completion endpoint"
git commit -m "fix: resolve null reference in task list"
git commit -m "test: add integration tests for task API"
```

### Branch Strategy
- **Feature branches**: `feature/<descriptive-name>`
- **Bug fix branches**: `fix/<issue-description>`
- **Main branch**: `main` (protected, requires passing tests)

### Commit Workflow
```bash
# Stage all changes
git add .

# Commit with conventional format
git commit -m "feat: descriptive message"

# Push to feature branch
git push origin <branch-name>
```

### Important Reminders
- Always stage all changes before committing: `git add .`
- Push to the correct branch, not directly to `main`
- Ensure all tests pass before pushing
- Keep commits focused and atomic
