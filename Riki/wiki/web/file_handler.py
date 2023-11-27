import os
from werkzeug.utils import secure_filename
from pprint import pprint

# Base file handler
class FileHandler:
    originalFile = ""
    fileName = ""
    page = ""
    def __init__(self, originalFile, page):
        self.originalFile = originalFile
        self.fileName = secure_filename(originalFile.filename)
        self.page = page.url
    def sortFile(self):
        if self.fileName.lower().endswith(('.png', '.jpg', '.jpeg')):
            handler = ImageHandler(self.originalFile, self.page)
            handler.saveFile()
        elif self.fileName.lower().endswith(('.mp4')):
            handler = VideoHandler(self.originalFile, self.page)
            handler.saveFile()
        elif self.fileName.lower().endswith(('.doc', '.docx', '.pdf', '.txt')):
            handler = DocumentHandler(self.originalFile, self.page)
            handler.saveFile()
        else:
            return "Invalid file type"

# Image handler
class ImageHandler(FileHandler):
    basepath = ""
    path = ""
    markdown = ""
    url = ""
    found = False
    def __init__(self, originalFile, page):
        self.originalFile = originalFile
        self.fileName = secure_filename(originalFile.filename)
        self.page = page
        self.basepath = os.getcwd().replace("\\", "/")
        self.path = self.basepath + "/wiki/web/static/files/" + self.page + "/images/"
        self.markdown = self.basepath + "/content/" + self.page + ".md"
        self.url = "/static/files/" + self.page + "/images/"
    def saveFile(self):
        fullPath = self.path + self.fileName
        os.makedirs(os.path.dirname(fullPath), exist_ok=True)
        with open(self.path + self.fileName, "wb") as newFile:
            newFile.write(self.originalFile.stream.read())
        with open(self.markdown, "r") as markdown:
            data = markdown.readlines()
            markdown.close()
        index = 0
        for entry in data:
            if entry.startswith("images:"):
                data[index] = data[index].strip() + ", " + self.url + self.fileName + "\n"
                self.found = True
                break
            index += 1
        index = 0
        if self.found == False:
            for entry in data:
                print(entry)
                if entry in ['\n', '\r\n']:
                    data[index] = "images: " + self.url + self.fileName + "\n"
                    break
                index += 1
        with open(self.markdown, "r+") as markdown:
            markdown.writelines(data)          

# Video handler
class VideoHandler(FileHandler):
    basepath = ""
    path = ""
    markdown = ""
    url = ""
    found = False
    def __init__(self, originalFile, page):
        self.originalFile = originalFile
        self.fileName = secure_filename(originalFile.filename)
        self.page = page
        self.basepath = os.getcwd().replace("\\", "/")
        self.path = self.basepath + "/wiki/web/static/files/" + self.page + "/videos/"
        self.markdown = self.basepath + "/content/" + self.page + ".md"
        self.url = "/static/files/" + self.page + "/videos/"
    def saveFile(self):
        fullPath = self.path + self.fileName
        os.makedirs(os.path.dirname(fullPath), exist_ok=True)
        with open(self.path + self.fileName, "wb") as newFile:
            newFile.write(self.originalFile.stream.read())
        with open(self.markdown, "r") as markdown:
            data = markdown.readlines()
            markdown.close()
        index = 0
        for entry in data:
            if entry.startswith("videos:"):
                data[index] = data[index].strip() + ", " + self.url + self.fileName + "\n"
                self.found = True
                break
            index += 1
        index = 0
        if self.found == False:
            for entry in data:
                print(entry)
                if entry in ['\n', '\r\n']:
                    data[index] = "videos: " + self.url + self.fileName + "\n\n"
                    break
                index += 1
        with open(self.markdown, "r+") as markdown:
            markdown.writelines(data)

# Document handler
class DocumentHandler(FileHandler):
    basepath = ""
    path = ""
    markdown = ""
    url = ""
    found = False
    def __init__(self, originalFile, page):
        self.originalFile = originalFile
        self.fileName = secure_filename(originalFile.filename)
        self.page = page
        self.basepath = os.getcwd().replace("\\", "/")
        self.path = self.basepath + "/wiki/web/static/files/" + self.page + "/documents/"
        self.markdown = self.basepath + "/content/" + self.page + ".md"
        self.url = "/static/files/" + self.page + "/documents/"
    def saveFile(self):
        fullPath = self.path + self.fileName
        os.makedirs(os.path.dirname(fullPath), exist_ok=True)
        with open(self.path + self.fileName, "wb") as newFile:
            newFile.write(self.originalFile.stream.read())
        with open(self.markdown, "r") as markdown:
            data = markdown.readlines()
            markdown.close()
        index = 0
        for entry in data:
            if entry.startswith("documents:"):
                data[index] = data[index].strip() + ", " + self.url + self.fileName + "\n\n"
                self.found = True
                break
            index += 1
        index = 0
        if self.found == False:
            for entry in data:
                print(entry)
                if entry in ['\n', '\r\n']:
                    data[index] = "documents: " + self.url + self.fileName + "\n\n"
                    break
                index += 1
        with open(self.markdown, "r+") as markdown:
            markdown.writelines(data)
            