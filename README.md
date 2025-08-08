# automated-credit-card-tracking

## Running tests
- `cd api && pipenv run coverage run -m pytest tests -vv`
- `pipenv run coverage report --omit "tests/*,tests/**/*,*/prompts.py"`

## Docker
`docker compose build --no-cache`
`docker compose up -d`
`docker compose down`
