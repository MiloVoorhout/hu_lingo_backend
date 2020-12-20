import unittest

from openapi_server.core.domain.game.game import check_characters, invalid_characters, check_validation_response


class TestGameLogicUnit(unittest.TestCase):
    # =============================
    # Test check_character function
    # =============================
    def test_characters_check_characters_partially_correct(self):
        """Test guess and correct word character response"""
        response = check_characters('DRAAD', 'BAARD')
        self.assertEqual(response.__eq__([{'letter': 'D', 'letterFeedback': 'absent'},
                                          {'letter': 'R', 'letterFeedback': 'present'},
                                          {'letter': 'A', 'letterFeedback': 'correct'},
                                          {'letter': 'A', 'letterFeedback': 'present'},
                                          {'letter': 'D', 'letterFeedback': 'correct'}]
                                         ), True)

    def test_characters_check_correct_word(self):
        """Test guess and correct word character response"""
        response = check_characters('PIZZA', 'PIZZA')
        self.assertEqual(response.__eq__([{'letter': 'P', 'letterFeedback': 'correct'},
                                          {'letter': 'I', 'letterFeedback': 'correct'},
                                          {'letter': 'Z', 'letterFeedback': 'correct'},
                                          {'letter': 'Z', 'letterFeedback': 'correct'},
                                          {'letter': 'A', 'letterFeedback': 'correct'}]
                                         ), True)

    def test_characters_check_wrong_word(self):
        """Test guess and correct word character response"""
        response = check_characters('OFFER', 'PIZZA')
        self.assertEqual(response.__eq__([{'letter': 'O', 'letterFeedback': 'absent'},
                                          {'letter': 'F', 'letterFeedback': 'absent'},
                                          {'letter': 'F', 'letterFeedback': 'absent'},
                                          {'letter': 'E', 'letterFeedback': 'absent'},
                                          {'letter': 'R', 'letterFeedback': 'absent'}]
                                         ), True)

    # ================================
    # Test invalid characters function
    # ================================
    def test_invalid_characters_set_all_character_invalid(self):
        """Test if response gives every character invalid"""
        response = invalid_characters('INVALID')
        self.assertEqual(response.__eq__([{'letter': 'I', 'letterFeedback': 'invalid'},
                                          {'letter': 'N', 'letterFeedback': 'invalid'},
                                          {'letter': 'V', 'letterFeedback': 'invalid'},
                                          {'letter': 'A', 'letterFeedback': 'invalid'},
                                          {'letter': 'L', 'letterFeedback': 'invalid'},
                                          {'letter': 'I', 'letterFeedback': 'invalid'},
                                          {'letter': 'D', 'letterFeedback': 'invalid'}]
                                         ), True)

    # ==============================
    # Test check_validation_response
    # ==============================
    def test_validation_response_there_was_a_validation_error(self):
        """Test if the validation response is correct"""
        response = check_validation_response(['A validation error message'])
        self.assertEqual(response[0], True)

    def test_validation_response_there_was_no_validation_error(self):
        """Test if the validation response is correct"""
        response = check_validation_response([])
        self.assertEqual(response[0], False)


if __name__ == '__main__':
    unittest.main()
