from urllib.request import urlopen

html = urlopen('http://pythonscraping.com/pages/page1.html')
print(html.read())

html = urlopen('https://www.cpp.edu/')
print("CPP: " + str(html.read()))


html_string = html.read().decode('utf-8')
print("CPP decoded" + html_string)