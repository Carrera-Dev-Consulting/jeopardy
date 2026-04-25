import click
import pytest
from zombie_nomnom_api.app import HostnameParameter


@pytest.mark.parametrize(
    "hostname",
    [
        "localhost",
        "127.0.0.1",
        "google.com",
        "sub.domain.com",
        "domain-with-hyphens.net",
        "123-abc.com-1",
    ],
)
def test_hostname_parameter__when_given_a_valid_hostname__validates_string(
    hostname: str,
):
    param = HostnameParameter()
    hostname = "localhost"

    value = param.convert(hostname, None, None)
    assert value == hostname


@pytest.mark.parametrize(
    "hostname",
    [
        "invalid host",
        "#invalid-host",
    ],
)
def test_hostname_parameter__when_given_an_invalid_hostname_string_spaces__raises_click_exception(
    hostname: str,
):
    param = HostnameParameter()

    with pytest.raises(click.BadParameter):
        param.convert(hostname, None, None)


def test_hostname_parameter__when_given_an_object__turns_into_string_and_validates_string():
    param = HostnameParameter()

    class SomeClass:
        def __str__(self):
            return "localhost"

    value = param.convert(SomeClass(), None, None)
    assert value == "localhost"
