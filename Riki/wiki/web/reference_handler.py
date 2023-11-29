import os

class ReferenceHandler:
    title = ""
    author = ""
    date = ""
    link = ""
    isbn = ""
    page = ""
    basepath = ""
    markdown = ""
    found = False
    def __init__(self, title, author, date, link, isbn, page):
        self.title = title
        self.author = author
        self.date = date
        self.link = link
        self.isbn = isbn
        self.page = page.url
        self.basepath = os.getcwd().replace("\\", "/")
        self.markdown = self.basepath + "/content/" + self.page + ".md"
    def addReference(self):
        reference = self.title + "|" + self.author + "|" + self.date + "|" + self.link + "|" + self.isbn
        with open(self.markdown, "r") as markdown:
            data = markdown.readlines()
            markdown.close()
        index = 0
        for entry in data:
            if entry.startswith("references:"):
                data[index] = data[index].strip() + "; " + reference + "\n"
                self.found = True
                break
            index += 1
        index = 0
        if self.found == False:
            for entry in data:
                print(reference)
                if entry in ['\n', '\r\n']:
                    data[index] = "references: " + reference + "\n\n"
                    break
                index += 1
        with open(self.markdown, "r+") as markdown:
            markdown.writelines(data)