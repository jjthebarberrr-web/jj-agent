"""Planner that converts user prompts into task graphs."""

from typing import Dict, Any, List, Optional
import json


class Planner:
    """Converts natural language prompts into executable task plans."""

    def __init__(self, llm_client):
        self.llm_client = llm_client

    def create_tool_schema(self) -> List[Dict[str, Any]]:
        """Create tool schemas for LLM function calling."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "fs_write",
                    "description": "Write content to a file. Creates the file if it doesn't exist, or overwrites if it does.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Relative path from workspace root",
                            },
                            "content": {
                                "type": "string",
                                "description": "Full file content to write",
                            },
                        },
                        "required": ["path", "content"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "fs_patch",
                    "description": "Patch a file by replacing old_string with new_string.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Relative path from workspace root",
                            },
                            "old_string": {
                                "type": "string",
                                "description": "Text to replace",
                            },
                            "new_string": {
                                "type": "string",
                                "description": "Replacement text",
                            },
                        },
                        "required": ["path", "old_string", "new_string"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "fs_mkdir",
                    "description": "Create a directory (and parent directories if needed).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Relative path from workspace root",
                            }
                        },
                        "required": ["path"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "fs_read",
                    "description": "Read a file's contents.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Relative path from workspace root",
                            }
                        },
                        "required": ["path"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "shell_run",
                    "description": "Run a shell command. Use this for installing packages, running scripts, building, etc.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {
                                "type": "string",
                                "description": "Shell command to execute",
                            },
                            "cwd": {
                                "type": "string",
                                "description": "Working directory (relative to workspace), optional",
                            },
                        },
                        "required": ["command"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "git_init",
                    "description": "Initialize a Git repository.",
                    "parameters": {"type": "object", "properties": {}, "required": []},
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "git_add",
                    "description": "Add files to Git staging area.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "files": {
                                "type": "string",
                                "description": "Files to add (default: '.')",
                            }
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "git_commit",
                    "description": "Commit changes to Git.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "Commit message",
                            }
                        },
                        "required": ["message"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "git_branch",
                    "description": "Create or switch to a Git branch.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Branch name"},
                            "create": {
                                "type": "boolean",
                                "description": "Create new branch (default: true)",
                            },
                        },
                        "required": ["name"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "git_push",
                    "description": "Push to remote Git repository.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "remote": {
                                "type": "string",
                                "description": "Remote name (default: 'origin')",
                            },
                            "branch": {
                                "type": "string",
                                "description": "Branch name (optional)",
                            },
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "pkg_install",
                    "description": "Install packages using the appropriate package manager.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "packages": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of packages to install (optional, if empty installs from lock file)",
                            },
                            "manager": {
                                "type": "string",
                                "description": "Package manager: uv, pip, npm, pnpm, yarn (optional, auto-detected)",
                            },
                            "path": {
                                "type": "string",
                                "description": "Project path (optional, defaults to workspace)",
                            },
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "docker_compose_up",
                    "description": "Start docker-compose services.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file": {
                                "type": "string",
                                "description": "docker-compose file path (optional)",
                            },
                            "detach": {
                                "type": "boolean",
                                "description": "Run in detached mode (default: true)",
                            },
                            "build": {
                                "type": "boolean",
                                "description": "Build images before starting (default: false)",
                            },
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "tests_run",
                    "description": "Run tests using pytest, jest, or other test framework.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "framework": {
                                "type": "string",
                                "description": "Test framework: pytest, jest (optional, auto-detected)",
                            },
                            "path": {
                                "type": "string",
                                "description": "Test path (optional)",
                            },
                            "args": {
                                "type": "string",
                                "description": "Additional test arguments (optional)",
                            },
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "browser_open",
                    "description": "Open a URL in the default browser.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {"type": "string", "description": "URL to open"}
                        },
                        "required": ["url"],
                    },
                },
            },
        ]

    async def plan(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Convert user prompt into a plan of tool calls."""
        system_prompt = """You are a planning agent that converts user requests into a sequence of tool calls.

You have access to the following tools:
- File system operations: fs_write, fs_patch, fs_mkdir, fs_read
- Shell commands: shell_run
- Git operations: git_init, git_add, git_commit, git_branch, git_push
- Package management: pkg_install
- Docker: docker_compose_up
- Testing: tests_run
- Browser: browser_open

Analyze the user's request and create a plan. Break down complex tasks into steps.
Consider:
1. Creating necessary directories
2. Writing files with proper content
3. Installing dependencies
4. Setting up configuration files
5. Running setup commands
6. Initializing Git if needed
7. Running tests
8. Starting services
9. Opening browser if requested

Return a JSON array of tool calls. Each tool call should have:
- tool: tool name
- args: arguments object

Be thorough and create complete, working solutions."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        if context:
            messages.append(
                {
                    "role": "assistant",
                    "content": f"Context: {json.dumps(context, indent=2)}",
                }
            )

        try:
            response = await self.llm_client.chat.completions.create(
                model="gpt-4o-mini",  # Can be made configurable
                messages=messages,
                tools=self.create_tool_schema(),
                tool_choice="auto",
                temperature=0.3,
            )

            # Extract tool calls from response
            plan = []
            if response.choices[0].message.tool_calls:
                for tool_call in response.choices[0].message.tool_calls:
                    plan.append(
                        {
                            "tool": tool_call.function.name,
                            "args": json.loads(tool_call.function.arguments),
                            "id": tool_call.id,
                        }
                    )

            return plan
        except Exception as e:
            # Fallback: try to parse as JSON plan
            return [
                {
                    "tool": "shell_run",
                    "args": {"command": f"echo Error in planning: {e}"},
                }
            ]
