from fwin_data_entry.models.project import Project
from fwin_data_entry.services.project_service import create_project

DB_PATH = "data/examples/test_project.sqlite"

project = Project(
    prj_cd="",
    prj_nm="Bad Project",
    wby_nm="Rice Lake",
    prj_date0="2026-09-15",
    prj_date1="2026-10-15",
)

try:
    create_project(DB_PATH, project)
    print("ERROR: validation failed")
except ValueError as e:
    print(f"PASS: {e}")