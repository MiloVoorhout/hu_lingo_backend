"""
    This scripted is made as an Game Service a bridge between controller and domain
"""

# pylint: disable=import-error
from datetime import datetime
from openapi_server.core.domain.game.game import run_turn
from openapi_server.core.domain.game.round_type import RoundType


class GameService:
    """
    GameService class contains all logic connections between port and domain
    """

    def __init__(self, game_repository, round_repository, turn_repository, word_repository):
        self.game_repository = game_repository
        self.round_repository = round_repository
        self.turn_repository = turn_repository
        self.word_repository = word_repository

    def create_game(self, user, language):
        """
        Creates a gamed based on user_id
        :param language: language game is played in
        :param user: This user is the users id
        :return: returns the first letter and word length
        """
        # Basic information for starting a game
        game_type = RoundType.FiveCharacters.value

        # Create first round object
        random_word = self._choose_random_word(game_type, language)

        game_id = self.game_repository.insert_game(int(user), language, game_type)
        if game_id is not None:
            round_id = self.round_repository.insert_round(game_id, random_word)

            if round_id is not None:
                self.turn_repository.insert_turn(round_id)

        return random_word[0], game_type

    def _choose_random_word(self, word_length, language):
        """
        Choose a random word based on word length
        :param word_length: length the word need to be
        :return: random word
        """
        return self.word_repository.get_random_word(word_length, language)

    def guess_turn(self, user_id, guessed_word):
        # pylint: disable=inconsistent-return-statements
        """
        Turn to guess the word
        :param user_id: id of user
        :param guessed_word: users guess
        :return: round type, word response, (validation error)
        """
        now = datetime.now()

        if guessed_word is not None:
            game_details = self.game_repository.get_game_round_information(user_id)

            # List of all the information
            game_id = game_details.get('game_id')
            round_id = game_details.get('round_id')

            # pylint: disable=line-too-long
            turn_response = run_turn(guessed_word, game_details.get('correct_word'),
                                     game_details.get('word_length'), game_details.get('turn_start_time'),
                                     now, self.turn_repository.get_turn_count(round_id),
                                     (game_details.get('game_language')).upper())
            # pylint: enable=line-too-long

            if turn_response[0].__eq__('correct'):
                # Update turn
                self.turn_repository.update_turn(guessed_word, round_id)
                # Change game length
                new_length = self._change_game_status(game_details.get('word_length'))
                self.game_repository.update_game_word_length(game_id, new_length)
                # End the round
                self.round_repository.update_end_round(round_id)
                # Update game score with +1
                self.game_repository.update_game_score(game_id)

            elif turn_response[0].__eq__('next-round') or \
                    turn_response[0].__eq__('validation-error'):
                # Update turn
                self.turn_repository.update_turn(guessed_word, round_id)
                # Insert new turn
                self.turn_repository.insert_turn(round_id)

            elif turn_response[0].__eq__('game-over'):
                self.turn_repository.insert_turn(round_id)
                self.round_repository.update_end_round(round_id)
                self.game_repository.update_end_game(game_id)
            else:
                return 'abort'

            if len(turn_response) == 3:
                return turn_response[0], turn_response[1], turn_response[2]

            return turn_response[0], turn_response[1]

        return 'abort'
        # pylint: enable=inconsistent-return-statements

    # pylint: disable=no-self-use
    def _change_game_status(self, current_length):
        """
        Change the game status based on the current word_length
        :param current_length: current game length
        :return: new game length
        """
        new_length = None

        if current_length == 5:
            new_length = RoundType.SixCharacters.value
        elif current_length == 6:
            new_length = RoundType.SevenCharacters.value
        elif current_length == 7:
            new_length = RoundType.FiveCharacters.value

        return new_length

    # enable: disable=no-self-use

    def create_round(self, user_id):
        """
        Create a new round
        :param user_id: id of user to make a new round for the user
        :return: first letter of new word and word length
        """
        game_details = self.game_repository.get_game_information(user_id)

        word_length = game_details.get('word_length')
        game_id = game_details.get('game_id')

        random_word = self._choose_random_word(word_length, game_details.get('language'))
        round_id = self.round_repository.insert_round(game_id, random_word)

        if round_id is not None:
            self.turn_repository.insert_turn(round_id)
            return random_word[0], word_length  # pylint: disable=inconsistent-return-statements

        return 'abort'
