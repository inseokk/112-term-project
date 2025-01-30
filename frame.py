from cmu_graphics import *
from pages.canvas import *
import time
from PIL import ImageGrab, Image
import pickle

class Frame:
    def __init__(self, frameList, currentFrameDict, musicLength): #currentFrameList #frameList = list of each frame, each frame is a canvas list >> list of lists
        self.frameList = frameList
        self.fps = 1
        self.paused = True
        self.mx = 0
        self.my = 0
        self.canvasHeight= 0
        self.canvasWidth = 0
        self.currentFrameIndex = 0
        self.currentFrameDict = currentFrameDict
        #self.currentFrameList = currentFrameList
        self.step = 0
        self.playUrl = 'images\\playbutton.png'
        self.lineX = 100
        self.musicLength = musicLength
        self.lineSpeed = 500/(musicLength)
        self.startTime = 0
        self.elapsedTime = 0
        self.thumbnails = ['']
        self.step = 25
        
    def changeFps(self, fps):
        self.fps = fps
 
    def addFrames(self):
        self.frameList.append(dict())
        #self.frameList.append([[None for i in  range(500//5)] for j in range(500//5)])
    
    def drawCurrentFrameOutline(self):
        i = self.currentFrameIndex
        length = len(self.frameList)
        drawRect((100 + i*(self.canvasWidth//length)), (self.canvasHeight+100)*1.05, self.canvasWidth//(length)*0.9, 
                     75, fill = None, border = 'pink', borderWidth = 5) 

    def drawPlay(self, canvasWidth, canvasHeight):
        self.canvasWidth = canvasWidth
        self.canvasHeight = canvasHeight
        drawImage(self.playUrl, (canvasWidth+100)*1.07-25, (canvasHeight+100)*0.1-25, width =50, height = 50)

    def drawDisplay(self, canvasHeight, canvasWidth):
        drawRect(100, (canvasHeight+100)*1.05, canvasWidth, 75, fill = 'gray', opacity = 50)
        drawCircle((canvasWidth+100)*1.07, (canvasHeight+100)*1.1, 25, fill = 'pink')
        drawLabel('+', (canvasWidth+100)*1.07, (canvasHeight+100)*1.1, size = 25)

    def drawLine(self):
        drawLine(self.lineX, (self.canvasHeight+100)*1.05, self.lineX, 744, lineWidth = 5)

    def drawThumbnails(self):
        length = len(self.frameList)
        for i in range(len(self.thumbnails)):
            if self.thumbnails[i] == '':
                pass
            else:
                drawImage(self.thumbnails[i], 100+(self.canvasWidth//length)*i,
                            (self.canvasHeight+100)*1.05, width = self.canvasWidth//(length)*0.9, height = 75)

    def drawFramePreviews(self, canvasHeight, canvasWidth):
        self.canvasHeight = canvasHeight
        self.canvasWidth = canvasWidth
        length = len(self.frameList)
        for i in range(length):
            drawRect(100+(canvasWidth//length)*i, (canvasHeight+100)*1.05, canvasWidth//(length)*0.9, 
                     75, fill = None, border = 'black')
            
    def onMousePress(self, mouseX, mouseY):
        self.mx = mouseX
        self.my = mouseY
        if self.pressedOnFrame(mouseX, mouseY) != None:
            self.currentFrameIndex = self.pressedOnFrame(mouseX, mouseY)
            self.currentFrameDict = self.frameList[self.currentFrameIndex]
            self.saveSnapshot(self.currentFrameIndex-1)
            #self.currentFrameList = self.frameList[self.currentFrameIndex]
        if self.pressedOnNewFrame(mouseX, mouseY):
            self.addFrames()
            self.thumbnails.append('')
        if (mouseX-(self.canvasWidth+100)*1.07)**2 + (mouseY-(self.canvasHeight+100)*0.1)**2 <= 25**2: #pressed on play
            self.paused = not self.paused
            if self.startTime == 0:
                self.startTime = time.time()
            else: 
                self.startTime = 0
    
    def pressedOnNewFrame(self, x, y):
        if ((x-(self.canvasWidth+100)*1.07)**2 + (y-(self.canvasHeight+100)*1.1)**2) <= 25**2:
            return True
        return False

    def pressedOnFrame(self, x, y):
        length = len(self.frameList)
        for i in range(length):
            cxLeft, cxRight = 100+(self.canvasWidth//length)*i, 100+(self.canvasWidth//length)*i + self.canvasWidth//(length)*0.9
            cyTop, cyBottom = (self.canvasHeight+100)*1.05, app.height
            if (cxLeft <= x <= cxRight) and (cyTop <= y <= cyBottom):
                return i    #returns the index of the frame that was pressed
            
    def onStep(self):
        if self.step%30 == 0:
            self.saveSnapshot(self.currentFrameIndex)
        if not self.paused:
            self.elapsedTime = time.time()
            progress = (self.elapsedTime-self.startTime) / self.musicLength  # progress as a percentage (0 to 1)
            self.lineX = 100 + 500 * progress
            print(self.lineX, progress)
            self.takeStep()
            
    def takeStep(self):
        # self.step += 1
        # if self.step % 10 == 0:
        # self.currentFrameIndex = 0
        # self.currentFrameList = self.frameList[self.currentFrameIndex]
        if self.currentFrameIndex < len(self.frameList)-1:
            self.currentFrameIndex += 1
            self.currentFrameDict = self.frameList[self.currentFrameIndex]
            #self.currentFrameList = self.frameList[self.currentFrameIndex]
        else:
            #self.currentFrameIndex -= 1
            self.paused = True

    def saveSnapshot(self, i):
        x = 550
        y = 100
        bbox = (x+100, y+100, x+700, y+700)
        snapshot = ImageGrab.grab(bbox)
        snapshot.save(f"snapshotThumbnail.png")
        #print(f"Saved snapshotThumbnail.png")
        pilImage = Image.open(f"snapshotThumbnail.png")
        snapshot = CMUImage(pilImage)
        self.thumbnails[i] = snapshot

    
    def savePickle(fileName, data):
        with open(fileName, 'wb') as file:
            pickle.dump(data, file)
        print(f"Saved {fileName}")