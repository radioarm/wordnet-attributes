# -*- coding: utf-8 -*-

import nltk
import spacy

from abc import ABC, abstractmethod
from stop_words import get_stop_words
from typing import List


class TextTokenizer(ABC):
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.nlp = spacy.load(model_path)

    @property
    @abstractmethod
    def allow_postags(self):
        pass

    @property
    @abstractmethod
    def stop_words(self):
        pass

    def check_token(self, token: str) -> bool:
        return all([
            token.text not in self.stop_words,
            token.pos_ in self.allow_postags
        ])

    def tokenize(self, text: str) -> List[str]:
        return [
            token.lemma_
            for token in self.nlp(text) if self.check_token(token)
        ]


class BasicEnglishTextTokenizer(TextTokenizer):
    allow_postags = ['NOUN', 'VERB', 'PROPN', 'ADJ', 'ADV']
    stop_words = nltk.corpus.stopwords.words('english')


class BasicEnglishTextTokenizerNoAdjectives(TextTokenizer):
    allow_postags = ['NOUN', 'VERB', 'PROPN', ]
    stop_words = nltk.corpus.stopwords.words('english')


class BasicPolishTextTokenizer(TextTokenizer):
    allow_postags = ['NOUN', 'VERB', 'PROPN', 'ADJ', 'ADV']
    stop_words = get_stop_words('polish')