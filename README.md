1. CodeTrack- A skills tracker (CLI + ORM)

A Command-Line Interface (CLI) application for logging, tracking, and analyzing coding practice sessions.  
Built with **Python**, **SQLAlchemy (ORM)**, and **Pipenv** for dependency management. Watch the project recording at (https://www.loom.com/share/8bbff45106384172acda6e7ea5d60595?sid=389d7bb4-6e22-4600-b5c9-ed0b6e0390fa)


2. Tech Stack

- Python (v3.8.13 with pyenv)

- Pipenv (for virtual environment & dependency management)
- Sqlite

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
pipenv run python -m src.main log --duration 60 -- programming language "sql" --notes "count" --skillname "database"
```

View sessions:

```bash
pipenv run python -m src.main view
```

View streak:

```bash
pipenv run python -m src.main streak
```

View progress report:

```bash
pipenv run python -m src.main progress
```

View summaries:

Daily summary

```bash
pipenv run python -m src.main summary daily
```

Weekly summary
```bash
pipenv run python -m src.main summary weekly
```

Monthly summary
```bash
pipenv run python -m src.main summary monthly
```


### Additional Dependencies
- [tabulate](https://pypi.org/project/tabulate/) for pretty-printing tables
  Install with:
  ```bash
  pipenv run pip install tabulate
  ```


