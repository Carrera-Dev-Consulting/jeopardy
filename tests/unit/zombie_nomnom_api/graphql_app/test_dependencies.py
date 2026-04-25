import pytest
from zombie_nomnom_api.graphql_app.dependencies import DIContainer


class DependantClass:
    pass


def test_di_container__when_fetching_a_type_that_is_not_registered__raises_key_error():
    container = DIContainer()
    with pytest.raises(KeyError):
        container[DependantClass]


def test_di_container__when_fetching_a_type_that_is_registered__returns_the_instance():
    container = DIContainer()
    container.register(DependantClass)
    assert isinstance(container[DependantClass], DependantClass)


def test_di_container__when_registering_a_type_that_is_already_registered__replaces_the_instance():
    container = DIContainer()
    container.register(DependantClass)
    second_instance = DependantClass()
    container.register(DependantClass, second_instance)
    assert container[DependantClass] is second_instance


def test_di_container__when_registering_by_name_with_no_instance__raises_value_error():
    container = DIContainer()
    with pytest.raises(ValueError):
        container.register("DependantClass")
