import unittest

from src.unitxt.blocks import (
    LoadHF,
    SplitRandomMix,
    AddFields,
    TaskCard,
    FormTask,
    TemplatesList,
    InputOutputTemplate,
    MapInstanceValues
)
from src.unitxt.test_utils.card import test_card

card = TaskCard(
        loader=LoadHF(path='glue', name='wnli'),
        preprocess_steps=[
            SplitRandomMix({'train': 'train[95%]', 'validation': 'train[5%]', 'test': 'validation'}),
            MapInstanceValues(mappers={'label': {"0": 'entailment', "1": 'not_entailment'}}),
            AddFields(
            fields={
                'choices': ['entailment', 'not_entailment'],
            }
            ),
        ],
        task=FormTask(
            inputs=['choices', 'sentence1', 'sentence2'],
            outputs=['label'],
            metrics=['metrics.accuracy'],
        ),
        templates=TemplatesList([
            InputOutputTemplate(
                input_format="""
                    Given this sentence: {sentence1}, classify if this sentence: {sentence2} is {choices}.
                """.strip(),
                output_format='{label}',
            ),
               ])
    )

from src.unitxt.test_utils.card import test_card

class TestCard(unittest.TestCase):
    
    def test_card(self):
        test_card(card)