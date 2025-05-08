#!/bin/bash

testlog=unit-tests-report.txt

# Run tests and store the output in a log file
pytest --cov=src ./unit-tests -p no:warnings > $testlog

# Check if there are any test failures
if grep -q "FAILED" $testlog; then
    echo "Some of the tests have failed! Heads up!"
    exit 1
fi

echo "===== COVERAGE ====="

# Extract the coverage percentage from the "TOTAL" line
coverage=$(grep -oP 'TOTAL\s+\d+\s+\d+\s+\K\d+' $testlog)

# Print the extracted coverage percentage
echo "Total coverage: ${coverage:-Unavailable}%"

# Check if the coverage is less than 65%
echo "If smaller than 65% - too bad."
if [ -n "$coverage" ] && [ "$(echo "$coverage < 65" | bc)" -eq 1 ]; then
    echo "Coverage $coverage% is too low!"
    exit 1
fi

echo "Wow! Coverage is higher than 65%, congrats!"
