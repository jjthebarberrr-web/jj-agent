"""CLI entry point for jj command."""

import argparse
import asyncio
from pathlib import Path
import sys

# Add parent directory to path for imports
agent_root = Path(__file__).parent.parent
sys.path.insert(0, str(agent_root))

from config import config  # noqa: E402
from api.llm_client import LLMClient  # noqa: E402
from agent import Planner, Executor  # noqa: E402
from state.manager import StateManager  # noqa: E402
from metrics import metrics  # noqa: E402
from cli.commands import cmd_doctor, cmd_config_show, cmd_version  # noqa: E402


async def run_job(args):
    """Run a job with the given prompt."""
    # Setup workspace
    if args.workspace:
        workspace = Path(args.workspace).resolve()
    else:
        workspace = config.default_workspace

    workspace.mkdir(parents=True, exist_ok=True)

    # Setup paths
    agent_dir = Path(__file__).parent.parent
    state_dir = agent_dir / "state"

    # Load capabilities
    try:
        capabilities = config.load_capabilities(agent_dir, workspace)
    except ValueError as e:
        print(f"Error: {e}")
        return 1

    # Production mode: dry-run off by default unless explicitly requested
    dry_run = args.dry_run
    if config.is_production and not args.dry_run:
        dry_run = False

    # Initialize components
    try:
        api_key = args.api_key or config.get_secret("OPENAI_API_KEY")
        if not api_key:
            print("Error: OPENAI_API_KEY not set")
            print("Please set OPENAI_API_KEY environment variable or use --api-key")
            return 1

        llm_client = LLMClient(api_key=api_key, model=args.model)
    except ValueError as e:
        print(f"Error: {e}")
        return 1

    # Start job
    state_manager = StateManager(state_dir)
    job_id = state_manager.start_run(args.prompt, workspace, dry_run=dry_run)

    from jj_agent.logging import get_logger

    logger = get_logger(job_id=job_id)
    logger.info(
        "Job started", prompt=args.prompt, workspace=str(workspace), dry_run=dry_run
    )
    metrics.record_job_start()

    planner = Planner(llm_client)
    executor = Executor(
        workspace=workspace,
        capabilities=capabilities,
        llm_client=llm_client,
        dry_run=dry_run,
        job_id=job_id,
        state_dir=state_dir,
    )

    try:
        # Create plan
        logger.info("Planning started")
        plan = await planner.plan(args.prompt)
        logger.info(f"Plan generated with {len(plan)} steps", steps=len(plan))

        # Show plan if requested or in dry-run
        if args.plan or dry_run:
            print("\n" + "=" * 60)
            print("PLAN PREVIEW")
            print("=" * 60)
            for i, step in enumerate(plan, 1):
                print(f"\nStep {i}: {step['tool']}")
                print(f"  Args: {step.get('args', {})}")
            print("\n" + "=" * 60)

            if dry_run:
                print("\n[DRY-RUN MODE: No changes will be made]")
                state_manager.complete_run(True, {"plan": plan})
                return 0

        # Execute plan
        logger.info("Execution started")
        result = await executor.execute_with_retry(plan)

        # Complete run
        state_manager.complete_run(result["success"], result)

        if result["success"]:
            logger.info("Job completed successfully")
            print("\n✅ Execution completed successfully!")
            return 0
        else:
            logger.error("Job completed with errors")
            print("\n❌ Execution completed with errors")
            print(f"Check state directory for logs: {state_dir / job_id}")
            return 1

    except KeyboardInterrupt:
        logger.warning("Job interrupted by user")
        state_manager.complete_run(False, {"error": "Interrupted"})
        print("\n\n⚠️  Interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Job failed with exception: {e}", exc_info=True)
        from monitoring import monitoring

        monitoring.capture_exception(e)
        state_manager.complete_run(False, {"error": str(e)})
        print(f"\n\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="JJ Agent - Local-first super-agent for code generation", prog="jj"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run a job")
    run_parser.add_argument(
        "prompt", help="Natural language prompt describing what to build"
    )
    run_parser.add_argument(
        "--workspace",
        "-w",
        type=str,
        help=f"Workspace directory (default: {config.default_workspace})",
    )
    run_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show plan and diffs without executing (required in production)",
    )
    run_parser.add_argument(
        "--plan", action="store_true", help="Show plan before execution"
    )
    run_parser.add_argument(
        "--api-key", type=str, help="OpenAI API key (or set OPENAI_API_KEY env var)"
    )
    run_parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o-mini",
        help="LLM model to use (default: gpt-4o-mini)",
    )
    run_parser.add_argument(
        "--allow-web",
        action="store_true",
        help="Allow web access (requires JJ_ALLOW_WEB=1 in production)",
    )

    # Legacy: allow prompt as positional argument
    parser.add_argument("prompt_legacy", nargs="?", help=argparse.SUPPRESS)

    # Other commands
    subparsers.add_parser("doctor", help="Run diagnostics")
    subparsers.add_parser("config", help="Show configuration")
    subparsers.add_parser("version", help="Show version")

    args = parser.parse_args()

    # Handle legacy usage (jj "prompt")
    if args.prompt_legacy and not args.command:
        args.command = "run"
        args.prompt = args.prompt_legacy

    # Route to appropriate command
    if args.command == "doctor":
        return cmd_doctor()
    elif args.command == "config":
        return cmd_config_show()
    elif args.command == "version":
        return cmd_version()
    elif args.command == "run":
        if args.daemon:
            # Run as daemon with API server
            from api.server import app
            import uvicorn

            host, port = args.listen.split(":")
            uvicorn.run(app, host=host, port=int(port))
            return 0

        if not args.prompt:
            run_parser.print_help()
            return 1
        return asyncio.run(run_job(args))
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
