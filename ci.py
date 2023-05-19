#!/usr/bin/env python3
"""
Check for CI config files in this repo, then open the CI webpages.

Works with origins in the form:
https://github.com/hugovk/ci-tools

Tip: add to your .zshrc or similar:
alias ci=ci.py
"""
import argparse
import os
from pathlib import Path

import git  # pip install GitPython


def check_pattern(pattern: str, thing: str) -> bool:
    if not pattern or pattern in thing:
        return True
    return False


def get_gitlab_url(origin_url: str) -> str:
    url = origin_url.split("@")[1].replace(":", "/")
    return "https://" + url


def do_ci(args: argparse.Namespace) -> None:
    # Find the user/repo of the Git origin
    git_repo = git.Repo(".")
    origin_url = list(git_repo.remotes.origin.urls)[0].removesuffix(".git")
    print(origin_url)
    user, repo = origin_url.rstrip("/").split("/")[-2:]
    print(user)
    print(repo)

    urls = []

    if check_pattern(args.pattern, "appveyor.yml") and (
        Path(".appveyor.yml").is_file() or Path("appveyor.yml").is_file()
    ):
        urls.append(f"https://ci.appveyor.com/project/{user}/{repo}")

    if check_pattern(args.pattern, ".travis.yml") and Path(".travis.yml").is_file():
        urls.append(f"https://app.travis-ci.com/github/{user}/{repo}")

    if (
        check_pattern(args.pattern, ".github/workflows/")
        and Path(".github/workflows/").is_dir()
    ):
        urls.append(f"https://github.com/{user}/{repo}/actions")

    if (
        check_pattern(args.pattern, ".gitlab-ci.yml")
        and Path(".gitlab-ci.yml").is_file()
    ):
        urls.append(get_gitlab_url(origin_url) + "/-/pipelines")

    if urls:
        # 'open 1 2 3' is faster than 3 x webbrowser.open_new_tab
        cmd = "open " + " ".join(urls)
        print(cmd)
        if not args.dry_run:
            os.system(cmd)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check for CI config files in this repo, "
        "then open the CI webpages.",
        # formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "pattern",
        nargs="?",
        help="Only open webpages for config matching this path (eg. github)",
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Show but don't open webpages",
    )
    args = parser.parse_args()
    do_ci(args)


if __name__ == "__main__":
    main()
