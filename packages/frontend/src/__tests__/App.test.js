import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import App from '../App';

// Create a test query client
const createTestQueryClient = () =>
  new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });

// Mock fetch for tests
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve([]),
  })
);

test('renders TODO App heading', async () => {
  const testQueryClient = createTestQueryClient();

  render(
    <QueryClientProvider client={testQueryClient}>
      <App />
    </QueryClientProvider>
  );

  const headingElement = await screen.findByText(/TODO App/i);
  expect(headingElement).toBeInTheDocument();
});

// Test delete functionality
test('delete button removes a todo', async () => {
  const testQueryClient = createTestQueryClient();
  const mockTodos = [
    { id: 1, title: 'Test Todo', completed: false },
  ];

  global.fetch
    .mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockTodos),
    })
    .mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({}),
    })
    .mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve([]),
    });

  render(
    <QueryClientProvider client={testQueryClient}>
      <App />
    </QueryClientProvider>
  );

  // Wait for the todo to appear
  await screen.findByText('Test Todo');

  // Click the delete button
  const deleteButton = screen.getByRole('button', { name: /delete/i });
  await userEvent.click(deleteButton);

  // Verify DELETE request was made
  await waitFor(() => {
    expect(global.fetch).toHaveBeenCalledWith(
      '/api/todos/1',
      expect.objectContaining({ method: 'DELETE' })
    );
  });
});

// Test stats calculation
test('displays correct stats for incomplete and completed todos', async () => {
  const testQueryClient = createTestQueryClient();
  const mockTodos = [
    { id: 1, title: 'Todo 1', completed: false },
    { id: 2, title: 'Todo 2', completed: false },
    { id: 3, title: 'Todo 3', completed: true },
  ];

  global.fetch.mockResolvedValueOnce({
    ok: true,
    json: () => Promise.resolve(mockTodos),
  });

  render(
    <QueryClientProvider client={testQueryClient}>
      <App />
    </QueryClientProvider>
  );

  // Wait for todos to load and verify stats
  await screen.findByText('Todo 1');
  
  // Should show 2 items left and 1 completed
  expect(screen.getByText('2 items left')).toBeInTheDocument();
  expect(screen.getByText('1 completed')).toBeInTheDocument();
});

// Test empty state
test('displays empty state message when no todos', async () => {
  const testQueryClient = createTestQueryClient();

  global.fetch.mockResolvedValueOnce({
    ok: true,
    json: () => Promise.resolve([]),
  });

  render(
    <QueryClientProvider client={testQueryClient}>
      <App />
    </QueryClientProvider>
  );

  // Wait for loading to finish and check for empty state
  await waitFor(() => {
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
  });

  // Should show empty state message
  const emptyMessage = screen.getByText(/no todos yet/i);
  expect(emptyMessage).toBeInTheDocument();
});

// Test error handling
test('displays error message when fetch fails', async () => {
  const testQueryClient = createTestQueryClient();

  global.fetch.mockRejectedValueOnce(new Error('Network error'));

  render(
    <QueryClientProvider client={testQueryClient}>
      <App />
    </QueryClientProvider>
  );

  // Wait for error message to appear
  const errorMessage = await screen.findByText(/error loading todos/i);
  expect(errorMessage).toBeInTheDocument();
});

afterEach(() => {
  jest.clearAllMocks();
});
