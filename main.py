from cmu_graphics import *
from pages.basePage import Page
from pages.home import HomePage
from pages.canvas import Canvas
from music import Music
from frame import *
from images import *
from PIL import ImageGrab
import tkinter as tk
import ctypes
import pickle

'''
used to learn how to screenshot using PIL : https://www.geeksforgeeks.org/python-pil-imagegrab-grab-method/
used to learn how to use pickle module: https://www.datacamp.com/tutorial/pickle-python-tutorial
used to learn how to import files: https://www.geeksforgeeks.org/create-an-import-file-button-with-tkinter/# 
'''

class PageManager:
    def __init__(self, app):
        # Initialize pages
        self.app = app
        self.app.width = 500
        self.app.height = 500
        self.pages = dict()
        self.pages['home'] = HomePage(app)
        self.pages['canvas'] = Canvas(app)
        self.currentPage = 'home'
        self.app.createNewButton = 'False'
        self.thumbList = []
        self.filePath = None


    def draw(self):
        # draw the current page
        self.pages[self.currentPage].draw()

    def onMousePress(self, mouseX, mouseY):
        # mouse press events to the current page
        self.pages[self.currentPage].onMousePress(mouseX, mouseY)
        if self.currentPage == 'home':
            self.importPage = self.pages[self.currentPage].importPage
            self.currentPage = self.pages[self.currentPage].currentPage
            if self.importPage:
                self.filePath = self.pages['home'].filePath
                self.pages['canvas'].pastProjectUrl = self.filePath
        # else:
        #     self.app.thumbList = self.pages['canvas'].frame.thumbnails

    def onMouseDrag(self, mouseX, mouseY):
        self.pages[self.currentPage].onMouseDrag(mouseX, mouseY)

    def onMouseRelease(self, mouseX, mouseY):
        self.pages[self.currentPage].onMouseRelease(mouseX, mouseY)

    def onKeyPress(self, key):
        # key press events to the current page
        self.pages[self.currentPage].onKeyPress(key)
        if key == 'escape':
            self.currentPage = 'home'
    
    def isCreateButtonPressed(self, x, y):
        return self.pages[self.currentPage].whereMouseClicked(x,y)

    def createdCanvas(self, x, y):
        return self.pages[self.currentPage].whereMouseClicked(x, y)

    def onStep(self):
        self.pages[self.currentPage].onStep()

# create page manager
def onAppStart(app):
    app.pageManager = PageManager(app)
    app.stepsPerSecond = 1
    app.setMaxShapeCount(4000)
    app.musicUrl = ''
    app.step = 97

def redrawAll(app):
    app.pageManager.draw()

def onMousePress(app, mouseX, mouseY):
    app.pageManager.onMousePress(mouseX, mouseY)

def onMouseDrag(app, mouseX, mouseY):
    app.pageManager.onMouseDrag(mouseX, mouseY)

def onMouseRelease(app, mouseX, mouseY):
    if app.pageManager.currentPage == 'canvas':
        app.pageManager.onMouseRelease(mouseX, mouseY)

def onKeyPress(app, key):
    app.pageManager.onKeyPress(key)
    if app.pageManager.currentPage == 'canvas':
        app.musicUrl = app.pageManager.pages['canvas'].musicUrl
        print(app.musicUrl)

def onStep(app):
    # if app.step%100 == 0:
    #     # x, y, w, h = getCaptureWindow()
    #     # saveSnapshot(app, app.step)
    #     savePickle(f"frameList{app.step}.pkl", app.pageManager.thumbList)
    app.pageManager.onStep()
    app.step += 1

# def saveSnapshot(app, step):
#     user32 = ctypes.windll.user32
#     screensize = user32.GetSystemMetrics(16), user32.GetSystemMetrics(17)
#     print(screensize)
#     x = 100
#     y = 100
#     x, y = screensize
#     width = app.width
#     height = app.height
#     width = app.width
#     height = app.height
#     bbox = (0, 0, x, y)
#     snapshot = ImageGrab.grab(bbox)
#     snapshot.save(f"snapshot_{step}.png")
#     print(f"Saved snapshot_{step}.png")

# def getCaptureWindow():
#     # windowX = root.winfo_rootx()  # x coordinate of the top-left corner
#     # windowY = root.winfo_rooty()  # y coordinate of the top-left corner
#     # windowW = root.winfo_width()  # Width of the window
#     # windowH = root.winfo_height()  # Height of the window
#     x = 0
#     y = 0
#     width=700
#     height=760
#     # print(windowX, windowY, width, height)
#     return x, y, width, height


def savePickle(fileName, data):
    with open(fileName, 'wb') as file:
        pickle.dump(data, file)
    print(f"Saved {fileName}")

def main():
    runApp()

main()