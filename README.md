# chess-twitter-bot
Post tweets when new chess.com games are played from a specified account

## Dependencies
* You need [python 3.5](https://www.python.org/downloads/) or newer installed.
- [pgn2gif](#pgn2gif)

## Installation
## Clone the repo
```
git clone https://github.com/laurence-dorman/chess-twitter-bot.git
```
## Activate new python virtual environment (recommended)
* Create a new virtual environment
```
python -m venv my_venv
```
* Activate on Linux:
```
source ./my_venv/bin/activate
```
* Activate on Windows:
```
.\my_venv\Scripts\activate
```
### Install dependencies
### pgn2gif
* Clone the repo 
```
git clone https://github.com/dn1z/pgn2gif
```
* Install dependencies for pgn2gif
```
cd pgn2gif \
pip3 install -r requirements.txt
```
* Run setup.py to install pgn2gif
```
python setup.py install
```
* Install dependencies for chess-twitter-bot
```
cd .. \
pip3 install -r requirements.txt
```
## Usage
* Modify the provided .env file with required keys and tokens from your [twitter project app](https://developer.twitter.com/en/portal/dashboard)

* Modify users.json file with the chess.com users you want to track, along with the twitter account you want to tag or just a name if you don't want to tag anyone

* Run
```
python script.py
```
## License
Copyright (c) L. Dorman. All rights reserved.

Licensed under the MIT license.
