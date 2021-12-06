# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

import gensim.models.keyedvectors as word2vec


class SimilarityCalculator(ABC):

    @abstractmethod
    def calculate(self, word1, word2) -> float:
        pass


class Word2VecSimilarityCalculator(SimilarityCalculator):

    def __init__(self, model_path, limit=0):
        self.model_path = model_path
        self.limit = limit
        self.model = word2vec.KeyedVectors.load_word2vec_format(
            model_path, binary=True, limit=limit)

    def calculate(self, word1, word2) -> float:
        try:
            return self.model.similarity(word1, word2)
        except KeyError:
            return 0