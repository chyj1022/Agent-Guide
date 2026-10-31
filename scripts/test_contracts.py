"""Application contract examples, not MCP protocol conformance tests."""
import copy
import json
from pathlib import Path
import unittest
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = json.loads((ROOT / 'contracts/examples.json').read_text(encoding='utf-8'))

def validate(name, value):
    schema = json.loads((ROOT / f'contracts/{name}.schema.json').read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(value)

class ContractTests(unittest.TestCase):
    def test_examples_match_schemas(self):
        for name,value in EXAMPLES.items():
            with self.subTest(schema=name):
                validate(name,value)

    def test_write_requires_approval_and_idempotency(self):
        value=copy.deepcopy(EXAMPLES['tool-request'])
        value['tool']='save_draft'
        with self.assertRaises(ValidationError): validate('tool-request',value)
        value.update(approval_id='a',idempotency_key='k')
        validate('tool-request',value)

    def test_errors_cannot_masquerade_as_data(self):
        value=copy.deepcopy(EXAMPLES['tool-result'])
        value.update(status='denied',error_code='forbidden')
        with self.assertRaises(ValidationError): validate('tool-result',value)
        value['data']=None
        validate('tool-result',value)

    def test_unknown_fields_negative_budget_and_bad_hash(self):
        for name,alter in [
            ('tool-request', lambda v:v.update(tool='delete_everything')),
            ('approval', lambda v:v.update(arguments_sha256='not-a-hash')),
            ('run-state', lambda v:v['limits'].update(steps=-1)),
            ('run-state', lambda v:v.update(untrusted_field=True))]:
            with self.subTest(schema=name):
                value=copy.deepcopy(EXAMPLES[name]);alter(value)
                with self.assertRaises(ValidationError):validate(name,value)

if __name__=='__main__': unittest.main()
