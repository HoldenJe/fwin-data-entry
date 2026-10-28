# FWIN Data Entry

Python desktop application for FWIN fisheries survey data entry.

# FWIN Data Entry

Python desktop application for FWIN fisheries survey data entry.

## Goals

- Fast keyboard-driven data entry
- FishNet-compatible data model
- SQLite backend
- Export to FishNet-compatible formats

## Current Features

- FN011 Project Information
- FN121 Effort Data Entry
- FN123 Catch Summaries
- FN125 Fish Samples
- Create, edit, and validate records
- SQLite project databases
- User-defined database locations

## Installation

A *.exe installer can be downloaded from https://github.com/HoldenJe/fwin-data-entry/releases

## Alternate Installation for Python Users
### Clone Repository

```powershell
git clone https://github.com/HoldenJe/fwin-data-entry.git
cd fwin-data-entry
```

### Build Locally

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/fwin_data_entry/app.py
```

### Build Installer

```powershell
pyinstaller FWIN-Data-Entry.spec
```

## Database Structure

The application stores data in an SQLite database using the following tables:

- FN011 - Project Information  
- FN121 - Effort Information  
- FN123 - Catch Summaries  
- FN125 - Fish Samples  

## Accessing Data in R

The SQLite database can be accessed directly from R.

### Read FN121

```r
library(DBI)
library(RSQLite)

con <- dbConnect(
  SQLite(),
  "MyProject.sqlite"
)

fn121 <- dbReadTable(
  con,
  "FN121"
)

dbDisconnect(con)

head(fn121)

```

### Read All Tables

```r
library(DBI)
library(RSQLite)

con <- dbConnect(
  SQLite(),
  "MyProject.sqlite"
)

fn011 <- dbReadTable(con, "FN011")
fn121 <- dbReadTable(con, "FN121")
fn123 <- dbReadTable(con, "FN123")
fn125 <- dbReadTable(con, "FN125")

dbDisconnect(con)
```

### Example Join

```r
library(DBI)
library(RSQLite)
library(dplyr)

con <- dbConnect(
  SQLite(),
  "MyProject.sqlite"
)

fn121 <- dbReadTable(con, "FN121")
fn123 <- dbReadTable(con, "FN123")

dbDisconnect(con)

catch_summary <- fn123 %>%
  left_join(
    fn121,
    by = c(
      "PRJ_CD",
      "SAM"
    )
  )

catch_summary
```

## Development Status

Current release: v0.5.0

This application is currently being tested by FWIN users. Feedback on workflow, validation, and usability is encouraged.

## Roadmap

Potential future enhancements include:

- Date and time validation
- Dynamic field configuration
- FN012-driven validation rules
- Species-specific FN125 entry requirements
- Improved testing coverage
