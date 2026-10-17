import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

import pytest

from api.services.alerts import get_maintenance_status


@pytest.mark.parametrize(
    "predicted_rul, expected",
    [
        (0, "CRITICAL"),
        (15, "CRITICAL"),
        (15.1, "WARNING"),
        (30, "WARNING"),
        (30.1, "NORMAL"),
        (125, "NORMAL"),
    ],
)
def test_maintenance_status_thresholds(predicted_rul, expected):
    assert get_maintenance_status(predicted_rul) == expected