{
  "name": "{{project-name}}",
  "version": "0.1.0",
  "description": "{{project-description}}",
  "main": "dist/main/app.js",
  "scripts": {
    "dev": "{{stack-choice}}-dev",
    "build": "tsc",
    "start": "node dist/main/app.js",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "quality-gate": "npm run lint && npm run type-check && npm test",
    "lint": "eslint . --ext .ts",
    "type-check": "tsc --noEmit",
    "doc-sync": "node .agent/scripts/doc-sync.js",
    "doc-review": "node .agent/scripts/doc-review.js"
  },
  "dependencies": {
    "zod": "^3.22.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "vitest": "^1.0.0",
    "eslint": "^8.0.0"
  }
}
