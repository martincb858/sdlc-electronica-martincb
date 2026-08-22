from app.domain.stats import ReadingStats, compute_stats


def test_compute_stats_with_values() -> None:
    stats = compute_stats([10.0, 20.0, 30.0])

    assert stats == ReadingStats(count=3, minimum=10.0, maximum=30.0, average=20.0)


def test_compute_stats_with_single_value() -> None:
    stats = compute_stats([15.5])

    assert stats == ReadingStats(count=1, minimum=15.5, maximum=15.5, average=15.5)


def test_compute_stats_with_no_values() -> None:
    stats = compute_stats([])

    assert stats == ReadingStats(count=0, minimum=None, maximum=None, average=None)
