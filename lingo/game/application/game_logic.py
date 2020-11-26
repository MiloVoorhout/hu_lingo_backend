import random

from flask import make_response, jsonify
from lingo.game.domain.round_type import RoundType
from lingo.game.application.validation import *
from lingo.game.port.data.game_repository import insert_game, get_game_round_information, update_game_word_length, \
    update_game_score, update_end_game, get_game_information

# TODO: Return first letter of word
from lingo.game.port.data.round_repository import insert_round, update_end_round
from lingo.game.port.data.turn_repository import insert_turn, update_turn, get_turn_count


def create_game(user_id):
    # Basic information for starting a game
    game_type = RoundType.FiveCharacters.value

    # Create first round object
    random_word = choose_random_word(game_type)

    game_id = insert_game(user_id, 'NL', game_type)
    if game_id is not None:
        round_id = insert_round(game_id, random_word)
        print(str(round_id))
        print(random_word[0])
        if round_id is not None:
            insert_turn(round_id)
            return random_word[0]


def choose_random_word(word_length):
    random_word = ""

    with open('assets/filtered_dictionaries/NL.txt', 'r') as words:
        filter_words = words.read().splitlines()
        while not len(random_word) == word_length:
            random_word = random.choice(filter_words).upper()

    return random_word


def guess_turn(user_id, guessed_word):
    # Get time of guess
    now = datetime.now().strftime("%Y-%b-%d %H:%M:%S.%f")

    # Get game data from database
    game_details = get_game_round_information(user_id)
    word_length = game_details.get('word_length')
    round_id = game_details.get('round_id')
    game_id = game_details.get('game_id')

    # List that eventually will be returned
    word_response = []

    # TODO: Check if word is NULL
    if guessed_word is not None:
        correct_word = game_details.get('correct_word')

        validation_status = run_all_turn_validations(guessed_word.upper(),
                                                     word_length,
                                                     round_id,
                                                     now)

        if not validation_status[0]:
            # TODO: Maybe make a function that is called validates and that runs all validations

            # If everything is correct do the following:
            # Change word to CAPS
            guess = guessed_word.upper()
            for iteration, char in enumerate(guess):
                if char in correct_word:
                    if correct_word[iteration].__eq__(char):
                        word_response.append(char + " correct")
                    else:
                        word_response.append(char + " present")
                else:
                    word_response.append(char + " absent")

            # TODO: Do something when word correct
            if correct_word.__eq__(guess):
                # Update turn
                update_turn(guess, round_id)

                # Change game length
                game_length = change_game_status(word_length, game_id)

                # End the round
                update_end_round(round_id)

                # Update game score with +1
                update_game_score(game_id)

                word_guess = 'correct'

                return word_response, word_guess
            else:
                update_turn(guess, round_id)
                word_guess = 'next-round'

            # TODO: check if total word is correct if so add a point

        else:

            # TODO: create good error handling for validation errors
            for iteration, char in enumerate(guessed_word):
                word_response.append(char + " invalid")
            update_turn(guessed_word.upper(), round_id)
            word_guess = 'next-round'
    else:
        users_input = 'NONE'
        update_turn(users_input, round_id)
        word_guess = 'next-round'

    # TODO: do something when 5 guesses where committed
    turn_count = get_turn_count(round_id)
    if turn_count >= 5:
        word_guess = 'game-over'
        update_end_round(round_id)
        update_end_game(game_id)
        return word_response, word_guess
    else:
        insert_turn(round_id)
        return word_response, word_guess


def change_game_status(current_length, game_id):
    new_length = None

    if current_length == 5:
        new_length = RoundType.SixCharacters.value
    elif current_length == 6:
        new_length = RoundType.SevenCharacters.value
    elif current_length == 7:
        new_length = RoundType.FiveCharacters.value

    update_game_word_length(game_id, new_length)

    return new_length


def create_round(user_id):
    game_details = get_game_information(user_id)

    word_length = game_details.get('word_length')
    game_id = game_details.get('game_id')

    random_word = choose_random_word(word_length)

    round_id = insert_round(game_id, random_word)

    if round_id is not None:
        insert_turn(round_id)
        return random_word[0]


def all_games():
    # games_info = [{"game_id": g.game_id,
    #                "score": g.score,
    #                "game_type": g.game_type.value,
    #                "rounds": [{"word": r.word, "turns": r.turn, "correct": r.correct} for r in g.rounds]
    #                }
    #               for g in games]
    games_info = "hello"

    return make_response(jsonify(games_info), 200)
