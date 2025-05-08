#!/bin/bash

echo "Starting the containers..."
docker compose --file compose.test.yaml up --build -d &> /dev/null

# grant the tests 10 seconds to run
echo "Runnning the tests"
sleep 10

echo "Shutting down, prepare to see the logs..."
docker compose down -v --remove-orphans &> /dev/null

# see the failed tests (if any)
cat /tmp/booktrack/testlog.txt

# get the coverage
cat /tmp/booktrack/report.txt

coverage=$(tail -1 /tmp/booktrack/report.txt 2>/dev/null | awk '{print $NF}' | tr -d '%')
echo "Total coverage: ${coverage:-Unavailable}%"

if [ -n "$coverage" ] && [ "$(echo "$coverage < 60" | bc)" -eq 1 ]; then
  echo "Coverage $coverage% is too low!"
  exit 1
fi
