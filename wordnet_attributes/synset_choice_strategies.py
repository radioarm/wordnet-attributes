# -*- coding: utf-8 -*-

import itertools

from abc import ABC, abstractmethod
from dataclasses import dataclass
from statistics import mean
from typing import List

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
    ) -> List[SynsetRepresenation]:
        pass



class MaxSimilarityChoiceStrategy(SynsetChoiceStrategy):
    def create_ordering(
        self,
        tokenized_concept_name: List[str],
        synset_repr_list: List[SynsetRepresenation],
    ) -> List[SynsetRepresenation]:

        ranked_synsets_reprs = []
        for synset_repr in synset_repr_list:
            partial_sims = []

            for pair in itertools.product(tokenized_concept_name, synset_repr.tokenized_definition):
                try:
                    partial_sims.append(self.similarity_calculator.calculate(*pair))
                except Exception as e:
                    partial_sims.append(0)

            try:
                max_sim = max(partial_sims)
            except ValueError:
                max_sim = 0

            ranked_synsets_reprs.append((synset_repr, max_sim))

        return [
            elem[0] for elem in sorted(
                ranked_synsets_reprs, key=lambda x: x[1], reverse=True)
        ]


class AvgSimilarityChoiceStrategy(SynsetChoiceStrategy):
    def create_ordering(
        self,
        tokenized_concept_name: List[str],
        synset_repr_list: List[SynsetRepresenation],
    ) -> List[SynsetRepresenation]:

        ranked_synsets_reprs = []
        for synset_repr in synset_repr_list:
            partial_sims = []

            for pair in itertools.product(tokenized_concept_name, synset_repr.tokenized_definition):
                try:
                    partial_sims.append(self.similarity_calculator.calculate(*pair))
                except Exception as e:
                    partial_sims.append(0)

            ranked_synsets_reprs.append((synset_repr, mean(partial_sims)))

        return [
            elem[0] for elem in sorted(
                ranked_synsets_reprs, key=lambda x: x[1], reverse=True)
        ]


class AvgWithoutZerosSimilarityChoiceStrategy(SynsetChoiceStrategy):
    def create_ordering(
        self,
        tokenized_concept_name: List[str],
        synset_repr_list: List[SynsetRepresenation],
    ) -> List[SynsetRepresenation]:

        ranked_synsets_reprs = []
        for synset_repr in synset_repr_list:
            partial_sims = []

            for pair in itertools.product(tokenized_concept_name, synset_repr.tokenized_definition):
                try:
                    partial_sims.append(self.similarity_calculator.calculate(*pair))
                except Exception as e:
                    continue

            partial_sims = list(filter(lambda x: x!=0, partial_sims))
            mean_sim = mean(partial_sims) if partial_sims else 0
            ranked_synsets_reprs.append((synset_repr, mean_sim))

        return [
            elem[0] for elem in sorted(
                ranked_synsets_reprs, key=lambda x: x[1], reverse=True)
        ]