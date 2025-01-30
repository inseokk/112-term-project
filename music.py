from cmu_graphics import *
import wave

'''
i learned how to use the wave module and how to read binary data from the following links:
https://docs.python.org/3/library/wave.html
https://www.geeksforgeeks.org/reading-binary-files-in-python/ 
https://learnpython.com/blog/plot-waveform-in-python/ 
'''
class Music: 
    def __init__(self, musicFile):
        self.musicFile = musicFile
        self.threshold = 0
        self.intData = []
        self.frameRate = 0
        self.numChannels = 0
        self.visualizedData = []
        self.percentage = 0.99
        self.duration = 0
        self.sorted = []
        self.dataLength = 0

    def findThreshold(self, percentage):
        percentValue = self.sorted[int(percentage*self.dataLength)]
        self.threshold = percentValue
        bpm = self.calculateBPM(self.detectPeaks(percentValue))
        if 0 < bpm <= 300:
            self.threshold = percentValue
            return
        else:
            if bpm <= 0:
                self.percentage *= 0.99
                return 
            elif self.percentage * 1.001 < 1:
                self.percentage *= 1.001
            else:
                return
            self.findThreshold(self.percentage)
        #print(self.percentage, self.threshold)

    def readWaveFile(self):
        """Read the WAV file and extract audio data"""
        with wave.open(self.musicFile, 'rb') as wavFile:
            self.numChannels = wavFile.getnchannels()       #number of audio channels/streams of audio data
            sampleWidth = wavFile.getsampwidth()            #number of bytes representing audio sameple (1: 8-bit, 2: 16-bit)
            self.frameRate = wavFile.getframerate()         #number of audio frames/second
            numFrames = wavFile.getnframes()                #total number of frames in file
            rawData = wavFile.readframes(numFrames)
            self.duration = numFrames/self.frameRate

            # Convert raw binary data to (integer) audio sample values
            for i in range(0, len(rawData), sampleWidth):
                sampleData = rawData[i:i + sampleWidth]
                if sampleWidth == 1:  # 8-bit audio
                    value = sampleData[0] - 128
                elif sampleWidth == 2:  # 16-bit audio
                    value = int.from_bytes(sampleData, byteorder='little', signed=True)
                else:
                    raise ValueError("Unsupported sample width")
                self.intData.append(value)

    def isolateFirstChannel(self):
        """If the audio is multi-channel, reduce it to the first channel"""
        if self.numChannels > 1:
            self.intData = self.intData[::self.numChannels]
        
         # Center and normalize
        meanValue = sum(self.intData) / len(self.intData)
        self.intData = [x - meanValue for x in self.intData]
        maxAmplitude = max(abs(x) for x in self.intData)
        self.intData = [x / maxAmplitude for x in self.intData]
        self.sorted = sorted(self.intData)
        self.dataLength = len(self.intData)


    def visualizeWaves(self):
        self.readWaveFile()
        self.isolateFirstChannel()
        minimum = abs(min(self.intData))
        maximum = max(self.intData)
        maxAmplitude = max(minimum, maximum)
        normalizedRangeData = [sample / maxAmplitude for sample in self.intData]
        resolution = 100
        self.visualizedData = normalizedRangeData[::resolution]
        return self.duration

    def detectPeaks(self, threshold):
        """Detect peaks in the audio data based on the threshold"""
        peaks = []
        for i in range(1, len(self.intData) - 1):
            if (self.intData[i] > threshold and 
                self.intData[i] > self.intData[i - 1] and 
                self.intData[i] > self.intData[i + 1]):
                peaks.append(i)
        return peaks

    def calculateBPM(self, peaks):
        """Calculate BPM from peaks"""
        intervals = [(peaks[i + 1] - peaks[i]) / self.frameRate for i in range(len(peaks) - 1)]
        avgInterval = sum(intervals) / len(intervals) if intervals else 0
        bpm = 60 / avgInterval if avgInterval > 0 else 0
        return bpm

    def analyze(self):
        """Main method"""
        self.readWaveFile()
        self.isolateFirstChannel()
        self.findThreshold(self.percentage)
        print(self.threshold)
        peaks = self.detectPeaks(self.threshold)
        bpm = self.calculateBPM(peaks)
        print(peaks, bpm)
        if bpm>300:
            bpm //= 2
        return bpm



    # def readFile(musicFile):
    #     with wave.open(musicFile, 'rb') as waveFile:
    #         numChannels = waveFile.getnchannels()   #number of audio channels/streams of audio data
    #         sampleWidth = waveFile.getsamplewidth() #number of bytes representing audio sameple (1: 8-bit, 2: 16-bit)
    #         frameRate = waveFile.getframerate()     #number of audio frames/second
    #         numFrames = waveFile.getnframes()       #total number of frames in file
    #         binaryData = waveFile.readframes(numFrames)
    #         totalSamples = numChannels * numFrames
    #         return binaryData, sampleWidth, frameRate, numChannels

    # def binaryToIntgers(data, sampleWidth):
    #     intData = []
    #     for i in range(0, len(data), sampleWidth):  #extract aduio samples
    #         sampleData = data[i:i+sampleWidth]      #binary data of sample
    #         if sampleWidth == 1:
    #             value = sampleData[0]-128
    #         elif sampleWidth == 2:
    #             value = int.from_bytes(sampleData, byteorder='little', signed=True)
    #         else:
    #             return None
    #         intData.append(value)
    #     return intData

    # def detectBeats(intData, threshold):
    #     beats = []
    #     for i in range(1, len(intData)-1):
    #         if (intData[i]> threshold and intData[i]>intData[i-1]
    #             and intData[i]>intData[i+1]):
    #             beats.append(i)
    #     return beats

    # def calculateBpm(beats, frameRate):
    #     timeIntervals = []
    #     for i in range(len(beats)-1):
    #         timeIntervals.append((beats[i+1]-beats[i])/frameRate)
    #     if len(timeIntervals) != 0:
    #         intervalAvg = sum(timeIntervals)/len(timeIntervals)
    #         bpm = 60/intervalAvg
    #     else: 
    #         return 0
    #     return bpm

    # def findBpm(musicFile, threshold = 5000):
    #     binaryData, sampleWidth, frameRate, numChannels = readFile(musicFile)
    #     intData = binaryToIntegers(binaryData, sampleWidth)
    #     if numChannels >1:
    #         intData = intData[::numChannels]
    #     beats = detectBeats(intData, threshold)
    #     bpm = calculateBpm(beats, frameRate)