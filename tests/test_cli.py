import jinja_docker_compose.main as main
import pytest


def test_failed_input():
    assert main.cli("-f /not-exists.yml.j2 -D tests/docker-compose.dic -o /dev/null".split()) is False


def test_failed_dictionary():
    assert main.cli("-f tests/docker-compose.yml.j2 -D /not-exist.dic -o /dev/null".split()) is False


def test_failed_output():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main.cli("-f tests/docker-compose.yml.j2 -D tests/docker-compose.dic -o /not-exists.yml".split())
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2


def test_cli():
    assert main.cli("-f tests/docker-compose.yml.j2 -D tests/docker-compose.dic -o /dev/null".split())
