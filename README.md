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
githubcollaborators -u <your-github-username> -t <github-personal-access-token> -o output.json
```

Full options:
```
usage: githubcollaborators [-h] -u USERNAME [-t TOKEN] [-v VISIBILITY]
                           [-o OUTPUT] [--verbose]

List collaborators for all repositories for the given user. Might take a while
to run, be patient.

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        GitHub username
  -t TOKEN, --token TOKEN
                        Personal Access Token for the specified GitHub
                        username. Requires following permissions: repo("Full
                        control of private repositories"), admin: org -> read:
                        org("Read or and team membership, read org projects"),
                        user -> read: user("Read all user profile data")
  -v VISIBILITY, --visibility VISIBILITY
                        Visibility level of the repositories, can be: all,
                        public, or private
  -o OUTPUT, --output OUTPUT
                        Save to specified output file
  --verbose             Set logging level to INFO
```

## As a library

```python
from githubcollaborators import githubcollaborators

print(githubcollaborators(<your_username>, <your_personal_access_token>))
```
