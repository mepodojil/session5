import { test, expect } from '@playwright/test';
import { TodoPage } from '../pages/TodoPage';

test.describe('Todo Management', () => {
  let todoPage;

  test.beforeEach(async ({ page }) => {
    // Clear all todos before each test to ensure isolation
    await page.request.delete('http://localhost:3001/api/todos');
    
    todoPage = new TodoPage(page);
    await todoPage.goto();
  });

  test('should create new task', async ({ page }) => {
    await todoPage.createTask('Buy groceries');
    
    // Verify task creation succeeded
    expect(await todoPage.isTaskVisible('Buy groceries')).toBe(true);
  });

  test('should toggle task completion', async ({ page }) => {
    await todoPage.createTask('Buy groceries');
    
    // Toggle to completed
    await todoPage.toggleTask('Buy groceries');
    expect(await todoPage.isTaskCompleted('Buy groceries')).toBe(true);
    
    // Verify stats show 1 completed
    const stats = await todoPage.getStatsText();
    expect(stats.completed).toContain('1 completed');
  });

  test('should delete task', async ({ page }) => {
    await todoPage.createTask('Buy groceries');
    // Verify task exists
    expect(await todoPage.isTaskVisible('Buy groceries')).toBe(true);
    
    await todoPage.deleteTask('Buy groceries');
    // Verify task was deleted
    expect(await todoPage.getTaskCount()).toBe(0);
    expect(await todoPage.hasEmptyStateMessage()).toBe(true);
  });

  test('should display empty state when no tasks', async ({ page }) => {
    // Page loads with no tasks
    expect(await todoPage.getTaskCount()).toBe(0);
    expect(await todoPage.hasEmptyStateMessage()).toBe(true);
    
    // Add a task - empty state should disappear
    await todoPage.createTask('Test task');
    expect(await todoPage.hasEmptyStateMessage()).toBe(false);
    
    // Delete task - empty state should reappear
    await todoPage.deleteTask('Test task');
    expect(await todoPage.hasEmptyStateMessage()).toBe(true);
  });

  test('should display error when API fails', async ({ page }) => {
    // Set up route BEFORE creating TodoPage to intercept initial load
    await page.route('**/api/todos', route => {
      route.fulfill({ 
        status: 500, 
        body: JSON.stringify({ error: 'Server error' }),
        headers: { 'Content-Type': 'application/json' }
      });
    });
    
    // Create a new TodoPage instance and navigate with the mock in place
    const errorPage = new TodoPage(page);
    await errorPage.goto();
    
    // Wait a bit for React Query to process the error
    await page.waitForTimeout(1000);
    
    // Verify error message is displayed
    const errorMsg = await errorPage.getErrorMessage();
    expect(errorMsg).toBeTruthy();
    expect(errorMsg).toMatch(/error/i);
  });
});
