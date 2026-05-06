---
description: Create UI tests for required critical user journeys
agent: test-engineer
tools: [search, read, edit, execute, todo]
---

# Create UI Tests

You will create Playwright UI tests for critical user journeys using Page Object Model patterns.

## User Input

**journeys** (optional): Specific user journeys to test. If not provided, use the default set.

**Default journeys**:
- Create task (happy path)
- Edit task (happy path)
- Toggle task completion (happy path)
- Delete task (happy path)
- Error handling (validation error, network error, or edge case)

## CRITICAL CONSTRAINT: Test Count Limit

**HARD LIMIT: Maximum 5 Playwright test cases per execution**

- Target: 3-5 total Playwright `test()` or `it()` blocks
- Include at least 1 error-path test within the 3-5 total
- If more than 5 candidate scenarios exist, select the highest-risk 5
- List deferred scenarios instead of creating more tests
- Count and verify before finishing: final authored test count must be ≤ 5

**Why this limit exists**:
- Keeps test suites focused and maintainable
- Prevents test bloat and over-specification
- Ensures tests remain fast and reliable
- Forces prioritization of critical paths

## Instructions

Follow this systematic test creation workflow:

### 1. Analyze Current Test Coverage

```bash
# Check existing UI tests
ls -la packages/frontend/tests/ui/

# Review existing test content
cat packages/frontend/tests/ui/*.spec.js
```

Identify:
- What journeys are already tested
- What gaps exist in coverage
- What page objects already exist

### 2. Identify Critical Journeys (If Not Specified)

Prioritize journeys based on:
- **User impact**: Core CRUD operations (create, read, update, delete)
- **Risk level**: Error-prone flows, complex interactions
- **Business value**: Revenue-critical or frequently used features

**Select the top 3-5 highest-priority journeys** (maximum 5).

### 3. Create or Update Page Objects

Use Page Object Model to separate UI interaction logic from test logic.

**Page Object Structure**:

```javascript
// packages/frontend/tests/pages/TodoPage.js
export class TodoPage {
  constructor(page) {
    this.page = page;
    
    // Selectors as properties (accessibility-first)
    this.taskInput = page.getByRole('textbox', { name: /add task/i });
    this.addButton = page.getByRole('button', { name: /add/i });
    this.taskList = page.getByRole('list');
    this.errorMessage = page.getByRole('alert');
  }

  // Navigation methods
  async goto() {
    await this.page.goto('/');
    await this.page.waitForLoadState('networkidle');
  }

  // Interaction methods with built-in waits
  async createTask(title) {
    await this.taskInput.fill(title);
    await this.addButton.click();
    // Wait for task to appear
    await this.page.getByText(title).waitFor();
  }

  async getTaskCount() {
    return await this.taskList.getByRole('listitem').count();
  }

  async toggleTask(title) {
    const taskItem = this.page.getByText(title).locator('..');
    await taskItem.getByRole('checkbox').click();
  }

  async deleteTask(title) {
    const taskItem = this.page.getByText(title).locator('..');
    await taskItem.getByRole('button', { name: /delete/i }).click();
  }

  async getErrorMessage() {
    return await this.errorMessage.textContent();
  }

  // Query methods
  async isTaskCompleted(title) {
    const taskItem = this.page.getByText(title).locator('..');
    const checkbox = taskItem.getByRole('checkbox');
    return await checkbox.isChecked();
  }
}
```

**Page Object Best Practices**:
- ✅ One class per logical page/component
- ✅ Selectors defined as properties in constructor
- ✅ Methods encapsulate interactions + necessary waits
- ✅ Return values for data queries (getTaskCount, isTaskCompleted)
- ❌ No assertions in page objects (keep in test files)

### 4. Create Test Files

Organize tests by feature or user journey.

**Test File Structure**:

```javascript
// packages/frontend/tests/ui/task-management.spec.js
import { test, expect } from '@playwright/test';
import { TodoPage } from '../pages/TodoPage';

test.describe('Task Management', () => {
  let todoPage;

  test.beforeEach(async ({ page }) => {
    todoPage = new TodoPage(page);
    await todoPage.goto();
  });

  test('should create new task', async ({ page }) => {
    await todoPage.createTask('Buy groceries');
    
    expect(await todoPage.getTaskCount()).toBe(1);
    await expect(page.getByText('Buy groceries')).toBeVisible();
  });

  test('should toggle task completion', async ({ page }) => {
    await todoPage.createTask('Buy groceries');
    await todoPage.toggleTask('Buy groceries');
    
    expect(await todoPage.isTaskCompleted('Buy groceries')).toBe(true);
  });

  test('should delete task', async ({ page }) => {
    await todoPage.createTask('Buy groceries');
    await todoPage.deleteTask('Buy groceries');
    
    expect(await todoPage.getTaskCount()).toBe(0);
  });

  test('should show error for empty task title', async ({ page }) => {
    // Try to create task without title
    await todoPage.addButton.click();
    
    const errorMsg = await todoPage.getErrorMessage();
    expect(errorMsg).toMatch(/title.*required/i);
    expect(await todoPage.getTaskCount()).toBe(0);
  });
});
```

**Test Best Practices**:
- ✅ Group related tests with `test.describe()`
- ✅ Use `beforeEach` for common setup
- ✅ One clear assertion per test (or closely related assertions)
- ✅ Descriptive test names: "should [expected behavior] when [condition]"
- ✅ Include at least one error-path test
- ✅ Keep tests independent and isolated
- ❌ No shared state between tests
- ❌ No fixed timeouts (use state-based waits)

