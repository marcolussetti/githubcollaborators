#!/usr/bin/env python3
# List all collaborators. Very basic script.

import logging
import sys

import requests

logger = None


def fetch_repos(creds: (str, str), repos_type: str, page: int = 1):
    logger.info(
        f"Fetching https://api.github.com/user/repos?per_page=100&page={page}&visibility={repos_type}")
    r = requests.get(
        f"https://api.github.com/user/repos?per_page=100&page={page}&visibility={repos_type}",
        auth=creds, timeout=5, headers={
            "User-Agent": "githubcollaborators"
        })
    if r.status_code != 200:
        logger.info(f"Wrong status code on {r.url}: {r.status_code}")
    if len(r.json()) == 0:
        return []
    curr_results = r.json()
    if len(curr_results) == 100:
        return curr_results + fetch_repos(creds, repos_type, page + 1)
    else:
        return curr_results


def fetch_collaborators(creds: (str, str), collaborators_url: str, page: int = 1):
    collaborators_url = collaborators_url.replace("{/collaborator}", "")
    logger.info(f"Fetching {collaborators_url}?per_page=100&page={page}")
    r = requests.get(
        f"{collaborators_url}?per_page=100&page={page}", auth=creds, timeout=5, headers={
            "User-Agent": "githubcollaborators"
        })
    if r.status_code != 200:
        logger.info(f"Wrong status code on {r.url}: {r.status_code}")
        return []
    if len(r.json()) == 0:
        return []
    curr_results = r.json()
    if len(curr_results) == 100:
        return curr_results + fetch_collaborators(creds, collaborators_url, page + 1)
    else:
        return curr_results


def process_repo(creds, repo):
    return {
        "url": repo["html_url"],
        "collaborators": [c["login"] for c in fetch_collaborators(creds, repo["collaborators_url"])],
        "owner": repo["owner"]["login"],
        "owner_type": repo["owner"]["type"],
        "private": repo["private"],
        "watchers_count": repo["watchers_count"]
    }


def filter_repos_by_collaborators(repos):
    return [repo for repo in repos if len(repo["collaborators"]) > 1]


def githubcollaborators(username: str, token: str, repos_type: str = 'all', logger_obj=None):
    creds = (username, token)

    # Clunky logging
    global logger
    if logger_obj is not None:
        logger = logger_obj
    else:
        logger = logging.getLogger("githubcollaborators")
        logger.setLevel(logging.ERROR)
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter("[%(levelname)s]: %(message)s"))
        logger.addHandler(handler)

    repos = fetch_repos(creds, repos_type=repos_type)
    logger.info(f"Fetched {len(repos)} repositories.")

    processed_repos = [process_repo(
        creds, repo) for repo in repos]
    logger.info("Fetched collaborators.")

    repos_with_collaborators = filter_repos_by_collaborators(
        processed_repos)
    logger.info(
        f"Found {len(repos_with_collaborators)} repositories with collaborators.")

    return repos_with_collaborators
