import re

def on_page_markdown(markdown, page, config, files):
    """
    Rewrite relative Markdown links for MkDocs-compatible paths.
    
    Parameters:
        markdown (str): Markdown content whose links should be rewritten.
        page: MkDocs page associated with the content.
        config: MkDocs configuration.
        files: MkDocs file collection.
    
    Returns:
        str: Markdown content with applicable relative links rewritten.
    """
    def replace_link(match):
        """
        Rewrite a Markdown link URL for MkDocs compilation.
        
        Parameters:
        	match: A regular expression match containing link text and URL groups.
        
        Returns:
        	str: The link with its relative URL adjusted, or the original link for external and anchor-only URLs.
        """
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
