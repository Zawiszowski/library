# Init documentation

## To run app
    docker compose up

## To test 
    docker compose exec -it server /bin/bash -lc 'uv run -frozen pytest -o log_cli=true --log-cli-level=DEBUG tests'