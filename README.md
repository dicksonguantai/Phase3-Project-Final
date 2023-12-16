# Parliamentary Bill Tracking System

The **Parliamentary Bill Tracking System** is a command-line interface (CLI) application designed to manage parliamentary bills, members of parliament (MPs), and voting records within a simulated parliamentary environment.

## Features

- **Bill Management:** Add, update, and delete bills with relevant details (title, sponsor, status).
- **MP Management:** Comprehensive management of MPs including party affiliations and personal details.
- **Vote Tracking:** Record and track votes distinguishing between 'yes' and 'no' votes.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/parliamentary-bill-tracking.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd parliamentary-bill-tracking
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

- **Run the CLI interface:**

    ```bash
    python cli.py
    ```

- **Follow the CLI prompts and commands to manage bills, MPs, and votes.**

## Technologies Used

- Python
- SQLAlchemy
- Click (CLI Framework)
- Alembic (Database Migration)
- Faker (Fake Data Generation)
