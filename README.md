1. CodeTrack- A skills tracker (CLI + ORM)

A Command-Line Interface (CLI) application for logging, tracking, and analyzing coding practice sessions.  
Built with **Python**, **SQLAlchemy (ORM)**, and **Pipenv** for dependency management.

2. Tech Stack

- Python (v3.8.13 with pyenv)

- Pipenv (for virtual environment & dependency management)

- SQLite (database)

- SQLAlchemy (ORM)

- Click (for CLI)

- Tabulate (for pretty tables)

3. Setup Instructions

Prerequisites:

Install pyenv

Install pipenv

Ensure SQLite libraries installed (libsqlite3-dev if on Linux)

Clone repo

### Install dependencies
Install project dependencies with:
```bash
pipenv install
```
### Enter the virtual environment
Activate the Pipenv shell with:
```bash
pipenv shell
```

### 4. Usage

Run the CLI:
```bash
pipenv run python -m src.main
```
Log a coding session:

```bash
pipenv run python -m src.main log --duration 60 --notes "Worked on data structures"
```

View sessions:

```bash
pipenv run python -m src.main view
```

### DEVELOPMENT NOTES

How to run tests:
```bash
pipenv run pytest
```

### Additional Dependencies
- [tabulate](https://pypi.org/project/tabulate/) for pretty-printing tables
  Install with:
  ```bash
  pipenv run pip install tabulate
  ```


