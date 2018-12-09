from kitty.model import *
from chaostoolkitfuzzdiscover.constants.generic_constants import GenericConstants

class UnannotatedInputParser:

    @staticmethod
    def __is_number(token):
        try:
            float(token)
            return True
        except ValueError:
            pass
        try:
            import unicodedata
            unicodedata.numeric(token)
            return True
        except (TypeError, ValueError):
            pass
        return False

    # ToDo: Improve string recognition
    @staticmethod
    def __get_string_token(token):
        if GenericConstants.http_request_methods.__contains__(token):
            kitty_field = Group(values=GenericConstants.http_request_methods, fuzzable=True)
        elif GenericConstants.network_protocols.__contains__(token):
            kitty_field = Group(values=GenericConstants.network_protocols, fuzzable=True)
        else:
            kitty_field = String(token)
        return kitty_field

    @staticmethod
    def __get_kittyfields_from_token(token):
        kitty_fields = []
        if token.isdigit():
            kitty_fields.append(Dword(value=int(token), encoder=ENC_INT_DEC))
        else:
            if token.isalpha():
                kitty_fields.append(UnannotatedInputParser.__get_string_token(token))
            elif token.isalnum():
                kitty_fields.append(String(value=token, fuzzable=True))
            elif UnannotatedInputParser.__is_number(token):
                kitty_fields.append(Float(value=float(token), fuzzable=True))
            elif re.match(r'[`\-=~!@#$%^&*()+\[\]{};\'\\:"|<,/<>? ]', token):
                kitty_fields.append(Delimiter(value=token, fuzzable=False))
            else:
                kitty_fields.append(String(value=token, fuzzable=True))
        return None if len(kitty_fields) == 0 else kitty_fields

    @staticmethod
    def get_kittytemplate_from_input(input_string):
        tokens = re.split(r'([`\-=~!@#$%^&*()+\[\]{};\'\\:"|<,/<>? ])', input_string)
        fields = []
        for token in tokens:
            kittyfields_from_token = UnannotatedInputParser.__get_kittyfields_from_token(token)
            if kittyfields_from_token is not None:
                fields.extend(kittyfields_from_token)
        return Template(fields=fields)
