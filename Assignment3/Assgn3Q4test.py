from bs4 import BeautifulSoup
import re

# The HTML content
html_content = """
<html>
<head>
<title>My first web page</title>
</head>
<body>
<h1>My first web page</h1>
<h2>What this is tutorial</h2>
<p>A simple page put together using HTML. <em>I said a simple page.</em>.</p>
<ul>
 <li>To learn HTML</li>
 <li>
 To show off
 <ol>
Grammar (CFG):
S → NP VP
NP → Det Nominal
Nominal → Nominal Noun | Noun
VP → V NP | V
Det → 'the' | 'a'
Noun → 'dog' | 'park' | 'chase'
V → 'sees' | 'finds'
Lexicon:
Det (Determiner): the, a
Noun: dog, park, chase
V (Verb): sees, finds
 <li>To my boss</li>
 <li>To my friends</li>
 <li>To my cat</li>
 <li>To the little talking duck in my brain</li>
 </ol>
 </li>
 <li>Because I have fallen in love with my computer and want to give her some HTML loving.</li>
</ul>
<h3>Where to find the tutorial</h3>
<p><a href="http://www.aaa.com"><img src=http://www.aaa.com/badge1.gif></a></p>
<h4>Some random table</h4>
<table>
 <tr class="tutorial1">
 <td>Row 1, cell 1</td>
 <td>Row 1, cell 2<img src=http://www.bbb.com/badge2.gif></td>
 <td>Row 1, cell 3</td>
 </tr>
 <tr class="tutorial2">
 <td>Row 2, cell 1</td>
 <td>Row 2, cell 2</td>
 <td>Row 2, cell 3<img src=http://www.ccc.com/badge3.gif></td>
 </tr>
</table>
</body>
</html>
"""

# Parse the HTML
soup = BeautifulSoup(html_content, "html.parser")

# a) The text of the HTML page title using only HTML tags
title_text = soup.html.head.title.text
#print("a.", title_text)
# b) The text of the second <li> element below "To show off"
second_li_text = soup.find_all("li")[3].text.strip()
#print("b.", second_li_text)
# c) All <td> tags in the first row <tr> of the table
first_row_tds = soup.find("tr", class_="tutorial1").find_all("td")
#print("c.", [td for td in first_row_tds])
# d) All <h2> headings text that include the word "tutorial" (using regex)
h2_with_tutorial = soup.find("h2", text=re.compile("tutorial")).text
#print("d.", h2_with_tutorial)
# e) All text that includes the word "HTML"
html_text = soup.find_all(string=re.compile("HTML"))
#print("e.", html_text)
# f) All text in the second row <tr> of the table
second_row_text = [td.get_text(strip=True) for td in soup.find("tr", class_="tutorial2").find_all("td")]
#print("f.", second_row_text)
# g) All <img> tags from the table
img_tags = [img["src"] for img in soup.find("table").find_all("img")]
#print("g.", img_tags)
