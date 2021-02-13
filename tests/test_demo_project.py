from demo_project import __version__
from demo_project.demo import hello_world


def test_version():
    assert __version__ == "0.1.0"


def test_function(capsys):
    hello_world()
    captured = capsys.readouterr()
    assert captured.out == "hello world\n"
