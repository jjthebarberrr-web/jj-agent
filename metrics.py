"""Metrics collection for monitoring."""

from typing import Dict, Any


class Metrics:
    """Simple metrics collector."""

    def __init__(self):
        self.jobs_started = 0
        self.jobs_succeeded = 0
        self.jobs_failed = 0
        self.job_times: list = []
        self.tool_times: list = []
        self.denied_actions_count = 0
        self.cache_hits = 0
        self.cache_misses = 0

    def record_job_start(self):
        """Record job start."""
        self.jobs_started += 1

    def record_job_success(self, duration_seconds: float):
        """Record successful job completion."""
        self.jobs_succeeded += 1
        self.job_times.append(duration_seconds)

    def record_job_failure(self, duration_seconds: float):
        """Record job failure."""
        self.jobs_failed += 1
        self.job_times.append(duration_seconds)

    def record_tool_call(self, duration_seconds: float):
        """Record tool call duration."""
        self.tool_times.append(duration_seconds)

    def record_denial(self):
        """Record denied action."""
        self.denied_actions_count += 1

    def record_cache_hit(self):
        """Record cache hit."""
        self.cache_hits += 1

    def record_cache_miss(self):
        """Record cache miss."""
        self.cache_misses += 1

    def get_stats(self) -> Dict[str, Any]:
        """Get current metrics."""
        avg_job_time = (
            sum(self.job_times) / len(self.job_times) if self.job_times else 0
        )
        avg_tool_time = (
            sum(self.tool_times) / len(self.tool_times) if self.tool_times else 0
        )

        total_cache = self.cache_hits + self.cache_misses
        cache_hit_rate = self.cache_hits / total_cache if total_cache > 0 else 0

        return {
            "jobs_started": self.jobs_started,
            "jobs_succeeded": self.jobs_succeeded,
            "jobs_failed": self.jobs_failed,
            "avg_job_time_seconds": avg_job_time,
            "avg_tool_time_seconds": avg_tool_time,
            "denied_actions_count": self.denied_actions_count,
            "cache_hit_rate": cache_hit_rate,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
        }


# Global metrics instance
metrics = Metrics()
