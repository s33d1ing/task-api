# Task API

A modular Flask API for managing tasks, featuring full test coverage, Docker support, and automated CI/CD.

## Quick Start

### Prerequisites

- Python 3.9+
- Docker (optional)

### Local Installation

1. Clone the repo:
   `git clone https://github.com/s33d1ing/task-api.git && cd task-api`

2. Install dependencies:
   `pip install -e ".[dev]"`

3. Run tests:
   `pytest`

4. Start the server:
   `flask run`

   Access at <http://localhost:5000>

### Docker Installation

Run the following command:
`docker-compose up --build`

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | /api/tasks | List all tasks |
| GET | /api/tasks/{id} | Get a specific task |
| POST | /api/tasks | Create a task |
| PUT | /api/tasks/{id} | Update a task |
| DELETE | /api/tasks/{id} | Delete a task |

**Example Request:**
`curl -X POST http://localhost:5000/api/tasks -H "Content-Type: application/json" -d '{"title": "Buy milk"}'`

## Testing & Quality

This project uses pytest, black, flake8, and mypy for quality assurance.

- Run all checks: `make check`
- Run tests: `make test`
- Format code: `make format`
- Lint code: `make lint`

## Architecture

- **app/main.py**: Flask routes and API logic.
- **app/models.py**: Data management (TaskManager class).
- **tests/**: Comprehensive unit and integration tests.

## Docker Commands

- Run app: `docker-compose up`
- Run tests: `docker-compose run --rm test`
- Shell access: `docker-compose exec app /bin/bash`

## Contributing

1. Fork the repo.
2. Create a branch (`git checkout -b feature/name`).
3. Commit changes (hooks run automatically).
4. Push and open a Pull Request.

## License

MIT License.
