# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List

from nltk.corpus.reader.wordnet import Synset


@dataclass
class SynsetRepresenation:
    base_synset: Synset
    tokenized_definition: List[str] = field(default_factory=list)