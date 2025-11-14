# Init documentation

## Create env from template:
    cp backend/.env.template backend/.env

## Configure your .env
    add your SECRET_KEY, POSTGRES_USER and POSTGRES_PASSWORD

## To run app
    docker compose up

## To test 
    docker compose exec -it server /bin/bash -lc 'uv run -frozen pytest -o log_cli=true --log-cli-level=DEBUG tests'