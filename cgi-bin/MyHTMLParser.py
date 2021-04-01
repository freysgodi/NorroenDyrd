from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    tFlag = False
    plaintext = ""
    title = ""

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.tFlag = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.tFlag = False

    def handle_data(self, data):
        if self.tFlag:
            self.title = data
        else:
            self.plaintext = self.plaintext + data
