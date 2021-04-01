class NorroenDyrd:

    import configparser


    config = configparser.ConfigParser()
    config.read("config.ini")

    mirror = config["Dirs"]["root"] + "/files" + config["Dirs"]["mirror"]
    root = config["Dirs"]["root"]
    base = config["Dirs"]["base"]
    ipath = root + "/files/index.json"
    index = []
    logfile = root + "/files/sync.log"

    @staticmethod
    def dload():
        from subprocess import call
        import datetime
        import os

        stime = datetime.datetime.today()
        os.chdir(NorroenDyrd.root + "/files")

        call(NorroenDyrd.root + "/cgi-bin/NorroenDyrdDload")
        ftime = datetime.datetime.today()
        delta = ftime - stime
        with open(NorroenDyrd.logfile, "w+", encoding="utf-8") as f:
            f.write("-- NorroenDyrd index sync\n\n")
            f.write("Start time: " + stime.strftime("%d.%m.%Y  %H:%M:%S")+"\n")
            f.write("Downloading time: " + str(delta.seconds) + "seconds\n")

    @staticmethod
    def removeMirror():
        import os

        for (p,d,f) in os.walk(NorroenDyrd.root + "/files/norse.ulver.com"):
            for fn in f:
                os.remove(os.path.join(p,fn))
            for dn in d:
                os.rmdir(os.path.join(p,dn))
        #os.rmdir(NorroenDyrd.root + "/files/norse.ulver.com")

    @staticmethod
    def setIndex():
        from MyHTMLParser import MyHTMLParser
        import os

        HTMLlist = []
        nobody = ["index.html", "index1.html", "index2.html", "index3.html", "index4.html", "ru3.html", "ru2.html",
                  "ru1.html", "rut.html", "rus.html", "ru.html"]
        for (parent, d, f) in os.walk(NorroenDyrd.mirror):
            for fn in f:
                if fn in nobody:
                    continue
                elif fn.find(".html") == -1:
                    continue
                elif os.path.join(parent, fn) in HTMLlist:
                    continue
                else:
                    HTMLlist.append(os.path.join(parent, fn))
        html = []
        for h in HTMLlist:
            entry = {}
            with open(h, "r", encoding="utf-8") as f:
                html = f.readlines()
            parser = MyHTMLParser()
            for i in html:
                parser.feed(i)
            entry["path"] = h.replace(NorroenDyrd.mirror, NorroenDyrd.base)
            entry["text"] = parser.plaintext
            entry["title"] = parser.title
            NorroenDyrd.index.append(entry)
            del parser

    @staticmethod
    def readIndex():
        import json
        NorroenDyrd.index = []
        with open(NorroenDyrd.ipath, "r", encoding="utf-8") as f:
            j = f.readline()
        NorroenDyrd.index = json.loads(j)

    @staticmethod
    def replaceIndex():
        import json
        import os
        if os.path.exists(NorroenDyrd.ipath):
            os.rename(NorroenDyrd.ipath, NorroenDyrd.ipath + ".old")

        with open(NorroenDyrd.ipath, "w", encoding="utf-8") as f:
            j = json.dumps(NorroenDyrd.index, ensure_ascii=False)
            f.write(j)

    @staticmethod
    def search(seek):
        matches = []
        for h in NorroenDyrd.index:
            counter = 0
            match = {}
            pos = -1
            while True:
                pos = h["text"].find(seek, pos+1)
                if  pos != -1:
                    counter += 1
                else:
                    break
            if counter != 0:
                print("<p>", seek, " : Match found", counter, "times in ", h["title"], "</p>")
                match["title"] = h["title"]
                match["link"] = h["path"]
                match["total"] = counter
                matches.append(match)
        return matches