from fwin_data_entry.models.effort import Effort
from fwin_data_entry.services.effort_service import (
    create_effort,
    get_effort,
)

DB_PATH = "data/examples/test_project.sqlite"

effort = Effort(
    prj_cd="26_PB_FW01",
    sam=1,
    gr="A12",
    area="01",
    effdt0="2026-09-15",
    efftm0="09:15",
    secchi=2.5,
    grdepmin=2.0,
    grdepmax=4.5,
)

create_effort(DB_PATH, effort)

record = get_effort(
    DB_PATH,
    "26_PB_FW01",
    1,
)

print(record)