#!/usr/bin/env python
"""Grep the logs of each build job for a given Travis CI build

For example: python grep-travis-logs.py -p "tests in" -n 3928
"""
from __future__ import print_function, unicode_literals
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Grep logs of each build job for a Travis CI build",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-s', '--slug',
        default= 'python-pillow/Pillow',
        help="Repo slug")
    parser.add_argument(
        '-p', '--pattern',
        help="Pattern to find. Omit to print full log")
    parser.add_argument(
        '-n', '--number',
        type=int,
        help="Build number. Omit for latest build")
    parser.add_argument(
        '-q', '--quiet', action='store_true',
        default=False,
        help="Quiet means only print from logs, with no extra build info")
    args = parser.parse_args()

    # Slow to import, no need for --help
    from travispy import TravisPy  # pip install travispy

    t = TravisPy()
#     repo = t.repo(args.slug)

    args.number=None
    build = t.builds(slug=args.slug, number=args.number)[0]

    job_ids = sorted(build.job_ids)

    for job_id in job_ids:
        job = t.job(job_id)
        if not args.quiet:
            print()
            print("#{}".format(job.number))
        log = t.log(job.log_id)
        if args.pattern:
            lines = log.body.splitlines()
            for line in lines:
                if args.pattern in line:
                    print(line)
        else:
            print(log.body)


# End of file
