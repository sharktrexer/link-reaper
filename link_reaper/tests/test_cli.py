import pytest
import click

from click.testing import CliRunner
from link_reaper.reaper import link_reaper

@pytest.mark.parametrize(
    "file_name, expected_exit_code",
    [
        ("testfile.md", 0),
        ("doesnotexist.md", 2),
    ],
)
def test_for_file(file_name, expected_exit_code):
    runner = CliRunner()
    
    # Create test file
    with runner.isolated_filesystem():
        with open('testfile.md', 'w') as f:
            f.write('1. [github](https://github.com/sharktrexer)')
    
        result = runner.invoke(link_reaper, ["reap", file_name, "-m", "-dl"])
        print(result.output)
        assert result.exit_code == expected_exit_code