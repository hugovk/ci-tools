#!/usr/bin/env python
"""TODO

For example: python time-travis-logs.py -n 3928
"""
from __future__ import annotations

import argparse

import dateutil.parser as dp


def iso2epoch(timestamp):
    parsed_t = dp.parse(timestamp)
    t_in_seconds = parsed_t.strftime("%s")
    return int(t_in_seconds)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="TODO", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-s", "--slug", default="python-pillow/Pillow", help="Repo slug"
    )
    parser.add_argument(
        "-p", "--pattern", help="Pattern to find. Omit to print full log"
    )
    parser.add_argument(
        "-n", "--number", type=int, help="Build number. Omit for latest build"
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        default=False,
        help="Quiet means only print from logs, with no extra build info",
    )
    args = parser.parse_args()

    # Slow to import, no need for --help
    from travispy import TravisPy  # pip install travispy

    t = TravisPy()

    for number in range(args.number - 100, args.number):
        # print(number)

        build = t.builds(slug=args.slug, number=number)[0]

        # print(build['started_at'])
        # print(build['finished_at'])
        start_seconds = iso2epoch(build["started_at"])
        finish_seconds = iso2epoch(build["finished_at"])
        # print(start_seconds)
        # print(finish_seconds)
        seconds = finish_seconds - start_seconds
        # print(seconds)
        m, s = divmod(seconds, 60)
        print("%02dm%02ds\t%d" % (m, s, number))


#     job_ids = sorted(build.job_ids)
#
#     first_started_at = sys.maxint
#     last_ended_at = 0

#     for job_id in job_ids:
#         job = t.job(job_id)
#
#
#         pprint(job)
#         pprint(dir(job))
#         print(job["started_at"])
#         print(job["finished_at"])
#         if not first_started_at
#         end
#
#         if not args.quiet:
#             print()
#             print("#{}".format(job.number))
#         log = t.log(job.log_id)
#         if args.pattern:
#             lines = log.body.splitlines()
#             for line in lines:
#                 if args.pattern in line:
#                     print(line)
#         else:
#             print(log.body)


# End of file
