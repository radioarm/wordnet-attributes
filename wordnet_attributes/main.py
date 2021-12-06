# -*- coding: utf-8 -*-

import click
import datetime
import openpyxl
import toml

from concepts import ConceptAttributeSemanticsGenerator
from mutation import TermMutator
from similarities import Word2VecSimilarityCalculator
from tokenizer import BasicEnglishTextTokenizer, BasicEnglishTextTokenizerNoAdjectives
from synset_choice_strategies import (
    MaxSimilarityChoiceStrategy,
    AvgSimilarityChoiceStrategy,
    AvgWithoutZerosSimilarityChoiceStrategy,
)
from utils import extract_attribute_name


@click.command()
@click.argument("source_data_file", type=click.Path(exists=True))
@click.option("--config", "-c", default="config.toml", type=click.Path(exists=True))
def main(source_data_file, config):
    now_str = datetime.datetime.now().strftime("%Y%m%d%H%M")
    config = toml.load(config)
    dest_filename = f"{now_str}-output-{source_data_file}"

    mutator = TermMutator(
        tokenizer=BasicEnglishTextTokenizer(model_path=config["Spacy"]["model_path"])
    )

    word2vec_similarity_calculator = Word2VecSimilarityCalculator(
        model_path=config["Word2Vec"]["model_path"], limit=config["Word2Vec"]["limit"]
    )

    max_sim_choice_strategy = MaxSimilarityChoiceStrategy(
        similarity_calculator=word2vec_similarity_calculator
    )

    workbook = openpyxl.load_workbook(filename=source_data_file)
    for work_sheet in workbook:
        click.echo(click.style(work_sheet, fg="green"))
        for row in work_sheet.iter_rows(min_row=2):
            concept_name = row[0].value
            attribute_name = extract_attribute_name(row[1].value)
            semantics_generator = ConceptAttributeSemanticsGenerator(
                concept_name=concept_name,
                attribute_name=attribute_name,
                term_mutator=mutator,
                synset_choice_strategy=max_sim_choice_strategy,
            )
            click.echo(f"Concept: {concept_name}")
            click.echo(f"Attribute: {attribute_name}")
            click.echo("Candidate synsets:")
            chosen_synset = semantics_generator.get_synset_for_attribute_semantics()
            click.echo(f"Chosen synset: {chosen_synset}")
            click.echo()
            if chosen_synset:
                row[-1].value = chosen_synset.name()
        click.echo()
    workbook.save(filename=dest_filename)


if __name__ == "__main__":
    main()
