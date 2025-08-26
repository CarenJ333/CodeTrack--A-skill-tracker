import click
from datetime import date as dt
from .db import SessionLocal, engine, Base
from .models import CodingSession
from tabulate import tabulate

# Create tables if not exist
Base.metadata.create_all(bind=engine)

@click.group()
def cli():
    """CodeTrack - Track your coding practice sessions."""
    pass

@cli.command()
@click.option("--date", prompt="Date (YYYY-MM-DD, leave empty for today)", default="", show_default=False)
@click.option("--duration", prompt="Duration (minutes)", type=int)
@click.option("--language", prompt="Programming Language")
@click.option("--notes", prompt="Notes", default="")

def log(date, duration, language, notes):
    """Log a new coding session interactively."""
    if date.strip() == "":
        session_date = dt.today()
    else:
        try:
            session_date = dt.fromisoformat(date)
        except ValueError:
            click.echo("❌ Invalid date format. Use YYYY-MM-DD.")
            return

    session = SessionLocal()
    new_entry = CodingSession(
        date=session_date,
        duration=duration,
        language=language,
        notes=notes,
    )
    session.add(new_entry)
    session.commit()
    session.close()

    click.echo(f"✅ Logged session: {duration} min of {language} on {session_date}")

@cli.command()
def view():
    """View all logged coding sessions."""
    session = SessionLocal()
    entries = session.query(CodingSession).order_by(CodingSession.date.desc()).all()
    session.close()

    if not entries:
        click.echo("📭 No coding sessions logged yet.")
        return

    table = [
        [e.id, e.date.strftime("%Y-%m-%d"), e.duration, e.language, e.notes or "-"]
        for e in entries
    ]
    headers = ["ID", "Date", "Duration (min)", "Language", "Notes"]

    click.echo(tabulate(table, headers=headers, tablefmt="fancy_grid"))