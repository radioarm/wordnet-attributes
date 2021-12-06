# -*- coding: utf-8 -*-

import itertools

from dataclasses import dataclass
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Synset
from typing import List

from synset_choice_strategies import SynsetChoiceStrategy
from synset_representation import SynsetRepresenation
from mutation import TermMutator


def get_candidate_synsets(word_list: List[str]) -> List[Synset]:
    return list(
        set(
            itertools.chain.from_iterable(
                [wn.synsets(word) for word in word_list]
            )
        )
    )


@dataclass
class ConceptAttributeSemanticsGenerator:
    concept_name: str
    attribute_name: str
    term_mutator: TermMutator
    synset_choice_strategy: SynsetChoiceStrategy

    @property
    def mutated_concept_name(self) -> List[str]:
        return self.term_mutator.mutate(self.concept_name)

    @property
    def mutated_attribute_name(self) -> List[str]:
        return self.term_mutator.mutate(self.attribute_name)

    def get_candidate_attribute_synsets(self) -> List[SynsetRepresenation]:
        simple_attribute_names = []
        compound_attribute_names = []

        for mut in self.mutated_attribute_name:
            if '_' in mut:
                compound_attribute_names.append(mut)
            else:
                simple_attribute_names.append(mut)

        output_synsets = get_candidate_synsets(compound_attribute_names)
        if not output_synsets:
            output_synsets = get_candidate_synsets(simple_attribute_names)

        return [
            SynsetRepresenation(
                synset, self.term_mutator.mutate(synset.definition()))
            for synset in output_synsets
        ]

    def get_synset_for_attribute_semantics(self) -> Synset:
        candidate_synsets = self.get_candidate_attribute_synsets()
        if candidate_synsets:
            ordered_synsets = self.synset_choice_strategy.create_ordering(
                self.mutated_concept_name,
                self.get_candidate_attribute_synsets()
            )
            for candid in ordered_synsets:
                print(f'    {candid[0].base_synset.name()}, {candid[0].tokenized_definition}, {candid[1]}')
            return ordered_synsets[0][0].base_synset
        return None
