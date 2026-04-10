# Project Context for AI Code Review

## Architecture

- Monorepo with NX
- Frontend: React + TypeScript + TanStack Query
- Backend: Node.js + NestJS + TypeORM
- Database: PostgreSQL

## Code Conventions

- Use functional components with hooks (no class components)
- All API calls go through `src/api/` layer — never call fetch directly in components
- Use `zod` for runtime validation of API responses
- Prefer `const` over `let`; never use `var`
- Error handling: always use custom `AppError` class, never throw raw strings
- Naming: camelCase for variables/functions, PascalCase for types/components
- Files: kebab-case (e.g. `user-profile.tsx`, not `UserProfile.tsx`)

## Security Rules

- Never commit secrets, API keys, or tokens
- Always sanitize user input before DB queries
- Use parameterized queries — no string concatenation in SQL
- Auth tokens must be validated on every API endpoint

## Testing

- Unit tests required for all business logic (utils, services)
- Integration tests required for API endpoints
- Use `describe/it` pattern with descriptive names
- Mock external dependencies, never call real APIs in tests

## What NOT to flag

- Import ordering (handled by ESLint)
- Trailing commas, semicolons (handled by Prettier)
- Line length (handled by Prettier)
