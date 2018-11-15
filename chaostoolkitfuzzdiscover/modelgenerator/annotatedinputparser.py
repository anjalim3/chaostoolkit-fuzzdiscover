from kitty.model import *
from chaostoolkitfuzzdiscover.constants.ctfuzzdiscoverconstants import SupportedUserAnnotations

#ToDo: Add support for more tokens (file etc)
class AnnotatedInputParser:

    @staticmethod
    def __get_kittyfields_from_token(token):
        return None

    @staticmethod
    def __get_kittyfields_from_token(token):
        __kitty_fields = []
        if "@@{ct_Fuzz_" in token and str(token).index("@@{ct_Fuzz_") == 0:
            __unmarshalled_token = token.lstrip("@@{ct_Fuzz_")
            if SupportedUserAnnotations.Number in __unmarshalled_token and __unmarshalled_token.index(SupportedUserAnnotations.Number) == 0:
                __unmarshalled_token = __unmarshalled_token.lstrip("Number{").rstrip("}}")
                __kitty_fields.append(Float(value=float(__unmarshalled_token)))
            elif SupportedUserAnnotations.String in __unmarshalled_token and __unmarshalled_token.index(SupportedUserAnnotations.String) == 0:
                __unmarshalled_token == __unmarshalled_token.lstrip("String{").rstrip("}}")
                __kitty_fields.append((String(value=__unmarshalled_token, fuzzable=True)))
            return __kitty_fields
        __kitty_fields.append(Delimiter(token, fuzzable=False))
        return __kitty_fields

    @staticmethod
    def get_kittytemplate_from_input(input_string):
        print input_string
        tokens = re.split(r'(@@{ct_Fuzz_.*?}})', input_string)
        kitty_fields = []
        for token in tokens:
            kittyfields_from_token = AnnotatedInputParser.__get_kittyfields_from_token(token)
            if kittyfields_from_token is not None:
                kitty_fields.extend(kittyfields_from_token)
        return Template(fields=kitty_fields)