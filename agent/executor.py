"""Executor that runs tool calls and manages execution loop."""

from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import sys
import time

# Add tools directory to path
tools_dir = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(tools_dir.parent))

from tools import (  # noqa: E402
    FileSystemTool,
    ShellTool,
    GitTool,
    PackageTool,
    DockerTool,
    TestTool,
)

# Import logging after path setup
sys.path.insert(0, str(Path(__file__).parent.parent))
from jj_agent.logging import get_logger, AuditLogger  # noqa: E402
from metrics import metrics  # noqa: E402
from monitoring import monitoring  # noqa: E402
import webbrowser  # noqa: E402


class Executor:
    """Executes tool calls and manages the execution loop."""

    def __init__(
        self,
        workspace: Path,
        capabilities: Dict[str, Any],
        llm_client,
        dry_run: bool = False,
        job_id: Optional[str] = None,
        state_dir: Optional[Path] = None,
    ):
        self.workspace = Path(workspace).resolve()
        self.capabilities = capabilities
        self.llm_client = llm_client
        self.dry_run = dry_run
        self.job_id = job_id

        # Initialize logging
        log_file = (state_dir / job_id / "exec.log") if (state_dir and job_id) else None
        self.logger = get_logger(job_id=job_id, log_file=log_file)
        self.audit = (
            AuditLogger(job_id=job_id, state_dir=state_dir)
            if (state_dir and job_id)
            else None
        )

        # Initialize tools
        self.fs = FileSystemTool(self.workspace, capabilities)
        self.shell = ShellTool(self.workspace, capabilities)
        self.git = GitTool(self.workspace, capabilities)
        self.pkg = PackageTool(self.workspace, capabilities)
        self.docker = DockerTool(self.workspace, capabilities)
        self.tests = TestTool(self.workspace, capabilities)

        # Execution history
        self.history: List[Dict[str, Any]] = []

    def _execute_tool_call(
        self, tool_name: str, args: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a single tool call."""
        start_time = time.time()
        self.logger.info(f"Executing tool: {tool_name}", tool=tool_name, args=args)

        try:
            if tool_name == "fs_write":
                return self.fs.write(
                    path=args["path"], content=args["content"], dry_run=self.dry_run
                )

            elif tool_name == "fs_patch":
                return self.fs.patch(
                    path=args["path"],
                    old_string=args["old_string"],
                    new_string=args["new_string"],
                    dry_run=self.dry_run,
                )

            elif tool_name == "fs_mkdir":
                return self.fs.mkdir(path=args["path"], dry_run=self.dry_run)

            elif tool_name == "fs_read":
                return self.fs.read(path=args["path"])

            elif tool_name == "shell_run":
                return self.shell.run(
                    command=args["command"], cwd=args.get("cwd"), dry_run=self.dry_run
                )

            elif tool_name == "git_init":
                return self.git.init(dry_run=self.dry_run)

            elif tool_name == "git_add":
                return self.git.add(files=args.get("files", "."), dry_run=self.dry_run)

            elif tool_name == "git_commit":
                return self.git.commit(message=args["message"], dry_run=self.dry_run)

            elif tool_name == "git_branch":
                return self.git.branch(
                    name=args["name"],
                    create=args.get("create", True),
                    dry_run=self.dry_run,
                )

            elif tool_name == "git_push":
                return self.git.push(
                    remote=args.get("remote", "origin"),
                    branch=args.get("branch"),
                    dry_run=self.dry_run,
                )

            elif tool_name == "pkg_install":
                return self.pkg.install(
                    packages=args.get("packages"),
                    manager=args.get("manager"),
                    path=args.get("path"),
                    dry_run=self.dry_run,
                )

            elif tool_name == "docker_compose_up":
                return self.docker.compose_up(
                    file=args.get("file"),
                    detach=args.get("detach", True),
                    build=args.get("build", False),
                    dry_run=self.dry_run,
                )

            elif tool_name == "tests_run":
                return self.tests.run(
                    framework=args.get("framework"),
                    path=args.get("path"),
                    args=args.get("args"),
                    dry_run=self.dry_run,
                )

            elif tool_name == "browser_open":
                if not self.dry_run:
                    webbrowser.open(args["url"])
                return {"success": True, "url": args["url"], "dry_run": self.dry_run}

            else:
                result = {"success": False, "error": f"Unknown tool: {tool_name}"}

        except Exception as e:
            result = {"success": False, "error": str(e), "tool": tool_name}
            monitoring.capture_exception(e, extra={"tool": tool_name, "args": args})

        finally:
            duration_ms = (time.time() - start_time) * 1000
            metrics.record_tool_call(time.time() - start_time)

            # Record denial if applicable
            if result.get("denied"):
                metrics.record_denial()
                if self.audit:
                    self.audit.log_denial(
                        tool_name, args, result.get("error", "Denied")
                    )

            # Log to audit trail
            if self.audit:
                self.audit.log_action(
                    tool=tool_name,
                    args=args,
                    result=result,
                    duration_ms=duration_ms,
                    exit_code=result.get("returncode"),
                )

            self.logger.info(
                f"Tool execution completed: {tool_name}",
                tool=tool_name,
                success=result.get("success", False),
                duration_ms=duration_ms,
            )

        return result

    async def execute_plan(self, plan: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute a plan of tool calls."""
        start_time = time.time()
        results = []

        self.logger.info(
            f"Starting plan execution with {len(plan)} steps", steps=len(plan)
        )

        for i, step in enumerate(plan):
            tool_name = step.get("tool")
            args = step.get("args", {})

            self.logger.info(
                f"Step {i+1}/{len(plan)}: {tool_name}", step=i + 1, total=len(plan)
            )

            if not isinstance(tool_name, str) or not tool_name:
                self.logger.error(
                    "Invalid tool name in plan",
                    step=i + 1,
                    tool=tool_name,
                    args=args,
                )
                continue

            result = self._execute_tool_call(tool_name, args)
            results.append(
                {"step": i + 1, "tool": tool_name, "args": args, "result": result}
            )

            self.history.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "tool": tool_name,
                    "args": args,
                    "result": result,
                }
            )

            # Log result
            if result.get("success"):
                if result.get("denied"):
                    self.logger.warning(
                        f"Action denied: {tool_name}",
                        tool=tool_name,
                        reason=result.get("error"),
                    )
                else:
                    self.logger.info(
                        f"Step {i+1} succeeded: {tool_name}", step=i + 1, tool=tool_name
                    )
            else:
                self.logger.error(
                    f"Step {i+1} failed: {tool_name}",
                    step=i + 1,
                    tool=tool_name,
                    error=result.get("error"),
                )

        duration = time.time() - start_time
        success = all(r["result"].get("success", False) for r in results)

        self.logger.info(
            "Plan execution completed",
            success=success,
            duration_seconds=duration,
            steps=len(plan),
        )

        return {
            "success": success,
            "results": results,
            "history": self.history,
            "duration_seconds": duration,
        }

    async def execute_with_retry(
        self, plan: List[Dict[str, Any]], max_iterations: int = 3
    ) -> Dict[str, Any]:
        """Execute plan with retry logic and adaptive planning."""
        iteration = 0
        full_results = []

        while iteration < max_iterations:
            iteration += 1
            print(f"\n=== Execution Iteration {iteration}/{max_iterations} ===\n")

            result = await self.execute_plan(plan)
            full_results.append(result)

            # If all steps succeeded, we're done
            if result["success"]:
                return {
                    "success": True,
                    "iterations": iteration,
                    "results": full_results,
                }

            # If we have failures, ask LLM to plan fixes
            failures = [
                r for r in result["results"] if not r["result"].get("success", False)
            ]

            if failures and iteration < max_iterations:
                print(f"\n{len(failures)} step(s) failed. Planning fixes...")
                # Create context for LLM to fix issues
                context = {
                    "failures": [
                        {
                            "tool": f["tool"],
                            "args": f["args"],
                            "error": f["result"].get("error", "Unknown"),
                        }
                        for f in failures
                    ],
                    "history": self.history[-10:],  # Last 10 actions
                }

                # Get fix plan from LLM
                from .planner import Planner

                planner = Planner(self.llm_client)
                fix_plan = await planner.plan(
                    "Fix the errors that occurred. Review the failures and create a plan to resolve them.",
                    context=context,
                )

                if fix_plan:
                    plan = fix_plan
                    continue

            break

        return {
            "success": False,
            "iterations": iteration,
            "results": full_results,
            "message": "Failed after max iterations",
        }
