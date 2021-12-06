# -*- coding: utf-8 -*-

import itertools
import re

from typing import List


def camel_case_split(text) -> List[str]:
    base = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', text))
    return base.split()


def normalize_text_value(value) -> List[str]:
    base = value.split('_')
    result = itertools.chain.from_iterable(
        [camel_case_split(elem) for elem in base])
    return [elem.lower() for elem in result]


def extract_attribute_name(text) -> str:
    return text.split(':')[0].strip()
