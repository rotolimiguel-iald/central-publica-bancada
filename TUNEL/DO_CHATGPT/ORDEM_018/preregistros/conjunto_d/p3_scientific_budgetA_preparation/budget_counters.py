"""Exact pre-evaluation counters; standard-library-only, no scientific calls."""
from failure_audit import BudgetStop

EXPECTED_LIMITS = {
    "max_likelihood_calls": 100000, "native_waveform_calls_at_most": 100000,
    "wall_soft_s": 14400, "supervisor_wall_s": 14410,
    "cpu_soft_s": 13200, "cpu_hard_s": 13205,
    "address_space_bytes": 8589934592, "workers": 1, "threads": 1,
    "parallel_jobs": 1, "jobs_at_most": 2, "no_retry": True,
}


def validate_limits(limits):
    if not isinstance(limits, dict) or set(limits) != set(EXPECTED_LIMITS):
        raise ValueError("Exact proposed A limits required")
    for key, expected in EXPECTED_LIMITS.items():
        if type(limits[key]) is not type(expected) or limits[key] != expected:
            raise ValueError("Limit/type differs: " + key)


class CallBudget:
    """Reservations include initialization; counters never reset or retry."""
    def __init__(self, likelihood_limit, native_limit):
        if any(type(x) is not int or x <= 0 for x in (likelihood_limit, native_limit)):
            raise ValueError("Positive integer call limits required")
        self.likelihood_limit = likelihood_limit
        self.native_limit = native_limit
        self.likelihood_started = 0
        self.native_reserved = 0

    def take_likelihood(self):
        if self.likelihood_started >= self.likelihood_limit:
            raise BudgetStop("MAXCALL_INCLUDING_INITIALIZATION")
        self.likelihood_started += 1
        return self.likelihood_started

    def take_native(self):
        if self.native_reserved >= self.native_limit:
            raise BudgetStop("MAX_NATIVE_RESERVED_BEFORE_WAVEFORM")
        self.native_reserved += 1
        return self.native_reserved

    def snapshot(self):
        return {"likelihood_started": self.likelihood_started,
                "native_reserved": self.native_reserved,
                "likelihood_limit": self.likelihood_limit,
                "native_limit": self.native_limit}
