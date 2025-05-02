#!/bin/bash

docker compose --file compose.test.yaml up --build -d > /dev/null

# grant the tests 10 seconds to run
sleep 10
docker compose down

# see the failed tests (if any)
cat /tmp/booktrack/testlog.txt

# get the coverage
tail -1 /tmp/booktrack/report.txt | awk '{print $NF}'
