import time
import random
from typing import Tuple
from graphai.core.models import RetryPolicy

class RetryCalculator:
    """
    RetryCalculator: Computes deterministic exponential backoff intervals with jitter.
    Formula: t = min(max_backoff, base * 2^(attempt - 1) + jitter)
    """
    @staticmethod
    def calculate_backoff(attempt: int, policy: RetryPolicy) -> float:
        if attempt <= 1:
            return 0.0
        exp_factor = policy.base_backoff_seconds * (2 ** (attempt - 1))
        jitter_val = random.uniform(0.01, 0.05) if policy.jitter else 0.0
        backoff = min(policy.max_backoff_seconds, exp_factor + jitter_val)
        return round(backoff, 3)

    @staticmethod
    def should_retry(attempt: int, policy: RetryPolicy) -> bool:
        return attempt < policy.max_attempts
