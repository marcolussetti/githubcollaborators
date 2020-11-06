#!/usr/bin/env python3
# List all collaborators. Very basic script.

import requests


def fetch_repos(creds: (str, str), repos_type: str, page: int = 1, verbose: bool = False):
    if verbose:
        print(
            f"Fetching https://api.github.com/user/repos?per_page=100&page={page}&visibility={repos_type}")
    r = requests.get(
        f"https://api.github.com/user/repos?per_page=100&page={page}&visibility={repos_type}",
        auth=creds, timeout=5, headers={
            "User-Agent": "githubcollaborators"
        })
    if verbose:
        print(r)
    if r.status_code != 200:
        if verbose:
            print(f"Wrong status code on {r.url}: {r.status_code}")
    if len(r.json()) == 0:
        return []
    curr_results = r.json()
    if len(curr_results) == 100:
        return curr_results + fetch_repos(creds, repos_type, page + 1, verbose)
    else:
        return curr_results


def fetch_collaborators(creds: (str, str), collaborators_url: str, page: int = 1, verbose: bool = False):
    collaborators_url = collaborators_url.replace("{/collaborator}", "")
    if verbose:
        print(f"Fetching {collaborators_url}?per_page=100&page={page}")
    r = requests.get(
        f"{collaborators_url}?per_page=100&page={page}", auth=creds, timeout=5, headers={
            "User-Agent": "githubcollaborators"
        })
    if r.status_code != 200:
        if verbose:
            print(f"Wrong status code on {r.url}: {r.status_code}")
        return []
    if len(r.json()) == 0:
        return []
    curr_results = r.json()
    if len(curr_results) == 100:
        return curr_results + fetch_collaborators(creds, collaborators_url, page + 1, verbose)
    else:
        return curr_results


def process_repo(creds, repo, verbose: bool = False):
    return {
        "url": repo["html_url"],
        "collaborators": [c["login"] for c in fetch_collaborators(creds, repo["collaborators_url"], verbose=verbose)],
        "owner": repo["owner"]["login"],
        "owner_type": repo["owner"]["type"],
        "private": repo["private"],
        "watchers_count": repo["watchers_count"]
    }


def filter_repos_by_collaborators(repos):
    return [repo for repo in repos if len(repo["collaborators"]) > 1]


def githubcollaborators(username: str, token: str, repos_type: str = 'all', verbose: bool = False):
    creds = (username, token)

    repos = fetch_repos(creds, repos_type=repos_type, verbose=verbose)
    if verbose:
        print(f"Fetched {len(repos)} repositories.")
    processed_repos = [process_repo(
        creds, repo, verbose=verbose) for repo in repos]
    if verbose:
        print("Fetched collaborators.")
    repos_with_collaborators = filter_repos_by_collaborators(
        processed_repos)
    if verbose:
        print(
            f"Found {len(repos_with_collaborators)} repositories with collaborators.")

    return repos_with_collaborators
