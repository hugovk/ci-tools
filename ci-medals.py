#!/usr/bin/env python3
"""
Award medals for CIs based on time to support a new Python release

https://twitter.com/hugovk/status/1321536957965574151
"""
from __future__ import annotations

import argparse
import datetime as dt
from pprint import pprint  # noqa: F401

import humanize  # pip3 install humanize


def released(date_string: str) -> dt.datetime:
    """Convert YYYY-MM-DD HH:MM to dt.datetime"""
    return dt.datetime.strptime(date_string, "%Y-%m-%d %H:%M")


# Useful for testing when they're not yet released
today = dt.datetime.today()

releases = {
    "3.8": {
        "python_release": released("2019-10-14 23:15"),
        "ci_releases": {
            # https://github.com/appveyor/ci/issues/3142
            "AppVeyor": released("2019-11-09 03:15"),
            # https://github.com/microsoft/azure-pipelines-image-generation/issues/1317
            "Azure Pipelines": released("2019-11-08 21:45"),
            # https://github.com/actions/setup-python/issues/30
            "GitHub Actions": released("2019-11-04 21:46"),
            # https://travis-ci.community/t/add-python-3-8-support/5463
            "Travis CI": released("2019-10-15 20:49"),
        },
    },
    "3.9": {
        "python_release": released("2020-10-05 20:01"),
        "ci_releases": {
            # https://github.com/appveyor/ci/issues/3541
            "AppVeyor": released("2020-10-27 02:15"),
            # https://github.com/actions/virtual-environments/issues/1740
            "Azure Pipelines": released("2020-10-28 12:44"),
            # https://github.com/actions/setup-python/issues/148
            "GitHub Actions": released("2020-10-06 13:58"),
            # https://travis-ci.community/t/python-3-9-0-build/10091
            "Travis CI": released("2020-10-26 19:58"),
        },
    },
    "3.10": {
        "python_release": released("2021-10-04 20:00"),
        "ci_releases": {
            # https://github.com/appveyor/ci/issues/3741
            "AppVeyor": released("2021-11-02 17:53"),
            # https://github.com/actions/virtual-environments/issues/4226
            "Azure Pipelines": released("2021-10-22 17:53"),
            # https://github.com/actions/setup-python/issues/249
            "GitHub Actions": released("2021-10-05 08:20"),
            # https://travis-ci.community/t/add-python-3-10/12220
            "Travis CI": released("2022-01-19 09:33"),
        },
    },
    "3.11": {
        "python_release": released("2022-10-24 19:48"),
        "ci_releases": {
            # https://github.com/appveyor/ci/issues/3844
            "AppVeyor": released("2022-11-07 20:57"),
            # https://github.com/actions/runner-images/issues/6459
            "Azure Pipelines": released("2022-10-26 20:00"),
            # https://github.com/actions/setup-python/issues/531#issuecomment-1291855440
            "GitHub Actions": released("2022-10-26 10:57"),
            # https://travis-ci.community/t/please-add-image-for-python-3-11/13384/3?u=hugovk
            "Travis CI": released("2022-11-22 5:11"),
        },
    },
    "3.12": {
        "python_release": released("2023-10-02 19:48"),
        "ci_releases": {
            # https://github.com/appveyor/ci/issues/3879
            "AppVeyor": today,
            # https://github.com/actions/setup-python/issues/736
            # https://github.com/actions/python-versions/releases/tag/3.12.0-6381888192
            "GitHub Actions": released("2023-10-03 09:22"),
            # https://github.com/actions/python-versions/releases/tag/3.12.0-6381888192
            "Azure Pipelines": released("2023-10-03 09:22"),
            # https://travis-ci.community/t/add-python-3-12/14006?u=hugovk
            "Travis CI": released("2023-10-23 12:45"),
        },
    },
}


def get_medals(ci_dates: list[tuple[str, dt.datetime]]) -> dict[str, int]:
    # Initialise medal counter
    medal = 0

    # Create a dictionary to store the medals and assign gold
    medals = {ci_dates[0][0]: medal}

    # Assign medals based on the sorted order, with shared medals for the same time
    for i, ci in enumerate(ci_dates):
        if i == 0:
            continue
        medal += 1
        previous_ci = ci_dates[i - 1]
        if ci[1] == previous_ci[1]:
            medals[ci[0]] = medals[previous_ci[0]]
        else:
            medals[ci[0]] = medal

    return medals


def get_medal(i: int) -> str:
    if i == 0:
        return "🥇"
    if i == 1:
        return "🥈"
    if i == 2:
        return "🥉"
    # 4️⃣...
    return f"{i+1}" + chr(0xFE0F) + chr(0x20E3) + "    "


def get_delta(value: dt.datetime, python_release: dt.datetime) -> str:
    return humanize.naturaldelta(value - python_release, months=False)


def get_name(name: str, twitter: bool) -> str:
    if not twitter:
        return name

    if name == "AppVeyor":
        return "@AppVeyor"
    if name == "Azure Pipelines":
        return "@AzureDevOps Pipelines"
    if name == "GitHub Actions":
        return "@GitHub Actions"
    if name == "Travis CI":
        return "@TravisCI"
    return name


def get_arrow(last_standing: list, ci_name: str, new_position: int) -> str:
    if not last_standing:
        return ""

    if ci_name not in last_standing:
        return "*️⃣"

    change = last_standing.index(ci_name) - new_position
    if change > 0:
        return "⬆️"
    if change < 0:
        return "⬇️"
    return "↔️"


def do_year(
    last_standing: list, version: str, data: dict, twitter: bool = False
) -> list:
    new_standing = []

    python_release = data["python_release"]
    ci_releases = data["ci_releases"]

    print(f"{python_release.year}: Python {version}\n")

    sorted_by_date = sorted(
        ci_releases.items(), key=lambda ci_date: ci_date[1] - python_release
    )

    medals = get_medals(sorted_by_date)

    for i, (ci, value) in enumerate(sorted_by_date):
        medal = get_medal(medals[ci])
        delta = get_delta(value, python_release)
        name = get_name(ci, twitter)
        arrow = get_arrow(last_standing, ci, i)
        print(f"{medal:<4}{delta}: {name} {arrow}")
        new_standing.append(ci)

    print()
    return new_standing


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-t", "--twitter", action="store_true", help="Use Twitter usernames"
    )
    args = parser.parse_args()

    last_standing = []

    for version, value in releases.items():
        last_standing = do_year(last_standing, version, value, args.twitter)


if __name__ == "__main__":
    main()


# End of file
