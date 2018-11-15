from kitty.model import *

#ToDo: The whole thing
class AnnotatedInputParser:

    @staticmethod
    def __get_kittyfields_from_token(token):
        return None

    @staticmethod
    def get_kittytemplate_from_input(input_string):
        print input_string
        tokens = re.findall('^@.*$}', input_string)
        print tokens

        return Template()
