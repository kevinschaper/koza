"""
Testing the biolink model dataclasses + pydandic
"""
from bioweave.model.biolink.named_thing import *


def test_foo():
    molec_entity = MolecularEntity()
    assert set(molec_entity.category) == {'MolecularEntity', 'BiologicalEntity', 'NamedThing'}
