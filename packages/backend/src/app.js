const express = require('express');
const cors = require('cors');

// Initialize express app
const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// In-memory data store for TODOs
let todos = [];

// Counter for ID generation
let nextId = 1;

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// GET /api/todos - Get all todos
// INTENTIONAL ISSUE: This endpoint has a bug - it doesn't handle the case when todos is null
app.get('/api/todos', (req, res) => {
  res.json(todos);
});

// POST /api/todos - Create a new todo
app.post('/api/todos', (req, res) => {
  const { title } = req.body;

  // Validate title is provided and not empty
  if (!title || title.trim() === '') {
    return res.status(400).json({ error: 'Title is required' });
  }

  // Create new todo
  const newTodo = {
    id: nextId++,
    title,
    completed: false,
    createdAt: new Date().toISOString()
  };

  todos.push(newTodo);
  res.status(201).json(newTodo);
});

// PUT /api/todos/:id - Update a todo
app.put('/api/todos/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const { title } = req.body;
  
  const todo = todos.find((t) => t.id === id);
  
  if (!todo) {
    return res.status(404).json({ error: 'Todo not found' });
  }

  // Update title if provided, but preserve completed status
  if (title !== undefined) {
    todo.title = title;
  }

  res.json(todo);
});

// PATCH /api/todos/:id/toggle - Toggle todo completion status
app.patch('/api/todos/:id/toggle', (req, res) => {
  const id = parseInt(req.params.id);
  const todo = todos.find((t) => t.id === id);

  if (!todo) {
    return res.status(404).json({ error: 'Todo not found' });
  }

  // Toggle the completed status
  todo.completed = !todo.completed;

  res.json(todo);
});


// DELETE /api/todos - Delete all todos (for test cleanup)
app.delete('/api/todos', (req, res) => {
  todos = [];
  nextId = 1; // Reset ID counter
  res.status(204).send();
});
// DELETE /api/todos/:id - Delete a todo
app.delete('/api/todos/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const todoIndex = todos.findIndex((t) => t.id === id);

  if (todoIndex === -1) {
    return res.status(404).json({ error: 'Todo not found' });
  }

  // Remove the todo from array
  todos.splice(todoIndex, 1);
  
  res.status(200).json({ message: 'Todo deleted' });
});

// INTENTIONAL ISSUE: Missing error handling middleware

module.exports = app;
