import re

def on_page_markdown(markdown, page, config, files):
    """
    MkDocs hook to dynamically translate GitHub-relative links to work with MkDocs.

    1. Removes 'docs/' prefix from links in root-level files compiled at the site root
       (e.g., [Cloning Guide](docs/HOWTO-CLONE-DSOM-PROJECT.md) -> [Cloning Guide](HOWTO-CLONE-DSOM-PROJECT.md)).
    2. Translates '../../' repository-root relative links in 2-level-deep docs to '../'
       (e.g., [START-HERE.md](../../START-HERE.md) -> [START-HERE.md](../START-HERE.md)).
    """
    def replace_link(match):
        text = match.group(1)
        url = match.group(2)

        # Keep external or anchor-only links intact
        if url.startswith(('http://', 'https://', 'mailto:', 'ftp:', '#')):
            return match.group(0)

        new_url = url

        # If the link starts with 'docs/', strip it
        if new_url.startswith('docs/'):
            new_url = new_url[5:]
        # If the link starts with '../../', convert to '../' for MkDocs compilation
        elif new_url.startswith('../../'):
            new_url = '../' + new_url[6:]

        return f"[{text}]({new_url})"

    # Match markdown links: [text](url)
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_link, markdown)