### 5. Use Stable Selectors (Priority Order)

**1. Accessibility-first (PREFERRED)**:
```javascript
page.getByRole('button', { name: 'Add Task' })
page.getByRole('textbox', { name: /task title/i })
page.getByLabelText('Email address')
page.getByText('Welcome')
```

**2. Test IDs (SECONDARY)**:
```javascript
page.getByTestId('task-item')
page.getByTestId('delete-button')
```

**3. CSS Selectors (AVOID)** - Only when no better option exists

### 6. Use State-Based Waits

```javascript
// ✅ Wait for element to appear
await page.getByText('Task added').waitFor();

// ✅ Wait for element to disappear
await page.getByText('Loading...').waitFor({ state: 'detached' });

// ✅ Wait for network response
await page.waitForResponse(res => res.url().includes('/api/tasks'));

// ✅ Wait for condition
await expect(page.getByText('Success')).toBeVisible();

// ❌ Avoid fixed timeouts
// await page.waitForTimeout(1000); // BAD
```

### 7. Verify Test Count Before Finishing

Before completing:

1. Count all `test()` and `it()` blocks created/modified
2. Verify count is ≤ 5
3. If count > 5, remove lower-priority tests or defer them

**Report format**:

```
Created/Updated Tests: X / 5 maximum

Test Cases:
✅ Create task (happy path)
✅ Toggle completion (happy path)
✅ Delete task (happy path)
✅ Empty title validation (error path)

[If count > 5 initially]
Deferred Scenarios (implement later):
- Edit task title
- Filter by completion status
- Bulk operations
```

### 8. Report Test Creation Summary

```
## UI Tests Created

Page Objects:
- TodoPage (created/updated) - Task management interactions

Test Files:
- task-management.spec.js (created/updated)

Test Cases: 4 / 5 maximum
✅ Create task - happy path
✅ Toggle completion - happy path
✅ Delete task - happy path
✅ Empty title validation - error path

Coverage:
- Core CRUD operations: Complete
- Error handling: Validation covered
- Edge cases: Empty state handling (deferred for future sprint)

Deferred Scenarios:
- Edit task title (medium priority)
- Network error handling (low priority - covered by retry logic)

Next step: /run-ui-tests
```

## Test Count Enforcement

**If initially planning > 5 tests**:

1. **Stop and prioritize**: Select top 5 highest-risk scenarios
2. **Document deferred tests**: List what's not being created and why
3. **Create only the top 5**: Implement the prioritized set
4. **Report the decision**: Explain prioritization in summary

**Example**:

```
Initial Assessment: 8 candidate scenarios identified

Prioritization (top 5 selected):
1. ✅ Create task (highest user impact)
2. ✅ Delete task (highest risk - data loss)
3. ✅ Toggle completion (core workflow)
4. ✅ Empty title validation (common error)
5. ✅ Network error handling (system resilience)

Deferred (3 scenarios):
6. Edit task title (lower risk, manual testing sufficient for now)
7. Filter tasks (UI-only feature, less critical)
8. Bulk actions (advanced feature, future enhancement)

Creating 5 tests within limit ✅
```

## Success Indicators

You're succeeding when:
- ✅ Test count is 3-5 (maximum 5 enforced)
- ✅ At least 1 error-path test included
- ✅ Page Objects separate interaction logic from test logic
- ✅ Tests use accessibility-first selectors
- ✅ Waits are state-based, not time-based
- ✅ Tests are independent and isolated
- ✅ Test names clearly describe expected behavior
- ✅ Coverage includes core user journeys
- ✅ If > 5 scenarios exist, you prioritized and deferred appropriately

## Common Patterns

### Pattern: Simple CRUD Journey

```javascript
test('should complete create-edit-delete cycle', async ({ page }) => {
  const todoPage = new TodoPage(page);
  await todoPage.goto();
  
  // Create
  await todoPage.createTask('Buy milk');
  expect(await todoPage.getTaskCount()).toBe(1);
  
  // Edit
  await todoPage.editTask('Buy milk', 'Buy milk and bread');
  await expect(page.getByText('Buy milk and bread')).toBeVisible();
  
  // Delete
  await todoPage.deleteTask('Buy milk and bread');
  expect(await todoPage.getTaskCount()).toBe(0);
});
```

### Pattern: Error Validation

```javascript
test('should prevent creating task with empty title', async ({ page }) => {
  const todoPage = new TodoPage(page);
  await todoPage.goto();
  
  await todoPage.addButton.click(); // No title entered
  
  await expect(todoPage.errorMessage).toBeVisible();
  await expect(todoPage.errorMessage).toContainText(/required/i);
  expect(await todoPage.getTaskCount()).toBe(0);
});
```

### Pattern: Network Error Handling

```javascript
test('should handle API failure gracefully', async ({ page }) => {
  // Mock API to return error
  await page.route('**/api/tasks', route => 
    route.fulfill({ status: 500, body: 'Server error' })
  );
  
  const todoPage = new TodoPage(page);
  await todoPage.goto();
  await todoPage.createTask('Buy milk');
  
  await expect(todoPage.errorMessage).toBeVisible();
  await expect(todoPage.errorMessage).toContainText(/error/i);
});
```

---

**Remember**: Maximum 5 tests, POM patterns, stable selectors, state-based waits.
