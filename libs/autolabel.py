try:
    import cv2
except ImportError:
    pass

class Cv2AutoLabel(object):
    def __init__(self, algname='KCF'):
        self._algname = algname
        self._trackers = None
        self._lastFramePath = None
        self._lastObjs = None
    
    def initTrackers(self, lastFramePath, lastObjs):
        #self._trackers = cv2.MultiTracker(self._algname)
        #frame = cv2.imread(framePath)
        #self._trackers.add(frame, objects)
        self._trackers = []
        frame = cv2.imread(lastFramePath)
        for obj in lastObjs:
            t = cv2.Tracker_create(self._algname)
            ok = t.init(frame, obj)
            self._trackers.append(t)
        self._lastFramePath = lastFramePath
        self._lastObjs = lastObjs
        
    def update(self, currentFramePath, lastFramePath, lastObjs):
        if self._trackers is not None:
            if (self._lastFramePath!=lastFramePath) or (len(self._lastObjs)!=len(lastObjs)):
                self.clear()
                self._trackers = None
                print("AutoAnnotation reset: Last file changed")
            else:
                for i,obj in enumerate(lastObjs):
                    if self._lastObjs[i] != obj:
                        self.clear()
                        self._trackers = None
                        print("AutoAnnotation reset: Objects changed")
                        break
        if self._trackers is None:
            self.initTrackers(lastFramePath, lastObjs)
        frame = cv2.imread(currentFramePath)
        height = len(frame)
        width = len(frame[0])
        objs = []
        for t in self._trackers:
            ok, obj = t.update(frame)
            x,y,w,h = obj
            w = min(w, width-x-1)
            h = min(h, height-y-1)
            obj = (x,y,w,h)
            objs.append(obj)
        self._lastFramePath = currentFramePath
        self._lastObjs = objs
        #ok, objects = self._trackers.update(frame)
        #if ok:
        #    self._objects = objects
    
    def clear(self):
        for t in self._trackers:
            t.clear()
    
    @property
    def objects(self):
        return self._lastObjs
        #return self._trackers.objects

class DummyAutoLabel(object):
    def __init__(self, algname='KCF'):
        pass
        
    def update(self, currentFramePath, lastFramePath, lastObjs):
        self._lastObjs = lastObjs
    
    @property
    def objects(self):
        return self._lastObjs

def getInstancce(algname='KCF'):
    try:
        _v = cv2.__version__
        return Cv2AutoLabel(algname)
    except:
        print("Autolabel engine fallback to DumyAutoLabel")
        return DummyAutoLabel(algname)
