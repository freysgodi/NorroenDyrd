#!/usr/bin/env python3
import cgi
from NorroenDyrd import NorroenDyrd

form = cgi.FieldStorage()
seek = form.getfirst("TEXT_1", "")

print("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Обработка данных форм</title>
        </head>
        <body>""")
print("<h1>Результаты поиска в корпусе Norrœn Dýrð</h1>")
print("<h2>", seek, "</h2>")

NorroenDyrd.readIndex()
total = 0
matches = []
if seek == "":
    print("<p>Не задана строка для поиска</p>")
else:
    matches = NorroenDyrd.search(seek)
    for i in matches:
        total += i["total"]
if total == 0:
    print("<p>Не найдено совпадений: ", seek, "</p>")
else:
    print("<p></p>")
    print("<h3>", seek, ": найдено ", total, "вхождений\n\n</h3>")
    k = 1
    print("<table border = 1>")
    for i in matches:
        print("<h4><tr><td>", k, "</td><td><a href=", i["link"], ">Ссылка</a></td><td>", "Текст: ", i["title"], "</td></tr></h4>")
        k += 1
    print("</table>")

print("""<h2><a href="http://127.0.0.1:8000">Назад к вводу строки поиска</a></h2>""")

print("""</body>
        </html>""")
