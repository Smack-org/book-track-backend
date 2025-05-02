import coverage
import sys
import subprocess

_cov = None


def start_cov():
    global _cov
    print("Initiating coverage collector...", file=sys.stderr)
    _cov = coverage.coverage(data_file="/app/coverage/.coverage", source=["src"])
    _cov.start()


def stop_cov():
    if _cov:
        print("Flushing coverage before shutdown!", file=sys.stderr)
        _cov.stop()
        _cov.save()

        print("Flushing coverage report!")
        try:
            # Create coverage report, calling coverage module in separate process.
            # Why not doing it outside the container? Because of path mapping issue.
            # Everything in .coverage database is calculated against docker internal paths.
            # On the host, rootfs is different, paths locations are different, thus we better
            # generate the report in there, inside this container, and analyse it outside.
            subprocess.run(
                [
                    "poetry", "run", "coverage", "report",
                    "--data-file=/app/coverage/.coverage"
                ],
                stdout=open('/app/coverage/report.txt', 'w'),
                stderr=subprocess.PIPE,
                check=True
            )
            print("Coverage report generated and saved to /app/coverage/report.txt")
        except subprocess.CalledProcessError as e:
            print(f"Error running coverage report: {e}", file=sys.stderr)
