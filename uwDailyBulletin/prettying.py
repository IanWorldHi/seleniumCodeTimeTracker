from bs4 import BeautifulSoup

uglyHtml = ""
with open("htmlOrg.html", "r", encoding="utf-8") as f:
    uglyHtml = f.read()

soup = BeautifulSoup(uglyHtml, "html.parser")
uglyHtml = soup.prettify()

#This would fix the type error as fyi
""" 
if isinstance(rawPretty, str):
    prettyHtml = rawPretty
else:
    prettyHtml = bytes(rawPretty).decode("utf-8", errors="replace")
 """

#Shows error bc type-checker can't gaurantee/know prettify returns a string
with open("htmlOrgP.html", "w", encoding="utf-8") as f:
    f.write(uglyHtml)


