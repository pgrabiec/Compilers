import unittest
import main as model


def test(self, list_arg, function):
    """
    Parameters:
    self     - pass the argument from the test* functions
    list_arg - list of binary tuples of the form: [(z, y), ...]
               where x is the string to be processed,
               y is the expected result for the function passed
               as 3rd argument to this function for the argument x.
    function - function returning string result,
               taking a single string as the only parameter
    Fails the test unless the function evaluations for all inputs are equal to their expected values
    """
    for tuple in list_arg:
        input, expected_result = tuple
        result = function(input)
        if result != expected_result:
            print("Expected: " + str(expected_result) + "  computed: " + str(result))
        self.failUnless(result == expected_result)


class RegExprTests(unittest.TestCase):
    def test_extract_keywords(self):
        pass

    def test_count_sentences(self):
        pass

    def test_count_abbreviations(self):
        pass

    def test_count_emails(self):
        pass

    def test_count_integers(self):
        list_arg = [
            ('\n  123 -342 000000000000000000002 0000000000000 -32768 32767', 6),
            ('\n -32769 327679 1498321478934918 0000000032768 -00000000000032769 4312a a6723 -389a a-89 32e 23.4', 0),
            (' 123 ', 1)
        ]
        test(self, list_arg, model.count_integers)
        pass

    def test_count_float_numbers(self):
        pass

    def test_count_dates(self):
        pass

    def test_extract_department(self):
        pass

    def test_extract_author(self):
        list_arg = [(
            '\n <META NAME = "AUTOR" CONTENT = " Danuta Walewska,Wiesława Mazur">\n',
            " Danuta Walewska,Wiesława Mazur"
        )]
        test(self, list_arg, model.extract_author)


def execute():
    unittest.main()


if __name__ == '__main__':
    execute()