from os import path
from random import shuffle
from utils import genBackdropImage, listMp4

class Channel:
    def __init__(self, root: str, label: str, uri: str, shuffle: bool=True):
        self.root: str = root
        self.label: str = label
        self.uri: str = uri
        self.shuffle: bool = shuffle
        self.items = []
        self.currentIndex = -1
        self.backdropImage = ''
        self.load()
    
    def getLen(self):
        return len(self.items);

    def getLabel(self):
        return self.label;

    def getType(self):
        if(self.uri.lower().startswith(tuple(['file', 'http', 'rtsp', 'rtmp']))):
            return 'url'
        return 'directory';
    
    def load(self):
        self.backdropImage = genBackdropImage(self.label)
        if(self.getType() == 'directory'):
            for file in listMp4(path.join(self.root, self.uri)):
                self.items.append(path.join(self.root, self.uri, file))

        elif(self.getType() == 'url'):
            self.items.append(self.uri)

        if(self.shuffle):
            shuffle(self.items)
        else:
            self.items.sort()
    
    def getItems(self):
        return self.items
    
    def nextVideo(self):
        self.currentIndex += 1
        if (self.currentIndex >= len(self.items)):
            self.currentIndex = 0;
        return self.items[self.currentIndex]

    def getBackdrop(self):
        return self.backdropImage