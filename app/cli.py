import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Base, MP, Bill, Vote
from sqlalchemy.orm import joinedload
from collections import Counter

# Create an SQLAlchemy engine
engine = create_engine('sqlite:///parliamentary_bill_tracker.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Helper function for sorting bills by vote count
def sort_bills_by_vote_count(bills):
    # Sort bills by the number of 'yes' votes in descending order
    sorted_bills = sorted(bills, key=lambda bill: sum(1 for vote in bill.votes if vote.vote_status), reverse=True)
    return sorted_bills


# Helper function for searching MP by name
def search_mp_by_name(name):
    session = Session()
    mps = session.query(MP).filter(MP.name.ilike(f"%{name}%")).all()
    session.close()
    return mps

@click.group()
def cli():
    pass

@cli.command()
@click.option('--name', prompt='MP Name', help='Name of the MP')
def add_mp(name):
    session = Session()
    new_mp = MP(name=name)
    session.add(new_mp)
    session.commit()
    session.close()
    click.echo(f"Added MP: {name}")

@cli.command()
@click.option('--title', prompt='Bill Title', help='Title of the Bill')
@click.option('--sponsor-id', prompt='Sponsor ID', type=int, help='ID of the sponsoring MP')
def add_bill(title, sponsor_id):
    session = Session()
    mp = session.query(MP).filter(MP.id == sponsor_id).first()
    if mp:
        new_bill = Bill(title=title, sponsor_id=sponsor_id)
        session.add(new_bill)
        session.commit()
        click.echo(f"Added Bill: {title} (Sponsor: {mp.name})")
    else:
        click.echo("MP(s) not found.")
    
    session.close()

@cli.command()
@click.option('--mp-id', prompt='MP ID', type=int, help='ID of the MP')
@click.option('--bill-id', prompt='Bill ID', type=int, help='ID of the Bill')
@click.option('--vote-status', prompt='Vote Status', type=bool, help='Vote status: True for yes, False for no')
def add_vote(mp_id, bill_id, vote_status):
    session = Session()
    mp = session.query(MP).filter(MP.id == mp_id).first()
    bill = session.query(Bill).filter(Bill.id == bill_id).first()
    if mp and bill:
        new_vote = Vote(mp_id=mp_id, bill_id=bill_id, vote_status=vote_status)
        session.add(new_vote)
        session.commit()
        session.close()
        click.echo(f"Vote recorded: MP ID {mp_id} voted {'Yes' if vote_status else 'No'} on Bill ID {bill_id}")
    else:
        click.echo("MP or Bill not found.")

@cli.command()
@click.option('--name', prompt='Search MP by Name', help='Name of the MP to search')
def search_mp(name):
    mps = search_mp_by_name(name)
    if mps:
        click.echo(f"MPs found with name '{name}':")
        for mp in mps:
            click.echo(f"- ID: {mp.id}, Name: {mp.name}")
    else:
        click.echo(f"No MPs found with name '{name}'.")


@cli.command()
@click.option('--sort-by-votes', is_flag=True, help='Sort bills by vote count')
def list_bills(sort_by_votes):
    session = Session()
    query = session.query(Bill).options(joinedload(Bill.sponsor), joinedload(Bill.votes))

    bills = query.all()

    if sort_by_votes:
        bills = sort_bills_by_vote_count(bills)

    click.echo("Bills:")
    for bill in bills:
        sponsor_name = bill.sponsor.name if hasattr(bill.sponsor, 'name') else "No sponsor"  # Check for sponsor existence
        vote_counts = Counter([vote.vote_status for vote in bill.votes])
        yes_count = vote_counts[True] if True in vote_counts else 0
        no_count = vote_counts[False] if False in vote_counts else 0

        click.echo(f"- ID: {bill.id}, Title: {bill.title}, Sponsor: {sponsor_name}, Yes Votes: {yes_count}, No Votes:{no_count}")

    session.close()


if __name__ == '__main__':
    cli()
