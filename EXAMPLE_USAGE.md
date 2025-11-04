# Example Usage

## Basic Examples

### 1. Create a Simple FastAPI App

```bash
python -m cli.main "Create a FastAPI app with a hello world endpoint at /"
```

### 2. Create Full-Stack App

```bash
python -m cli.main "Create a FastAPI + React app in ./myapp with JWT auth, Postgres via docker-compose, tests, CI, start it, and open it in the browser" --workspace ./myapp
```

### 3. Dry-Run to Preview

```bash
python -m cli.main --dry-run "Create a React app with TypeScript and Tailwind CSS"
```

### 4. Specify Model

```bash
python -m cli.main --model gpt-4 "Create a complex microservices architecture"
```

### 5. Custom Workspace

```bash
python -m cli.main -w ./projects/my-new-app "Set up a Next.js project with TypeScript"
```

## What the Agent Can Do

### File Operations
- Create new files with full content
- Modify existing files (patch)
- Create directories
- Read files to understand context

### Package Management
- Install Python packages (pip, uv)
- Install Node packages (npm, pnpm, yarn)
- Auto-detect package manager

### Git Operations
- Initialize repositories
- Create branches
- Commit changes
- Push to remote

### Docker
- Start docker-compose services
- Build images
- Check service status

### Testing
- Run pytest
- Run jest
- Auto-detect test framework

### Development Servers
- Start FastAPI servers
- Start Next.js dev servers
- Open browser automatically

## Example Workflow

```bash
# 1. Create project structure
python -m cli.main "Create a FastAPI project structure with main.py, requirements.txt, and tests"

# 2. Add features
python -m cli.main "Add JWT authentication endpoints to the FastAPI app"

# 3. Set up database
python -m cli.main "Add PostgreSQL docker-compose.yml and database connection code"

# 4. Run tests
python -m cli.main "Run pytest and fix any failing tests"

# 5. Initialize Git
python -m cli.main "Initialize git, create initial commit, and push to origin"
```

## Tips

1. **Be specific**: The more details you provide, the better the plan
2. **Use dry-run first**: Preview complex operations before executing
3. **Check state logs**: Review `state/run_*.json` for detailed execution history
4. **Iterate**: The agent can fix errors automatically, but you can also run multiple commands

## Safety

- All file operations are restricted to the workspace
- Dangerous commands are blocked
- Command whitelisting prevents unauthorized operations
- Dry-run mode lets you preview changes

