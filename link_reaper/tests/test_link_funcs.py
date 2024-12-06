import pytest

from link_reaper import link_collector

@pytest.mark.parametrize("str, expected_length", [
    ("[test](https://test.com)", 1), 
    ("<https://test.com>", 1),
    ("[i](i)", 1),
    ("[invalid(http://test.com)", 0),
    ("[i]http://test.com)", 0),
    ("i]http://test.com)", 0),
    ("http://test.com", 0)
])
def test_markdown_link_formats(str, expected_length):

    assert len(link_collector.grab_md_links(str)) == expected_length
