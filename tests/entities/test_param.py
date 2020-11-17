from tests.factories import (
    I18nFactory,
    ParamOperationSpecsFactory,
)

from tests.utils import case, create_entity_test_suite


class Dummy:
    i18n = I18nFactory(name='dummy-name', description='dummy-desc')
    jsonschema = {'type': 'object'}


class Case:
    I18n = case('i18n', Dummy.i18n, Dummy.i18n, id='i18n')
    Uid = case('uid', 'test-uid', 'test-uid', id='uid')
    PropsSchema = case(
        'properties_schema',
        Dummy.jsonschema,
        Dummy.jsonschema,
        id='properties_schema',
    )


test_param_operation_spec_has_expected_attribute = create_entity_test_suite(
    ParamOperationSpecsFactory,
    [Case.Uid, Case.I18n, Case.PropsSchema]
)
