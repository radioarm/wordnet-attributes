# -*- coding: utf-8 -*-

import itertools

from abc import ABC, abstractmethod
from dataclasses import dataclass
from statistics import mean
from typing import List, Tuple

from synset_representation import SynsetRepresenation
from similarities import SimilarityCalculator


@dataclass
class SynsetChoiceStrategy(ABC):
    similarity_calculator: SimilarityCalculator

    @abstractmethod
    def create_ordering(
        self,
        tokenized_concept_name: List[str],
        synset_repr_list: List[SynsetRepresenation],
    ) -> List[Tuple[SynsetRepresenation, float]]:
        pass


class MaxSimilarityChoiceStrategy(SynsetChoiceStrategy):
    def create_ordering(
        self,
        tokenized_concept_name: List[str],
        synset_repr_list: List[SynsetRepresenation],
    ) -> List[Tuple[SynsetRepresenation, float]]:

        ranked_synsets_reprs = []
        for synset_repr in synset_repr_list:
            partial_sims = [
                self.similarity_calculator.calculate(*pair)
                for pair in itertools.product(
                    tokenized_concept_name, synset_repr.tokenized_definition
                )
            ]

            max_sim = max(partial_sims) if partial_sims else 0
            ranked_synsets_reprs.append((synset_repr, max_sim))

        return list(sorted(
            ranked_synsets_reprs, key=lambda x: x[1], reverse=True))


class AvgSimilarityChoiceStrategy(SynsetChoiceStrategy):
    def create_ordering(
        self,
        tokenized_concept_name: List[str],
        synset_repr_list: List[SynsetRepresenation],
    ) -> List[Tuple[SynsetRepresenation, float]]:

        ranked_synsets_reprs = []
        for synset_repr in synset_repr_list:
            partial_sims = [
                self.similarity_calculator.calculate(*pair)
                for pair in itertools.product(
                    tokenized_concept_name, synset_repr.tokenized_definition
                )
            ]


            mean_sim = mean(partial_sims) if partial_sims else 0
            ranked_synsets_reprs.append((synset_repr, mean_sim))

        return list(sorted(
            ranked_synsets_reprs, key=lambda x: x[1], reverse=True))


class AvgWithoutZerosSimilarityChoiceStrategy(SynsetChoiceStrategy):
    def create_ordering(
        self,
        tokenized_concept_name: List[str],
        synset_repr_list: List[SynsetRepresenation],
    ) -> List[Tuple[SynsetRepresenation, float]]:

        ranked_synsets_reprs = []
        for synset_repr in synset_repr_list:
            partial_sims = [
                self.similarity_calculator.calculate(*pair)
                for pair in itertools.product(
                    tokenized_concept_name, synset_repr.tokenized_definition
                )
            ]

            partial_sims = filter(lambda x: x!=0, partial_sims)
            mean_sim = mean(partial_sims) if partial_sims else 0
            ranked_synsets_reprs.append((synset_repr, mean_sim))

        return list(sorted(
            ranked_synsets_reprs, key=lambda x: x[1], reverse=True))