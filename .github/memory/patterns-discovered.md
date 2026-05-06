# Patterns Discovered

Accumulated code patterns, solutions, and conventions discovered during development. Each pattern includes context, problem, solution, and examples.

---

## Pattern Template

```markdown
### [Pattern Name]

**Context**: When does this pattern apply?

**Problem**: What issue does it solve?

**Solution**: How to implement it

**Example**:
\`\`\`javascript
// Code example demonstrating the pattern
\`\`\`

**Related Files**: 
- path/to/relevant/file.js

**Notes**: Additional considerations or variations
```

---

## Example Pattern: Service Initialization with Empty Arrays

### Context
When initializing services that manage collections (tasks, users, items), the initial state must be defined.

### Problem
Using `null` or `undefined` for initial collection state causes errors when attempting to iterate or access array methods. For example:
- `tasks.map()` throws error if `tasks` is `null`
- Conditional checks (`if (tasks)`) required before every operation
- Inconsistent handling between services

### Solution
Initialize collections as empty arrays (`[]`) rather than `null` or `undefined`. This ensures:
- Safe iteration without null checks
- Consistent API contract (always returns array)
- Cleaner code without defensive programming

### Example
```javascript
// ❌ Problematic approach
class TaskService {
  constructor() {
    this.tasks = null;  // Requires null checks everywhere
  }
  
  getTasks() {
    return this.tasks || [];  // Defensive conversion
  }
}

// ✅ Preferred approach
class TaskService {
  constructor() {
    this.tasks = [];  // Safe to iterate immediately
  }
  
  getTasks() {
    return this.tasks;  // No conversion needed
  }
  
  addTask(task) {
    this.tasks.push(task);  // Works without null check
  }
}
```

### Related Files
- `packages/backend/src/services/taskService.js` (if exists)
- Any service managing collections

### Notes
- This pattern applies to any collection state (tasks, users, notifications, etc.)
- Consider immutability: return copies (`[...this.tasks]`) if callers shouldn't mutate internal state
- For more complex initialization, still prefer empty array over null

---

*Add new patterns below this line as they are discovered and validated*
