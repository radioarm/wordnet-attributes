# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List

from tokenizer import TextTokenizer
from utils import normalize_text_value


@dataclass
class TermMutator:
    tokenizer: TextTokenizer

    def mutate(self, text) -> List[str]:
        ''' has_PostalCode_Regional ->
        ['postal', 'code', 'postal_code', 'regional', 'postal_code_regional']
        '''
        split_value = ' '.join(normalize_text_value(text))
        output = self.tokenizer.tokenize(split_value)
        if len(output) <= 1:
            return output
        head, *tail = output
        result = [head, ]
        for elem in tail:
            head += f'_{elem}'
            result.extend([elem, head])
        return result
