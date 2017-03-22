# HTWG syslab reviewer

[![build status](https://git.brn.li/htwg-syslab/syslab-reviewer/badges/master/build.svg)](https://git.brn.li/htwg-syslab/syslab-reviewer/commits/master)
[![coverage report](https://git.brn.li/htwg-syslab/syslab-reviewer/badges/master/coverage.svg)](https://git.brn.li/htwg-syslab/syslab-reviewer/commits/master)

## Config

Create a personal GitHub token at: https://github.com/settings/tokens

Required scopes:  [X] repo (Full control of private repositories) 

```
cp config/syslab-reviewer.sample.yml ~/.syslab-reviewer.yml
vim ~/.syslab-reviewer.yml # add github token
```

## Usage

```
python3 htwg/syslab/reviewer/main.py
```

This currently list all BSYS and SYSO groups with open pull requests.

Groups sorted by (oldest) pull request creation (asc).


## Development
### Install Requirements
```
pip3 install -r requirements.txt --upgrade
```

### Lint
```
./setup.py lint
```

### Test
```
./setup.py test
```
