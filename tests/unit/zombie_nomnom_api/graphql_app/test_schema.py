from copy import copy
import pytest
from zombie_nomnom_api.graphql_app.schema import register, _registry
from ariadne import ScalarType, SchemaBindable


@pytest.fixture(autouse=True)
def clear_registry():
    old_records = copy(_registry)
    yield
    _registry.clear()
    _registry.update(old_records)


def test_register__when_we_register_a_schema_with_new_name__adds_to_registry():
    name = "SomeType"
    assert name not in _registry, "Failed precheck fix tests"

    register(ScalarType(name))

    assert name in _registry, "New type was not registered correctly"


def test_register__when_we_register_a_schema_that_already_exists__does_not_replace_schema():
    second = ScalarType("SomeType")
    first = ScalarType(second.name)
    assert second.name not in _registry, "Failed precheck fix tests"

    register(first)
    register(second)

    registered_type = _registry[second.name]
    assert registered_type is not second, "Should not have replaced type"
    assert registered_type is first, "Should have resolved to first registered type"


def test_register__when_we_register_a_non_bindable_schema__does_not_add_to_registry():
    class Object:
        pass

    obj = Object()
    obj.name = "SomeType"

    register(obj)

    assert obj.name not in _registry


def test_register__when_we_register_bindable_with_no_name__does_not_bind():
    class CustomBinder(SchemaBindable):
        pass

    obj = CustomBinder()
    old_count = len(_registry)

    register(obj)

    assert len(_registry) == old_count
