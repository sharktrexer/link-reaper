import link_reaper


def test_valid_markdown_link():
    valid_md_link = "[test](https://test.com)"
    assert link_reaper.find_markdown_link(valid_md_link) is None
