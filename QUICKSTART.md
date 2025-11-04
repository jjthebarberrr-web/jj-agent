# Quick Start Guide

## Installation

1. **Install dependencies:**
```bash
cd jj-agent
pip install -r requirements.txt
```

2. **Set OpenAI API key:**
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sk-your-key-here"

# Linux/Mac
export OPENAI_API_KEY="sk-your-key-here"
```

## Usage

### Basic Example

```bash
# Create a simple FastAPI project
python -m cli.main "Create a FastAPI app with a hello world endpoint"
```

### Advanced Example

```bash
# Create a full-stack app
python -m cli.main "Create a FastAPI + React app in ./myapp with JWT auth, Postgres via docker-compose, tests, CI, start it, and open it in the browser" --workspace ./myapp
```

### Dry-Run Mode

```bash
# See what will happen without executing
python -m cli.main --dry-run "Create a React app with TypeScript"
```

## Making the `jj` Command Available

### Windows

Add `jj-agent` directory to your PATH, or create an alias:

```powershell
# In PowerShell profile
function jj { python -m cli.main $args }
```

### Linux/Mac

```bash
# Make script executable
chmod +x jj.sh

# Add to PATH or create symlink
ln -s $(pwd)/jj.sh /usr/local/bin/jj
```

Or install as a package:
```bash
pip install -e .
jj "your prompt here"
```

## First Test

Try this simple command to verify everything works:

```bash
python -m cli.main --dry-run "Create a hello world Python script"
```

This should show you a plan without executing anything.

## Troubleshooting

### "OPENAI_API_KEY not set"
Set the environment variable as shown above.

### "Module not found"
Make sure you're in the `jj-agent` directory or have installed it as a package.

### Import errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check `capabilities.yaml` to customize security settings
- Explore `skills/` directory to see available scaffolding templates
- Check `state/` directory to see execution logs

