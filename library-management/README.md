# Library Management System (LMS)

A small Flask REST API for tracking books, members, and loans. Data is stored
**in memory** (plain Python objects, no database) and is reset every time the
app restarts — this project is meant to run before you've covered databases.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

The API runs at `http://127.0.0.1:5000`.

## Web UI

Open `http://127.0.0.1:5000/` in a browser for a basic HTML front end (plain
forms and tables, no JavaScript) to add/delete books and members, and check
books in/out:

| Page | Path |
|---|---|
| Home | `/` |
| Books | `/ui/books` |
| Members | `/ui/members` |
| Loans | `/ui/loans` |

This UI is separate from the JSON API below — it's there so you can see the
app working without a REST client, and calls the same in-memory store.

## Entities

- **Book**: `id, title, author, isbn, total_copies, available_copies`
- **Member**: `id, name, email, membership_date`
- **Loan**: `id, book_id, member_id, loan_date, due_date, return_date`

## JSON API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/books` | List all books |
| POST | `/books` | Create a book |
| GET | `/books/<id>` | Get one book |
| PUT | `/books/<id>` | Update a book |
| DELETE | `/books/<id>` | Delete a book |
| GET | `/members` | List all members |
| POST | `/members` | Create a member |
| GET | `/members/<id>` | Get one member |
| PUT | `/members/<id>` | Update a member |
| DELETE | `/members/<id>` | Delete a member |
| POST | `/loans` | Check out a book (`book_id`, `member_id`) |
| PUT | `/loans/<id>/return` | Return a loaned book |
| GET | `/loans?member_id=&book_id=` | Look up loans |

## Tests

Uses pytest and playwright for end to end testing

Install play wright and chromium
```bash
pip install pytest-playwright
python -m playwright install chromium
```
Run tests
```bash
python -m pytest
```
Run end to end test with visable browser:

```bash
python -m pytest tests/e2e -v --headed
```


## Docker

Build Docker image from project folder
```bash
docker build -t cisc327-a4 .
```

Run Docker container

```bash
docker run --rm -p 5000:5000 cisc327-a4
```

The application runs on port 5000 at http://localhost:5000. Flask binds to 0.0.0.0 so the service remains accessible outside the container.

Press Ctrl+C in the active terminal to stop the container. Because the --rm flag is set, the container is removed automatically once it stops.

## End to End test with Docker
Run the docker conatiner and close any other local runs of the program
```bash
docker run --rm -p 5000:5000 cisc327-a4
```

Open another terminal run:
```bash
python -m pytest tests/e2e -v --headed
```

The tests access the application at http://127.0.0.1:5000

## Docker Hub Repository
```bash
https://hub.docker.com/r/bluegamer18/cisc327_a4_library/tags
```

Download the image:

```bash
docker pull bluegamer18/cisc327_a4_library:latest
```

Run the downloaded image:

```bash
docker run --rm -p 5000:5000 cisc327-a4
```

Note that in memory data does not save after the application is closed