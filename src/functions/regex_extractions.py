import re


def extract_markdown_images(text):
    pattern = re.compile(r"!\[(.*?)\]\((.*?)\)")
    return re.findall(pattern, text)


def extract_markdown_links(text):
    pattern = re.compile(r"[^!]\[(.*?)\]\((.*?)\)")
    return re.findall(pattern, text)
