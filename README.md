# githubcollaborators

This is a very simple tool. It takes a GitHub username & Personal Access Token,
and returns a JSON with the collaborators on the user's GitHub repos, where
there are collaborators.


## Personal Access Token

Should be generated from https://github.com/settings/tokens

Requires the following permissions:
- repo ("Full control of private repositories")
- admin:org -> read:org ("Read or and team membership, read org projects")
- user -> read:user ("Read all user profile data")


## Standalone

```bash
pip install githubcollaborators
githubcollaborators -u <your-github-username> -t <github-personal-access-token>
```

## As a library

```python
from githubcollaborators import githubcollaborators

print(githubcollaborators(<your_username>, <your_personal_access_token>))
```
