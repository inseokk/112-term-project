from cmu_graphics import *
from music import *
import os, pathlib
from images import *
import tkinter as tk
from tkinter import filedialog 
from PIL import ImageGrab, Image

def loadSound(relativePath):
        # Convert to absolute path (because pathlib.Path only takes absolute paths)
        absolutePath = os.path.abspath(relativePath)
        # Get local file URL
        url = pathlib.Path(absolutePath).as_uri()
        # Load Sound file from local URL
        return Sound(url)

class MusicVisuals:
    def __init__(self, url):
        self.url = url
        self.urlLoaded = False
        self.sound = Sound('rumo-ao-sol-13162-VEED.wav')
        self.paused = True
        self.music = Music('rumo-ao-sol-13162-VEED.wav')
        self.canvasH = 0
        self.canvasW = 0
        self.addMusic = False
        self.duration = self.music.visualizeWaves()
        self.wavesLength = len(self.music.visualizedData)
        self.bpm = self.music.analyze()
        self.musicIcon = r'images\music.PNG'
        self.musicLoaded = True
        self.waveSnapshot = ''
        self.step = 0
    
    def draw(self, canvasH, canvasW):
        self.canvasH = canvasH
        self.canvasW = canvasW
        self.drawMusicImport()
        if self.musicLoaded:
            self.drawWave(canvasH, canvasW)
        else:
            if self.waveSnapshot != '':
                drawImage(self.waveSnapshot, 100, (canvasH+100)*1.05+79)
        if self.addMusic:
            self.drawAddMusic()
        drawRect(98, (canvasH+100)*1.05+80, canvasW+4, app.height-(canvasH+160)*1.1, fill = None, border = 'lightSeaGreen')

    def drawWave(self, canvasH,canvasW):
        scalingFactor = (app.height-(canvasH+160)*1.1)/2
        for i in range(len(self.music.visualizedData)-1):
            x1 = 100 + i * (canvasW) / len(self.music.visualizedData)
            x2 = 100 + (i+1) * (canvasW) / len(self.music.visualizedData)
            y1 = (canvasH+100)*1.21 - self.music.visualizedData[i] * scalingFactor
            y2 = (canvasH+100)*1.21 - self.music.visualizedData[i+1] * scalingFactor
            drawLine(x1, y1, x2, y2, fill = 'steelBlue')
            if self.step >=20:
                self.musicLoaded = False

    def drawMusicImport(self):
        drawImage(self.musicIcon, 48, 60, width = 50, height = 50, align = 'center')
        drawLabel(f'bpm {int(self.bpm)}', 125, (self.canvasH+100)*0.08, align = 'left')

    def isMusicPressed(self, x, y):
        return 48<=x<=48+50 and 60<=y<=60+50
    
    def isAddingMusic(self, x, y):
        xLeft, xRight = (self.canvasW+100)*0.09, (self.canvasW+100)*0.09+130
        yTop, yBottom = (self.canvasH+100)*0.1, (self.canvasH+100)*0.13+17 
        return (xLeft<=x<=xRight) and (yTop<=y<=yBottom)
    
    def onMousePress(self, x, y, paused):
        if self.isMusicPressed(x, y):
            self.url = self.openFile()
            self.sound = Sound(self.url)
            self.music = Music(self.url)
            self.duration = self.music.visualizeWaves()
            self.wavesLength = len(self.music.visualizedData)
            self.bpm = self.music.analyze()
            self.step = 0
            self.musicLoaded = True
        self.paused = paused
        if not self.paused:
            self.sound.play(restart=False, loop=False)
        # elif self.sound.play(): 
        #     self.sound.pause()

    def openFile(self):
        root = tk.Tk()
        root.withdraw() 
        musicFilePath = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("Sound File", "*.wav")]
        )
        return musicFilePath
    
    def onStep(self):
        self.step +=1
        if self.musicLoaded == False:
            if self.step >= 20:
                self.saveSnapshot()
                self.musicLoaded = None

    def saveSnapshot(self):
        x = 551
        y = 250
        bbox = (x+98, y+710, x+602, y+744)
        firstSnapshot = ImageGrab.grab(bbox)
        firstSnapshot.save(f"snapshot1_musicWave.png")
        print(f"Saved snapshot1_musicWave.png")
        pilImage = Image.open(f"snapshot1_musicWave.png")
        self.waveSnapshot = CMUImage(pilImage)