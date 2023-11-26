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
        elif self.fileName.lower().endswith(('.mp3', '.mp4')):
            handler = VideoHandler(self.originalFile, self.page)
            handler.saveFile()
        elif self.fileName.lower().endswith(('.doc', '.docx', '.pdf')):
            handler = DocumentHandler(self.originalFile, self.page)
            handler.saveFile()
        else:
            return "Invalid file type"

# Image handler
class ImageHandler(FileHandler):
    basepath = ""
    path = ""
    markdown = ""
    found = False
    def __init__(self, originalFile, page):
        self.originalFile = originalFile
        self.fileName = secure_filename(originalFile.filename)
        self.page = page
        self.basepath = os.getcwd().replace("\\", "/")
        self.path = self.basepath + "/wiki/web/files/" + self.page + "/images/"
        self.markdown = self.basepath + "/content/" + self.page + ".md"
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
                data[index] = data[index].strip() + ", " + self.path + self.fileName + "\n"
                self.found = True
                break
            index += 1
        index = 0
        if self.found == False:
            for entry in data:
                if entry in ['\n', '\r\n']:
                    print(True)
                    data[index] = "images: " + self.path + self.fileName + "\n"
                break
            index += 1
        with open(self.markdown, "r+") as markdown:
            markdown.writelines(data)          

# Video handler
class VideoHandler(FileHandler):
    basepath = ""
    path = ""
    markdown = ""
    def __init__(self, originalFile, page):
        self.originalFile = originalFile
        self.fileName = secure_filename(originalFile.filename)
        self.page = page
        self.basepath = os.getcwd().replace("\\", "/")
        self.path = self.basepath + "/wiki/web/files/" + self.page + "/videos/"
        self.markdown = self.basepath + "/content/" + self.page + ".md"
    def saveFile(self):
        fullPath = self.path + self.fileName
        os.makedirs(os.path.dirname(fullPath), exist_ok=True)
        with open(self.path + self.fileName, "wb") as newFile:
            newFile.write(self.originalFile.stream.read())
        details = open(self.markdown)
        
# Document handler
class DocumentHandler(FileHandler):
    basepath = ""
    path = ""
    markdown = ""
    def __init__(self, originalFile, page):
        self.originalFile = originalFile
        self.fileName = secure_filename(originalFile.filename)
        self.page = page
        self.basepath = os.getcwd().replace("\\", "/")
        self.path = self.basepath + "/wiki/web/files/" + self.page + "/documents/"
        self.markdown = self.basepath + "/content/" + self.page + ".md"
    def saveFile(self):
        fullPath = self.path + self.fileName
        os.makedirs(os.path.dirname(fullPath), exist_ok=True)
        with open(self.path + self.fileName, "wb") as newFile:
            newFile.write(self.originalFile.stream.read())
        details = open(self.markdown)