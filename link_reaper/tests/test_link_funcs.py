from link_reaper import link_collector


def test_valid_markdown_link_formats():
    valid_links = []
    valid_links.append("[test](https://test.com)")
    valid_links.append("<https://test.com>")
    valid_links.append("[i](i)")
    for link in valid_links:
        assert len(link_collector.grab_md_links(link))


test_valid_markdown_link_formats()


def test_invalid_markdown_link_formats():
    invalid_links = []
    invalid_links.append("[invalid(http://test.com)")
    invalid_links.append("[i]http://test.com)")
    invalid_links.append("i]http://test.com)")
    invalid_links.append("http://test.com")

    for link in invalid_links:
        assert not link_collector.grab_md_links(link)
