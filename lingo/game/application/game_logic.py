import random

from flask import make_response, jsonify

from lingo.game.domain.game import Game
from lingo.game.domain.round_type import RoundType
from lingo.game.domain.round_data import GameRound
from lingo.game.application.validation import *
from lingo.game.port.data.game_repository import insert_game, insert_round, insert_turn

calls = {"pipo": "14:34:57"}

games = []

some_length = 0
correct_word = ""


def create_game(user_id):
    # TODO: create function that gets the latest game_id

    # Basic information for starting a game
    game_type = RoundType.FiveCharacters.value

    # Create first round object
    random_word = choose_random_word(game_type)

    game_id = insert_game(user_id, 'NL', game_type)
    if game_id is not None:
        rounds_id = insert_round(game_id, random_word)
        if rounds_id is not None:
            if insert_turn(rounds_id):
                return True
    else:
        return False


def choose_random_word(word_length):
    random_word = ""

    with open('assets/filtered_dictionaries/NL.txt', 'r') as words:
        filter_words = words.read().splitlines()
        while not len(random_word) == word_length:
            random_word = random.choice(filter_words).upper()

    return random_word


def guess_turn(guess, time, word_length):
    # TODO: Check if word is NULL

    # TODO: Maybe make a function that is called validates and that runs all validations
    validate_word_length(guess, word_length)
    validate_only_alphabetic(guess)
    validate_time(time)

    # Change word to lower
    guess = guess.lower()
    validate_word(guess)

    # If everything is correct do the following:
    # Change word to CAPS
    guess = guess.upper()
    word_response = []
    for iteration, char in enumerate(guess):
        if char in correct_word:
            if correct_word[iteration].__eq__(char):
                word_response.append(char + " correct")
            else:
                word_response.append(char + " present")
        else:
            word_response.append(char + " absent")

    return print(word_response)

    # TODO: check if total word is correct if so add a point


def all_games():
    games_info = [{"game_id": g.game_id,
                   "score": g.score,
                   "game_type": g.game_type.value,
                   "rounds": [{"word": r.word, "turns": r.turn, "correct": r.correct} for r in g.rounds]
                   }
                  for g in games]

    return make_response(jsonify(games_info), 200)
