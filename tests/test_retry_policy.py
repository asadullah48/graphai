import pytest
from graphai.core.retry_policy import RetryCalculator
from graphai.core.models import RetryPolicy

def test_retry_calculation():
    policy = RetryPolicy(max_attempts=3, base_backoff_seconds=0.5, max_backoff_seconds=5.0, jitter=False)
    b1 = RetryCalculator.calculate_backoff(1, policy)
    b2 = RetryCalculator.calculate_backoff(2, policy)
    b3 = RetryCalculator.calculate_backoff(3, policy)
    assert b1 == 0.0
    assert b2 == 1.0 # 0.5 * 2^1
    assert b3 == 2.0 # 0.5 * 2^2
    assert RetryCalculator.should_retry(2, policy) is True
    assert RetryCalculator.should_retry(3, policy) is False
