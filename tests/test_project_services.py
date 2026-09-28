"""Test Project services."""
from fwin_data_entry.models.project import Project
from fwin_data_entry.services.project_service import (
    create_project,
    get_project,
)

DB_PATH = "data/examples/test_project.sqlite"

project = Project(
    prj_cd="26_PB_FW02",
    prj_nm="Scugog Lake FWIN 2026",
    wby_nm="Scugog Lake",
    prj_date0="2026-09-15",
    prj_date1="2026-10-15",
    comment="Dataclass test",
)

create_project(DB_PATH, project)

record = get_project(DB_PATH, "26_PB_FW02")

print(record)