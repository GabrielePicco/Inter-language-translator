from enum import Enum
import pandas as pd

ENG_TO_ITA_DICTIONARY = "./eng_to_ita.csv"


class Languages(Enum):
    ENGLISH = 1
    ITALIAN = 2


class WordTanslator:

    def __init__(self, language_from, language_to):
        self.language_from = language_from
        self.language_to = language_to

    def translate_word(self, word):
        if self.language_from == Languages.ENGLISH and self.language_to == Languages.ITALIAN:
            dict = pd.read_csv(ENG_TO_ITA_DICTIONARY, header=None, sep=";")
            lookup = list(dict[dict[0] == word][1])
            if len(lookup) > 0:
                return lookup[0]
            else:
                return word
        else:
            raise NotImplementedError()
