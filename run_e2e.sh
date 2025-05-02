#!/bin/bash

docker compose --file compose.test.yaml up --build -d

# grant the tests 10 seconds to run
sleep 10
docker compose down

# see the failed tests (if any)
cat /tmp/booktrack/testlog.txt

# get the coverage
tail -1 /tmp/booktrack/report.txt | awk '{print $NF}'


coverage=$(tail -1 /tmp/booktrack/report.txt 2>/dev/null | awk '{print $NF}' | tr -d '%')
echo "Total coverage: ${coverage:-Unavailable}%"

if [ -n "$coverage" ] && [ "$(echo "$coverage < 60" | bc)" -eq 1 ]; then
  echo "Coverage $coverage% is too low!"
  exit 1
fi
