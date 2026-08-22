from dataclasses import dataclass


@dataclass(frozen=True)
class ReadingStats:
    count: int
    minimum: float | None
    maximum: float | None
    average: float | None


def compute_stats(values: list[float]) -> ReadingStats:
    """Calcula minimo, maximo y promedio de un conjunto de lecturas."""
    if not values:
        return ReadingStats(count=0, minimum=None, maximum=None, average=None)

    return ReadingStats(
        count=len(values),
        minimum=min(values),
        maximum=max(values),
        average=sum(values) / len(values),
    )
