import pgn2gif
import tweepy
from dotenv import dotenv_values
import urllib.request, urllib.error, json
import os
import time
from datetime import datetime
import pytz

# load environment variables
config = dotenv_values(".env")

# create tweepy client using environment variables
client = tweepy.Client(
    config['BEARER_TOKEN'],
    config['API_KEY'],
    config['API_KEY_SECRET'],
    config['ACCESS_TOKEN'],
    config['ACCESS_TOKEN_SECRET'],
)
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(config['API_KEY'], config['API_KEY_SECRET'])
auth.set_access_token(config['ACCESS_TOKEN'], config['ACCESS_TOKEN_SECRET'])
api = tweepy.API(auth)

users = []

# load users from json file
with open ('users.json', 'r') as file:
    users = json.load(file)['users']
    print(users)

newest_game_end_time = int(time.time()) # the initial time that we will use to check for new games
refresh_rate = 10 # how often to check for new games in seconds


# timestamped logging
def log(message):
    output = f"[{datetime.now(pytz.timezone('Europe/London')).strftime('%d/%m/%Y %H:%M:%S')}] {message}"
    print(output)


def get_recent_game(username):
    # get month and year
    now = datetime.now()
    month = now.strftime("%m")
    year = now.strftime("%Y")
    global newest_game_end_time
    try:
        with urllib.request.urlopen(f"https://api.chess.com/pub/player/{username}/games/{year}/{month}") as url:
            data = json.load(url)
            newest_game = data["games"][-1]
            if newest_game["end_time"] > newest_game_end_time:
                newest_game_end_time = newest_game["end_time"]
                return newest_game
            else:
                return False
    except Exception as err:
        log(f'Exception error: {err}')


def get_result(user, termination):
    way_of = termination.split("won ")[1]
    if termination.lower().find(user["chess_username"].lower()) != -1:
        return (user["twitter_username"] + " won " + way_of)
    else:
        return (user["twitter_username"] + " lost " + way_of)


def make_gif(reverse):
    creator = pgn2gif.PgnToGifCreator(reverse=reverse, duration=0.5)
    creator.create_gif("game.pgn", out_path="game.gif")
    media = api.media_upload("game.gif")
    log("Gif created.")
    return media.media_id


def make_tweet(result, media_id):
    try:
        response = client.create_tweet(text="Game over: " + result, media_ids=[media_id]);
        log("Tweeted.")
        log(response.data)
        return True;
    except Exception as err:
        log(f"Error tweeting: {err}")
        return False;


def new_game(game, user):
    reverse = False
    pgn = game["pgn"]
    with open ("game.pgn", "w") as f:
        f.write(pgn)
    sides = pgn[pgn.find("[White"):pgn.find("\n[Result")].split("\n")
    termination = pgn[pgn.find("[Termination \"")+len("[Termination \""):pgn.find("\"]\n[StartTime")]
    result = get_result(user, termination)
    time_control = game["time_class"]
    if sides[0].lower().find(user["chess_username"].lower()) == -1:
        reverse = True;
        new_rating = game["black"]["rating"]
    else:
        new_rating = game["white"]["rating"]
    media_id = make_gif(reverse)
    result = f"{result}, new {time_control} rating: {new_rating}."
    return result, media_id


def clean_up():
    os.remove("game.pgn")
    os.remove("game.gif")


def check_for_new_game():
    for user in users:
        game = get_recent_game(user["chess_username"])
        if game:
            log("New game found.")
            result, media_id = new_game(game, user)
            make_tweet(result, media_id)
            clean_up()
        else:
            log("No new game found.")
    time.sleep(refresh_rate)


def main():
    while True:
        check_for_new_game()


if __name__ == "__main__":
    main()