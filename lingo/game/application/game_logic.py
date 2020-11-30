"""
    This scripted is made as an Game Service a bridge between controller and domain
"""

# pylint: disable=import-error
from datetime import datetime
from lingo.game.domain.game import run_turn
from lingo.game.domain.round_type import RoundType
from lingo.game.port.file.word_repository import get_random_word
from lingo.game.port.data.round_repository import insert_round, update_end_round
from lingo.game.port.data.turn_repository import insert_turn, update_turn, get_turn_count
from lingo.game.port.data.game_repository import insert_game, get_game_round_information, \
    update_game_word_length, update_game_score, update_end_game, get_game_information


def create_game(user):
    """
    Creates a gamed based on user_id
    :param user: This user is the users id
    :return: returns the first letter and word length
    """
    # Basic information for starting a game
    game_type = RoundType.FiveCharacters.value

    # Create first round object
    random_word = choose_random_word(game_type)

    game_id = insert_game(int(user), 'NL', game_type)
    if game_id is not None:
        round_id = insert_round(game_id, random_word)

        if round_id is not None:
            insert_turn(round_id)

    return random_word[0], game_type


# TODO: add language as parameter
def choose_random_word(word_length):
    """
    Choose a random word based on word length
    :param word_length: length the word need to be
    :return: random word
    """
    return get_random_word(word_length)


def guess_turn(user_id, guessed_word):
    # pylint: disable=inconsistent-return-statements
    """
    Turn to guess the word
    :param user_id: id of user
    :param guessed_word: users guess
    :return: round type, word response, (validation error)
    """
    now = datetime.now().strftime("%Y-%b-%d %H:%M:%S.%f")

    if guessed_word is not None:
        game_details = get_game_round_information(user_id)

        # List of all the information
        game_id = game_details.get('game_id')
        round_id = game_details.get('round_id')

        # pylint: disable=line-too-long
        turn_response = run_turn(guessed_word, game_details.get('correct_word'),
                                 game_details.get('word_length'), game_details.get('turn_start_time'),
                                 now, get_turn_count(round_id), (game_details.get('game_language')).upper())
        # pylint: enable=line-too-long

        if turn_response[0].__eq__('correct'):
            # Update turn
            update_turn(guessed_word, round_id)
            # Change game length
            change_game_status(game_details.get('word_length'), game_id)
            # End the round
            update_end_round(round_id)
            # Update game score with +1
            update_game_score(game_id)

        elif turn_response[0].__eq__('next-round'):
            # Update turn
            update_turn(guessed_word, round_id)
            # Insert new turn
            insert_turn(round_id)

        elif turn_response[0].__eq__('validation-error'):
            # Update turn
            update_turn(guessed_word, round_id)
            # Insert new turn
            insert_turn(round_id)

        elif turn_response[0].__eq__('game-over'):
            update_end_round(round_id)
            update_end_game(game_id)
        else:
            return 'abort'

        if len(turn_response) == 3:
            return turn_response[0], turn_response[1], turn_response[2]

        return turn_response[0], turn_response[1]

    return 'abort'
    # pylint: enable=inconsistent-return-statements


def change_game_status(current_length, game_id):
    """
    Change the game status based on the current word_length
    :param current_length: current game length
    :param game_id: id of current game
    :return: new game length
    """
    new_length = None

    if current_length == 5:
        new_length = RoundType.SixCharacters.value
    elif current_length == 6:
        new_length = RoundType.SevenCharacters.value
    elif current_length == 7:
        new_length = RoundType.FiveCharacters.value

    update_game_word_length(game_id, new_length)


def create_round(user_id):
    """
    Create a new round
    :param user_id: id of user to make a new round for the user
    :return: first letter of new word and word lenth
    """
    game_details = get_game_information(user_id)

    word_length = game_details.get('word_length')
    game_id = game_details.get('game_id')

    random_word = choose_random_word(word_length)
    round_id = insert_round(game_id, random_word)

    if round_id is not None:
        insert_turn(round_id)

    return random_word[0], word_length # pylint: disable=inconsistent-return-statements
