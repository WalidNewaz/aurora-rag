from selectolax.parser import HTMLParser
from urllib.parse import urljoin, urlparse

class HtmlParser:
    @staticmethod
    def extract_links(html: str, base_url: str, allowed_domains: list[str]) -> list[str]:
        tree = HTMLParser(html)
        links = []

        for node in tree.css("a"):
            href = node.attrs.get("href")
            if not href:
                continue

            absolute = urljoin(base_url, href)
            domain = urlparse(absolute).netloc

            if any(domain.endswith(d) for d in allowed_domains):
                links.append(absolute)

        return links