# -*- coding: utf-8 -*-
# MENU: Experiments/Record Trap Test

from .Translate import Translate
import json
import datetime as dt
import numpy as np

class RecordTrapTest(Translate):
    
    """
    Translate subclasses Move. Has parameter dr, and inherits smooth and stepSize from Move.
    Translate moves traps by dr (a 3-tuple or list). If smooth=False, this occurs instantaneously; if smooth=True, this occurs in increments of stepSize.
    self.nframes is automatically reset to int(|dr|/stepSize)
    Example: If you want to move traps by (0, 0, 0.5) each frame for 200 frames, then set dr=(0, 0, 100.) and stepSize=0.5
    """
    
    def __init__(self,  filename=None, **kwargs):
        super(RecordTrapTest, self).__init__(**kwargs)
        self.filename = filename
        self.dx = -500.
        self.dy = 100.           
        self.dz = -200.
        self.stepSize = 1
        self.mpp=1. #### mpp=1 means stepSize is in units of pixels 
                                        
    def initialize(self, frame):
        if self.traps is None or (isinstance(self.traps, list) and len(self.traps) == 0):
            self.traps = self.parent().pattern.prev   #### Or self.parent().pattern.traps for all traps
        super(RecordTrapTest, self).initialize(frame)
        self.recordtrajs = self.trajectories.copy()        #### Save parameterized trajectories; make place to store trap positions
        
        self.out = []        
        time = dt.datetime.now()
        if self.filename is None:                     #### If filename not provided, get it from timestamp
            self.filename = str(time)[:10]            #### Base name
            videoname = self.filename + '.avi'        #### Video name
            self.filename += '--' + str(time)[11:-7]  #### Serial name
        else:
            videoname = self.filename + '.avi'        #### Otherwise, use filename.avi and filename.json
        record = self.register('Record', fn=videoname, blocking=False, nframes=self.nframes)    
        record.pause(self._paused)
        
    def process(self, frame):
        super(RecordTrapTest, self).process(frame)
        self.out.append([(trap.r.x(), trap.r.y(), trap.r.z()) for trap in self.traps])

    def complete(self):
        with open(self.filename + '.json', 'w') as myfile:
             json.dump(self.out, myfile)
        print('Traps were recorded to be at')
        print(self.out)
        print('And the trajectories were')
        print(self.recordtrajs)
        
                
        
# from .QExperiment import QExperiment
# import json
# import datetime as dt

# class RecordTrapTest(QExperiment):
    
#     def __init__(self, info=None, loop=1, **kwargs):
#         super(RecordTrapTest, self).__init__(**kwargs)
#         self.info = info or 'RecordTrapTest.json'
#         print(self.info)
                                        
#     def initialize(self, frame):
#         super(RecordTrapTest, self).initialize(frame)
#         time = dt.datetime.now()
#         self.tasks[0].fn = str(time)[:10] + '.avi'
#         self.tasks[0].widget.updateUi()
      
