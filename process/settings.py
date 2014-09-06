from iepy.models import set_custom_entity_kinds
from iepy.tokenizer import TokenizeSentencerRunner
from iepy.combined_ner import CombinedNERRunner

from process.person import PersonNERRunner
from process.date import DateNERRunner
from process.position_code import PositionCodeNERRunner
from process.resolution_ref import ResolutionRefNERRunner
from process.position import PositionNERRunner


# Optional custom step:
def extract_plain_text(doc):
    doc.text = doc.metadata['raw_data']
    doc.save()


# Insert here your custom entities:
CUSTOM_ENTITIES = ['date', 'position_code', 'resolution_ref', 'position']


set_custom_entity_kinds(zip(map(lambda x: x.lower(), CUSTOM_ENTITIES),
                            CUSTOM_ENTITIES))


pipeline_steps = [
    #extract_plain_text, # optional custom step
    TokenizeSentencerRunner(),
    CombinedNERRunner([
        PositionCodeNERRunner(),
        DateNERRunner(),
        ResolutionRefNERRunner(),
        PositionNERRunner(),
        ], override=True)
]
