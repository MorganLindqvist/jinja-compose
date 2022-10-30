import jinja_docker_compose.cli as cli
import pytest


def test_all_default():
    assert cli.main() == 0


def test_bad_input():
    assert cli.main("-f /not-exists.yml.j2 -D docker-compose.dic -o /dev/null".split()) == 101


def test_empty_input():
    with pytest.raises(RuntimeError) as pytest_wrapped_e:
        cli.main("-f /dev/null -D docker-compose.dic -o /dev/null".split())
    assert pytest_wrapped_e.type == RuntimeError
    assert pytest_wrapped_e.value.args[0] == "Compose file is empty"


def test_bad_dictionary():
    assert cli.main("-f docker-compose.yml.j2 -D /not-exist.dic -o /dev/null".split()) == 102


def test_empty_dic():
    assert cli.main("-f docker-compose.yml.j2 -D docker-compose.empty.dic -o /dev/null".split()) == 1


def test_noOp_dic():
    assert cli.main("-f docker-compose.yml.j2 -D docker-compose.noOp.dic -o /dev/null".split()) == 2


def test_bad_output():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        cli.main("-f docker-compose.yml.j2 -D docker-compose.dic -o /not-exists.yml".split())
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2


def test_compose_drop_output():
    assert cli.main("-f docker-compose.yml.j2 -D docker-compose.dic -o /dev/null".split()) == 0


def test_compose_default_input():
    assert cli.main("-D docker-compose.dic -o /dev/null".split()) == 0


def test_compose_default_dic():
    assert cli.main("-f docker-compose.yml.j2 -o /dev/null".split()) == 0


def test_compose_default_output():
    assert cli.main("-f docker-compose.yml.j2 -D docker-compose.dic".split()) == 0


def test_fullloader():
    assert cli.main("-f docker-compose.yml.j2 -D docker-compose.dic -o /dev/null --loader".split()) == 0


def test_compose_check_result():
    assert cli.main("-f docker-compose.yml.j2 -D docker-compose.dic -o docker-compose.yml".split()) == 0
    with open('docker-compose.yml') as produced:
        pro_lines = produced.readlines()
    with open('docker-compose.ref.yml') as reference:
        ref_lines = reference.readlines()
    assert pro_lines == ref_lines


def test_compose_up_down():
    assert cli.main("-f docker-compose.yml.j2 -D docker-compose.dic -o docker-compose.yml -r up -d".split()) == 0
    assert cli.main("-f docker-compose.yml.j2 -D docker-compose.dic -o docker-compose.yml -r down".split()) == 0
