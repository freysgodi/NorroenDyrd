#!/usr/bin/env python3
import cgi
import datetime
from NorroenDyrd import NorroenDyrd

form = cgi.FieldStorage()
refresh = form.getfirst("refresh", "nope")

print ("Content-type: text/html\n")
print ("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Обновление индекса</title>
        </head>
        <body>""")
print ("""<p></p>""")
print ("""<p></p>""")
print ("""<p></p>""")
print ("""<hr>""")
if refresh == "doit":
    NorroenDyrd.removeMirror()
    stime = datetime.datetime.today()
    print ("<center><h2>Начало синхронизации индекса:", stime.strftime("%d.%m.%Y  %H:%M:%S"),"</h2></center>")
    NorroenDyrd.dload()
    NorroenDyrd.setIndex()
    ftime = datetime.datetime.today()
    d = ftime - stime
    with open(NorroenDyrd.logfile, "w+", encoding="utf-8") as f:
        f.write("-- Full sync time " + str(d.seconds) + "seconds")
    print("<p></p>")
    print ("<center><h2>Синхронизация индекса завершена за ", d.seconds,"секунд</h2></center>")

else:
    print ("""<center><h2>Что-то не так...</h2></center>""")    
print ("""<p></p>""")
print ("""<p></p>""")
print ("""<p></p>""")
print ("""<center><h2><a href="http://localhost:8000">Назад к строке поиска</a></h2></center>""")    

print ("""</body>
        </html>""")

