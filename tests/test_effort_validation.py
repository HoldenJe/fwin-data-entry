from fwin_data_entry.models.effort import Effort
from fwin_data_entry.services.effort_service import create_effort

DB_PATH = "data/examples/test_project.sqlite"

effort = Effort(
    prj_cd="26_PB_FW01",
    sam=0,
    gr="A12",
    area="01",
)

try:
    create_effort(DB_PATH, effort)
    print("ERROR: validation failed")
except ValueError as e:
    print(f"PASS: {e}")