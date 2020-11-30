from lingo.game.application.validation_logic import run_all_turn_validations


def run_turn(guessed_word, correct_word, word_length, turn_start_time, now, turn_count, game_language):
    # First check validations
    validation_response = run_all_turn_validations(guessed_word, word_length,
                                                   turn_start_time, now, game_language)
    validation = check_validation_response(validation_response)
    word_guess = ''
    character_response = ''

    if not validation[0]:
        character_response = check_characters(guessed_word, correct_word)

        if correct_word.__eq__(guessed_word):
            word_guess = 'correct'
        else:
            word_guess = 'next-round'

    if turn_count >= 5:
        if validation[0]:
            return 'game-over', character_response, validation[1]
        else:
            return 'game-over', character_response
    else:
        if validation[0]:
            character_response = invalid_characters(guessed_word)
            return 'validation-error', character_response, validation[1]
        else:
            return word_guess, character_response


def check_characters(guessed_word, correct_word):
    word_response = []

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

    return word_response


def invalid_characters(guessed_word):
    word_response = []

    for iteration, char in enumerate(guessed_word):
        word_response.append(char + " invalid")

    return word_response


def check_validation_response(validation_response):
    validation_error = False
    error_message = []
    for response in validation_response:
        if len(response) > 0:
            validation_error = True
            error_message.append(response)

    return validation_error, error_message
