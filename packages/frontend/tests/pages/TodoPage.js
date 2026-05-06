export class TodoPage {
  constructor(page) {
    this.page = page;
    
    // Selectors as properties (accessibility-first)
    this.taskInput = page.getByPlaceholder('What needs to be done?');
    this.addButton = page.getByRole('button', { name: 'Add' });
    this.errorAlert = page.getByRole('alert');
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
    // Wait for task to appear in the list
    await this.page.getByRole('listitem').filter({ hasText: title }).waitFor({ timeout: 5000 });
    // Wait for DOM to fully stabilize after React Query update
    await this.page.waitForLoadState('networkidle');
  }

  async getTaskCount() {
    // Ensure page is stable before counting
    await this.page.waitForLoadState('domcontentloaded');
    const tasks = await this.page.locator('[role="listitem"]').count();
    return tasks;
  }

  async toggleTask(title) {
    // Find the list item containing the task title, then find its checkbox
    const taskItem = this.page.getByRole('listitem').filter({ hasText: title });
    const checkbox = taskItem.getByRole('checkbox').first();
    await checkbox.click();
    // Wait for the state to update
    await this.page.waitForTimeout(300);
  }

  async deleteTask(title) {
    // Find the list item containing the task title, then find its delete button
    const taskItem = this.page.getByRole('listitem').filter({ hasText: title });
    const deleteButton = taskItem.getByRole('button', { name: /delete/i });
    await deleteButton.click();
    // Wait for the task to be removed
    await this.page.getByRole('listitem').filter({ hasText: title }).waitFor({ state: 'detached', timeout: 5000 });
    // Wait for state to stabilize
    await this.page.waitForLoadState('networkidle');
  }

  // Query methods
  async isTaskCompleted(title) {
    const taskItem = this.page.getByRole('listitem').filter({ hasText: title });
    const checkbox = taskItem.getByRole('checkbox').first();
    return await checkbox.isChecked();
  }

  async getTaskText(title) {
    const task = this.page.getByText(title);
    return await task.textContent();
  }

  async hasEmptyStateMessage() {
    try {
      const emptyMessage = this.page.getByText(/no todos yet/i);
      return await emptyMessage.isVisible({ timeout: 2000 });
    } catch {
      return false;
    }
  }

  async getStatsText() {
    const stats = {
      itemsLeft: await this.page.getByText(/items? left/).textContent(),
      completed: await this.page.getByText(/completed/).textContent(),
    };
    return stats;
  }

  async getErrorMessage() {
    try {
      await this.errorAlert.waitFor({ state: 'visible', timeout: 5000 });
      return await this.errorAlert.textContent();
    } catch {
      return null;
    }
  }

  async isTaskVisible(title) {
    try {
      const task = this.page.getByRole('listitem').filter({ hasText: title });
      return await task.isVisible({ timeout: 2000 });
    } catch {
      return false;
    }
  }
}
