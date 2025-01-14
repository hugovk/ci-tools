#!/usr/bin/env python3
"""
Check for CI config files in this repo, then open the CI webpages.

Works with origins in the form:
https://github.com/hugovk/ci-tools

Tip: add to your .zshrc or similar:
alias ci=ci.py
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path

import git  # pip install GitPython


def clean_url(url: str) -> str:
    # git@github.com:user/repo.git
    # ->
    # https://github.com/user/repo.git
    if url.startswith("git@"):
        url = "https://" + url.removeprefix("git@").replace(":", "/")

    # https://github.com/user/repo.git
    # ->
    # https://github.com:user/repo
    url = url.removesuffix(".git")

    return url


def check_pattern(pattern: str, thing: str) -> bool:
    if not pattern or pattern in thing:
        return True
    return False


def get_gitlab_url(origin_url: str) -> str | None:
    if "gitlab" not in origin_url:
        return None
    url = origin_url.split("@")[1].replace(":", "/")
    return "https://" + url


def do_ci(args: argparse.Namespace) -> None:
    # Find the user/repo of the Git origin
    repo_dir = Path(".").resolve()
    while True:
        try:
            git_repo = git.Repo(repo_dir)
            break
        except git.exc.InvalidGitRepositoryError:
            if repo_dir == Path("/"):
                print("Not in a Git repo")
                raise
            repo_dir = repo_dir.parent

    origin_url = list(git_repo.remotes.origin.urls)[0]
    origin_url = clean_url(origin_url)
    print(origin_url)
    user, repo = origin_url.rstrip("/").split("/")[-2:]
    print(user)
    print(repo)

    urls = []

    if check_pattern(args.pattern, "appveyor.yml") and (
        Path(repo_dir / ".appveyor.yml").is_file()
        or Path(repo_dir / "appveyor.yml").is_file()
    ):
        urls.append(f"https://ci.appveyor.com/project/{user}/{repo}")

    if (
        check_pattern(args.pattern, ".travis.yml")
        and Path(repo_dir / ".travis.yml").is_file()
    ):
        urls.append(f"https://app.travis-ci.com/github/{user}/{repo}")

    if (
        check_pattern(args.pattern, ".github/workflows/")
        and Path(repo_dir / ".github/workflows/").is_dir()
    ):
        urls.append(f"https://github.com/{user}/{repo}/actions")

    if (
        check_pattern(args.pattern, ".gitlab-ci.yml")
        and Path(repo_dir / ".gitlab-ci.yml").is_file()
    ):
        url = get_gitlab_url(origin_url)
        if url:
            urls.append(url + "/-/pipelines")

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
