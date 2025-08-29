import click
from sqlalchemy import func
from datetime import date as dt, datetime, timedelta
from .db import SessionLocal, engine, Base
from .models import CodingSession, Skill
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
@click.option("--skill", prompt="Skill name")

def log(date, duration, language, notes, skill):
    """Log a new coding session interactively."""
    from .models import Skill

    if date.strip() == "":
        session_date = dt.today()
    else:
        try:
            session_date = dt.fromisoformat(date)
        except ValueError:
            click.echo("Invalid date format. Use YYYY-MM-DD.")
            return

    db = SessionLocal()

        # Find or create skill
    skill_obj = db.query(Skill).filter_by(name=skill).first()
    if not skill_obj:
        skill_obj = Skill(name=skill)
        db.add(skill_obj)
        db.commit() 
        click.echo(f" Created new skill: {skill}")

    new_entry = CodingSession(
        date=session_date,
        duration=duration,
        language=language,
        notes=notes,
        skill=skill_obj 
    )
    db.add(new_entry)
    db.commit()
    db.close()

    click.echo(f"✅ Logged session: {duration} min of {language} ({skill}) on {session_date}")


@cli.command()
def view():
    """View all logged coding sessions."""
    session = SessionLocal()
    entries = session.query(CodingSession).order_by(CodingSession.date.desc()).all()
    session.close()

    if not entries:
        click.echo("No coding sessions logged yet.")
        return

    table = [
        [e.id, e.date.strftime("%Y-%m-%d"), e.duration, e.language, e.notes or "-"]
        for e in entries
    ]

    headers = ["ID", "Date", "Duration (min)", "Language", "Notes"]
    click.echo(tabulate(table, headers=headers, tablefmt="fancy_grid"))

@cli.command()
def skills():
    """View all skills in the database."""
    session = SessionLocal()
    all_skills = session.query(Skill).order_by(Skill.name).all()
    session.close()

    if not all_skills:
        click.echo("No skills logged yet.")
        return

    table = [[s.id, s.name] for s in all_skills]
    headers = ["ID", "Skill"]
    click.echo(tabulate(table, headers=headers, tablefmt="fancy_grid"))


@cli.command()
@click.argument("period", type=click.Choice(["daily", "weekly", "monthly"], case_sensitive=False))
def summary(period):
    """Show total coding time for a chosen period."""
    db = SessionLocal()

    now = datetime.utcnow()

    if period.lower() == "daily":
        start_date = datetime(now.year, now.month, now.day)
    elif period.lower() == "weekly":
        start_date = now - timedelta(days=now.weekday())  # Monday of this week
        start_date = datetime(start_date.year, start_date.month, start_date.day)
    else:  # monthly
        start_date = datetime(now.year, now.month, 1)

    # Query sessions since start_date
    sessions = db.query(CodingSession).filter(CodingSession.date >= start_date).all()

    if not sessions:
        click.echo(f"No coding sessions logged for {period}.")
        db.close()
        return

    # Total duration
    total_minutes = sum(s.duration for s in sessions)

    # Breakdown by skill
    breakdown = {}
    for s in sessions:
        skill_name = s.skill.name
        breakdown[skill_name] = breakdown.get(skill_name, 0) + s.duration

    db.close()

    click.echo(f"🗓 {period.capitalize()} Summary (since {start_date.date()}):")
    click.echo(f"Total time: {total_minutes} min")

    # Show breakdown
    table = [[skill, minutes] for skill, minutes in breakdown.items()]
    headers = ["Skill", "Minutes"]
    click.echo(tabulate(table, headers=headers, tablefmt="fancy_grid"))


@cli.command()
@click.option("--skill", default=None, help="Filter sessions by skill name")
def history(skill):
    """Show all coding sessions, optionally filtered by skill."""
    db = SessionLocal()

    query = db.query(CodingSession)

    if skill:
        query = query.join(Skill).filter(Skill.name.ilike(f"%{skill}%"))

    sessions = query.order_by(CodingSession.date.desc()).all()

    if not sessions:
        if skill:
            click.echo(f" No coding sessions found for skill '{skill}'.")
        else:
            click.echo("No coding sessions found.")
        db.close()
        return

    # Format table
    table = []
    for s in sessions:
        table.append([
            s.id,
            s.date.strftime("%Y-%m-%d %H:%M"),
            s.language,
            s.skill.name,
            s.duration,
            s.notes or ""
        ])

    headers = ["ID", "Date", "Language", "Skill", "Minutes", "Notes"]
    click.echo(tabulate(table, headers=headers, tablefmt="fancy_grid"))

    db.close()

@cli.command()
def progress():
    """Show overall progress statistics."""
    db = SessionLocal()

    sessions = db.query(CodingSession).order_by(CodingSession.date).all()
    if not sessions:
        click.echo(" No sessions logged yet.")
        db.close()
        return

    # Total practice hours
    total_minutes = sum(s.duration for s in sessions)
    total_hours = total_minutes / 60

    # Most practiced skill
    skill_totals = {}
    for s in sessions:
        skill_totals[s.skill.name] = skill_totals.get(s.skill.name, 0) + s.duration
    most_practiced = max(skill_totals, key=skill_totals.get)

    # Longest streak
    dates = sorted({s.date.date() for s in sessions})
    longest_streak = 1
    current_streak = 1
    for i in range(1, len(dates)):
        if (dates[i] - dates[i-1]).days == 1:
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            current_streak = 1

    # Average daily practice
    first_day, last_day = dates[0], dates[-1]
    total_days = (last_day - first_day).days + 1
    avg_daily = total_minutes / total_days

    # Average weekly practice
    total_weeks = max(1, total_days // 7)
    avg_weekly = total_minutes / total_weeks

    db.close()

    click.echo("Progress Report")
    click.echo(f"Total practice: {total_hours:.1f} hours ({total_minutes} min)")
    click.echo(f"Most practiced skill: {most_practiced} ({skill_totals[most_practiced]} min)")
    click.echo(f"Longest streak: {longest_streak} days")
    click.echo(f"Average daily: {avg_daily:.1f} min")
    click.echo(f"Average weekly: {avg_weekly:.1f} min")

@cli.command()
def streak():
    """Track your current and longest streaks, with break alerts."""
    db = SessionLocal()
    sessions = db.query(CodingSession).order_by(CodingSession.date).all()

    if not sessions:
        click.echo(" No sessions logged yet.")
        db.close()
        return

    dates = sorted({s.date.date() for s in sessions})
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)

    # Longest streak calculation
    longest_streak = 1
    current_streak = 1
    for i in range(1, len(dates)):
        if (dates[i] - dates[i-1]).days == 1:
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            current_streak = 1

    #  Current streak (check today/yesterday)
    if dates[-1] == today:
        streak_count = current_streak
        streak_status = "🔥 Active streak!"
    elif dates[-1] == yesterday:
        streak_count = current_streak
        streak_status = "⚠️ Continue tomorrow to keep it alive!"
    else:
        streak_count = 0
        streak_status = "💔 Streak broken."

    db.close()

    click.echo(" Streak Tracker")
    click.echo(f"Current streak: {streak_count} days → {streak_status}")
    click.echo(f"Longest streak: {longest_streak} days")

    last_log = max(dates)
    if last_log == today - timedelta(days=1) and today not in dates:
        click.echo("⚠️ Streak in danger! Log a session today to keep it alive!")
    elif last_log < today - timedelta(days=1):
        click.echo("❌ Your streak has already been broken.")



