# JJ Agent - Local-First Super-Agent

A local-first super-agent similar to Cursor, Devin, and Rork, but more advanced. The agent can take one natural-language prompt and automatically plan, create, modify, and manage all files in a workspace directory.

## Features

- 🚀 **One-Command Execution**: Run complex tasks with a single natural language prompt
- 📁 **File Management**: Create, modify, and manage files automatically
- 🔧 **Package Management**: Install dependencies using uv, pip, npm, pnpm, yarn
- 🐳 **Docker Support**: Run docker-compose services
- 🧪 **Testing**: Run pytest or jest and fix errors iteratively
- 🔐 **Git Integration**: Initialize repos, commit, branch, and push
- 🌐 **Browser Control**: Open browser windows after completion
- 🔒 **Safety First**: Capabilities-based security, kill-switch for dangerous commands
- 👀 **Dry-Run Mode**: Preview plans and diffs before execution

## Installation

### Production Install (Recommended)

**pipx (single command):**
```bash
pipx install jj-agent
```

**Docker:**
```bash
docker pull ghcr.io/ORG/jj-agent:latest
docker run -it --rm -e OPENAI_API_KEY=sk-... ghcr.io/ORG/jj-agent:latest jj version
```

**pip:**
```bash
pip install jj-agent
```

### Development Install

1. Clone this repository
2. Install dependencies:
```bash
cd jj-agent
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

3. Set your OpenAI API key:
```bash
export OPENAI_API_KEY=your-api-key-here
```

4. Install in development mode:
```bash
pip install -e .
```

## Usage

### Basic Usage

```bash
# After installation via pipx/pip
jj run "Create a FastAPI + React app in ./project with JWT auth, Postgres via docker-compose, tests, CI, start it, and open it in the browser."

# Or legacy format (still supported)
jj "Create a FastAPI app with JWT auth and PostgreSQL"
```

### Production Mode

```bash
# Set production environment
export JJ_ENV=production
export JJ_PROD_STRICT=1
export OPENAI_API_KEY=sk-your-key

# Run with production security
jj run "Create a FastAPI app" --workspace ~/code/demo
```

### Commands

```bash
# Run diagnostics
jj doctor

# Show configuration
jj config

# Show version
jj version

# Preview plan without executing
jj run "Create app" --plan

# Dry-run mode
jj run "Create app" --dry-run
```

### CLI Options

```bash
python -m cli.main "your prompt" [options]

Options:
  --workspace, -w DIR    Workspace directory (default: current directory)
  --dry-run              Show plan and diffs without executing
  --api-key KEY          OpenAI API key (or set OPENAI_API_KEY env var)
  --model MODEL          LLM model to use (default: gpt-4o-mini)
  --capabilities FILE    Path to capabilities.yaml file
```

### Examples

```bash
# Create a FastAPI project
python -m cli.main "Create a FastAPI app with JWT auth and PostgreSQL"

# Dry-run to see what will happen
python -m cli.main --dry-run "Create a React app with TypeScript"

# Specify workspace
python -m cli.main -w ./my-project "Set up a Next.js project with Tailwind CSS"
```

## Architecture

```
jj-agent/
├── api/              # LLM client wrapper
├── agent/            # Planner and executor
├── tools/            # Toolbox (fs, shell, git, pkg, docker, tests)
├── skills/           # Reusable scaffolding templates
├── state/            # State management and logging
├── cli/              # CLI entry point
├── prompts/          # Prompt templates
├── sandboxes/        # Docker sandbox configs
└── capabilities.yaml # Security configuration
```

## Safety Features

- **Capabilities File**: Defines allowed/denied paths, commands, and network rules
- **Kill-Switch**: Blocks dangerous commands (rm -rf /, curl|bash, fork bombs)
- **Path Validation**: Ensures all file operations stay within workspace
- **Command Whitelisting**: Only allows pre-approved commands

## Skills

Skills are reusable templates for scaffolding common frameworks:

- `fastapi`: FastAPI with JWT auth, PostgreSQL, tests

More skills can be added in the `skills/` directory.

## State Management

All runs are logged in `state/` directory with:
- Execution history
- Tool call results
- Timestamps
- Success/failure status

## Development

To add new tools:

1. Create a new tool class in `tools/`
2. Add it to `tools/__init__.py`
3. Register it in `agent/planner.py` tool schema
4. Add handler in `agent/executor.py`

To add new skills:

1. Create a skill function in `skills/`
2. Register it in `skills/__init__.py`

## License

MIT

