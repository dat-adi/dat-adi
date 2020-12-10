import requests
import pathlib
import json
import sys
import re
import os
from bs4 import BeautifulSoup


root = pathlib.Path(__file__).parent.resolve()

def replace_chunk(content, marker, chunk, inline=False):
	# build the regular expression pattern, DOTALL will match any character, including a newline
	r = re.compile(
		r"<!-- {} starts -->.*<!-- {} ends -->".format(marker, marker),
		re.DOTALL,
	)
	# add newline before and after
	if not inline:
		chunk = "\n{}\n".format(chunk)
	# build the final chunk by adding comments before and after the chunk
	chunk = "<!-- {} starts -->{}<!-- {} ends -->".format(marker, chunk, marker)
	# replace matched string using pattern provided with the chunk
	return r.sub(chunk, content)

def fetch_article_links(link):
	page = requests.get(link).text
	soup = BeautifulSoup(page, "html.parser")
	articles_tag = soup.find_all("a", "author--post")
	article_links = [link.get("href") for link in articles_tag]
	return article_links


if __name__ == "__main__":
	readme = root / "README.md"

	readme_contents = readme.open().read()
	rewritten = readme_contents

	posts = fetch_article_links("https://www.askpython.com/author/datta")
	if len(posts) != 0:
		posts_md = "\n".join(
			["{} <br/>".format(link) for link in posts]
		)

		rewritten = replace_chunk(rewritten, "article-links", posts_md)

	readme.open("w").write(rewritten)
