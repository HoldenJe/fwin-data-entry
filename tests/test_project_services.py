"""Test Project services."""

from fwin_data_entry.services.project_service import (
get_project,
)

DB_PATH = "data/examples/test_project.sqlite"

project = get_project(
DB_PATH,
"26_PB_FW02",
)

print(project.prj_cd)
print(project.prj_nm)