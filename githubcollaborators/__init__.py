#!/usr/bin/env python3
# List all collaborators. Very basic script.

import requests


def fetch_repos(creds: (str, str), page: int = 1):
    r = requests.get(
        f"https://api.github.com/user/repos?per_page=100&page={page}&visibility=all", auth=creds)
    if r.status_code != 200:
        print(f"Wrong status code on {r.url}: {r.status_code}")
    if len(r.json()) == 0:
        return []
    curr_results = r.json()
    if len(curr_results) == 100:
        return curr_results + fetch_repos(creds, page + 1)
    else:
        return curr_results


def fetch_collaborators(creds: (str, str), collaborators_url: str, page: int = 1):
    collaborators_url = collaborators_url.replace("{/collaborator}", "")
    r = requests.get(
        f"{collaborators_url}?per_page=100&page={page}", auth=creds)
    if r.status_code != 200:
        # print(f"Wrong status code on {r.url}: {r.status_code}")
        if r.status_code == 403:
            return []
        return []
    # print(f"{user}: {len(r.json())} {list_type}. page {page}")
    if len(r.json()) == 0:
        return []
    curr_results = r.json()
    if len(curr_results) == 100:
        return curr_results + fetch_collaborators(creds, collaborators_url, page + 1)
    else:
        return curr_results


def process_repo(repo):
    return {
        "url": repo["html_url"],
        "collaborators": [c["login"] for c in fetch_collaborators(repo["collaborators_url"])],
        "owner": repo["owner"]["login"],
        "owner_type": repo["owner"]["type"],
        "private": repo["private"],
        "watchers_count": repo["watchers_count"]
    }


def filter_repos_by_collaborators(repos):
    return [repo for repo in repos if len(repo["collaborators"]) > 1]


def githubcollaborators(username: str, token: str):
    creds = (username, token)

    repos = fetch_repos(creds)
    processed_repos = [process_repo(repo) for repo in repos]
    repos_with_collaborators = filter_repos_by_collaborators(
        creds, processed_repos)

    return repos_with_collaborators
