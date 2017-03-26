#!/usr/bin/env python
"""Grep the logs of each build job for a given Travis CI build

For example: python grep-travis-logs.py -p "tests in" -n 3928
For example: python grep-travis-logs.py -p "tests in" -n 3928.2
"""
from __future__ import print_function, unicode_literals
import argparse
import re


def split_build_number(number):
    """Split a float into build int and job int:
    Given 3928.2, return 3829 and 2
    Given 3928, return 3829 and None
    """
    # Use string to avoid 4393.2 -> 4393, 1 due to floating-point arithmetic
    build, job = str(number).split(".")
    build, job = int(build), int(job)
    if job == 0:
        job = None
    return build, job


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Grep logs of each build job for a Travis CI build",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-s', '--slug',
        default='python-pillow/Pillow',
        help="Repo slug")
    parser.add_argument(
        '-p', '--pattern',
        help="Pattern to find. Omit to print full log")
    parser.add_argument(
        '-n', '--number',
        type=float,
        help="Build number (and optional job number). Omit for latest build")
    parser.add_argument(
        '-q', '--quiet', action='store_true',
        default=False,
        help="Quiet means only print from logs, with no extra build info")
    args = parser.parse_args()

    build_no, job_no = split_build_number(args.number)

    # Slow to import, no need for --help
    from travispy import TravisPy  # pip install travispy

    t = TravisPy()
#     repo = t.repo(args.slug)

    build = t.builds(slug=args.slug, number=build_no)[0]

    job_ids = sorted(build.job_ids)

    for job_id in job_ids:
        job = t.job(job_id)

        if job_no:
            # Job number specified, only print that one
            if str(args.number) != job.number:
                continue

        if not args.quiet:
            print()
            print("#{}".format(job.number))
        log = t.log(job.log_id)
        if args.pattern:
            lines = log.body.splitlines()
            for line in lines:
                if re.search(args.pattern, line):
                    print(line)
        else:
            print(log.body.encode("utf-8"))

# End of file
