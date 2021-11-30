# -*- coding: utf-8 -*-

import re


def camel_case_split(text):
    base = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', text))
    return base.split()