import pytest

from link_reaper import link_collector


@pytest.mark.parametrize(
    "str, expected_length",
    [
        ("[test](https://test.com)", 1),
        ("<https://test.com>", 1),
        ("[i](i)", 1),
        ("[invalid(http://test.com)", 0),
        ("[i]http://test.com)", 0),
        ("i]http://test.com)", 0),
        ("http://test.com", 0),
        ("[hi()](http://test.com)", 1),
        ("[woah[]](i)", 1),
    ],
)
def test_markdown_link_formats(str, expected_length):
    assert len(link_collector.grab_md_links(str)) == expected_length


@pytest.mark.parametrize(
    "url_str, expected_bool",
    [
        ("https://github.com/sharktrexer", True),
        ("wrong", False),
        ("https//invalid.com", False),
        ("https://stackoverflow.com/", True),
    ],
)
def test_valid_url(url_str, expected_bool):
    assert link_collector.check_url_validity(url_str) == expected_bool
