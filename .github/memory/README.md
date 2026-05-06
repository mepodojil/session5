# Memory System

## Purpose

This memory system tracks patterns, decisions, and lessons learned during development. It helps both human developers and AI assistants understand the evolution of the codebase and apply context-aware suggestions based on accumulated knowledge.

## Memory Types

### Persistent Memory
**Location**: `.github/copilot-instructions.md`

Contains foundational principles, workflows, and guidelines that remain stable across sessions:
- Core development principles (TDD, incremental changes)
- Project architecture and tech stack
- Testing strategies and conventions
- Workflow patterns (TDD, code quality, integration)

### Working Memory
**Location**: `.github/memory/`

Contains discoveries, patterns, and session-specific insights that emerge during development:
- Session summaries (historical record of completed work)
- Code patterns discovered and validated
- Active session notes (ephemeral, not committed)

## Directory Structure

```
.github/memory/
├── README.md                    # This file - explains the memory system
├── session-notes.md             # Historical summaries of completed sessions (committed)
├── patterns-discovered.md       # Accumulated code patterns and solutions (committed)
└── scratch/
    ├── .gitignore              # Ignores all files in scratch/ (active work not committed)
    └── working-notes.md        # Active session notes (not committed)
```

## When to Use Each File

### session-notes.md (Committed)
**Purpose**: Historical record of completed development sessions

**Use when**:
- Completing a development session or milestone
- Summarizing key findings from a feature implementation
- Documenting decisions that future work should reference
- Recording outcomes of debugging or refactoring efforts

**Update frequency**: At the end of each significant development session

**Format**: Append new session summaries chronologically

### patterns-discovered.md (Committed)
**Purpose**: Document recurring code patterns and validated solutions

**Use when**:
- Discovering a pattern that solves a specific problem
- Finding a better approach after refactoring
- Identifying conventions that should be followed consistently
- Documenting solutions to tricky integration issues

**Update frequency**: As patterns emerge and are validated through testing

**Format**: Update existing patterns or add new ones with clear examples

### scratch/working-notes.md (Not Committed)
**Purpose**: Active session notes for work in progress

**Use when**:
- Starting a new development task or debugging session
- Tracking approach and findings as you work
- Recording decisions made during implementation
- Noting blockers or questions that arise
- Planning next steps mid-session

**Update frequency**: Continuously during active development

**Format**: Overwrite with current session content; summarize key findings into session-notes.md when session ends

## Workflow Integration

### TDD Workflow
1. **Before starting**: Review `patterns-discovered.md` for relevant testing patterns
2. **During work**: Record test failures, hypothesis, and solutions in `scratch/working-notes.md`
3. **After session**: If new testing patterns emerge, document in `patterns-discovered.md`
4. **Session end**: Summarize TDD cycle outcomes in `session-notes.md`

### Linting Workflow
1. **During fixes**: Track categories of lint errors in `scratch/working-notes.md`
2. **If pattern emerges**: Document the systematic fix approach in `patterns-discovered.md`
3. **Session end**: Summarize code quality improvements in `session-notes.md`

### Debugging Workflow
1. **Initial investigation**: Document symptoms and hypotheses in `scratch/working-notes.md`
2. **As you debug**: Track what you've tried and what worked
3. **Resolution**: If the solution reveals a pattern, add to `patterns-discovered.md`
4. **Session end**: Record the root cause and fix in `session-notes.md`

### Integration Work
1. **Planning**: Note integration points and data flow in `scratch/working-notes.md`
2. **During implementation**: Track API contracts and state management decisions
3. **Validation**: Document successful integration patterns in `patterns-discovered.md`
4. **Session end**: Summarize integration approach and outcomes in `session-notes.md`

## How AI Reads and Applies Memory

### Context-Aware Suggestions
When GitHub Copilot or AI assistants work on this codebase, they:
1. Read `.github/copilot-instructions.md` for core principles and workflows
2. Review `session-notes.md` for recent development context
3. Check `patterns-discovered.md` for established patterns to follow
4. Reference `scratch/working-notes.md` for current session context

### Pattern Application
AI assistants use this memory to:
- Suggest code that follows documented patterns
- Avoid approaches that were tried and rejected
- Apply lessons from debugging sessions to new issues
- Maintain consistency with established conventions
- Provide context-aware explanations and recommendations

### Evolution Over Time
As the codebase matures:
- Patterns become more refined and specific
- Session notes provide historical context for decisions
- New patterns build on validated approaches
- AI suggestions improve based on accumulated knowledge

## Best Practices

### Writing Session Notes
- Be concise but specific
- Focus on decisions and outcomes, not just activities
- Include enough context for future reference
- Link to relevant commits or PRs when applicable

### Documenting Patterns
- Use clear, descriptive names
- Include concrete code examples
- Explain the problem context and why the solution works
- Reference related files or patterns

### Maintaining Working Notes
- Update throughout the session as you learn
- Don't worry about polish - they're scratch space
- At session end, extract key findings for session-notes.md
- Working notes can be cleared or overwritten for next session

### Keeping Memory Current
- Review session notes periodically to extract patterns
- Update patterns as better approaches emerge
- Archive or consolidate old session notes if they become outdated
- Keep the memory system focused on actionable insights

## Benefits

1. **Continuity**: Pick up where you left off, even after breaks
2. **Learning**: Convert debugging time into reusable knowledge
3. **Consistency**: Follow established patterns automatically
4. **Efficiency**: Avoid repeating mistakes or re-discovering solutions
5. **Collaboration**: Share context with team members and AI assistants
6. **Quality**: Build on validated approaches rather than ad-hoc solutions

---

*Remember: The memory system is a living document. Update it as you learn, and it will help you work more effectively over time.*
