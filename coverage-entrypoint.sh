#!/bin/bash

poetry run coverage run --concurrency greenlet --branch --source=src --data-file=coverage/.coverage -m uvicorn src.main:app --host 0.0.0.0 --port 8000

# Create coverage report, calling coverage module in separate process.
# Why not doing it outside the container? Because of path mapping issue.
# Everything in .coverage database is calculated against docker internal paths.
# On the host, rootfs is different, paths locations are different, thus we better
# generate the report in there, inside this container, and analyse it outside.
poetry run coverage report --data-file=/app/coverage/.coverage > coverage/report.txt
poetry run coverage html --directory=/app/coverage/html --data-file=/app/coverage/.coverage
