from element import Element
import sys
import numpy as np


class Process(Element):

    def __init__(self, delay: float, channels = 1, max_queue = sys.maxsize, distribution = "", name = None):
        super().__init__(delay) 
        self.queue = 0 
        self.name = name
        if self.name is None:
            self.name = "PROCESS"+str(self.id) 
        self.mean_queue = 0.0 
        self.busy_time = 0.0
        #no failure: 0, yes failure : 1
        self.failure = 0
        self.proba = [1]
        self.max_queue = max_queue
        self.channels = channels
        self.distribution = distribution
        self.states = []
        for i in range(self.channels):
            self.states.append(0)
        self.tnext = []
        for i in range(self.channels):
            self.tnext.append(sys.float_info.max)

    def onStart(self):
        #find free place in process
        #if at least one channel is free
        if 0 in self.states:
            for i in self.states:
                if self.states[i] == 0:
                    self.states[i] = 1
                    self.tnext[i] = self.tcurr + self.delay_mean
                    #self.next element id = get.id
                    break

        else:
            if self.get_queue() < self.get_maxqueue():
                self.set_queue(self.get_queue() + 1) 
        
            else:
                self.failure+=1

    def onFinish(self):
        super().onFinish()

        id = None
        for id in range(self.channels):
            if self.tnext[id] == self.tcurr:
                break
                
        #quantity ++

        self.tnext[id] = sys.float_info.max
        self.states[id] = 0

        if self.queue > 0:
            self.queue -= 1
            self.states[id] = 1
            self.tnext[id] = self.tcurr + self.delay_mean
        
        #find next element with consider. to probas
        if self.next_element is not None:
            next_element = None
            if type(self.next_element) is Process or len(self.next_element) == 1:
                #why choose one
                next_element = self.next_element
            else:  
                #type is list
                next_element = np.random.choice(a=self.next_element, p=self.proba)

            next_element.onStart()

    def define_proba_branch(self, proba = [1], nextElements = None):
        self.proba = proba
        self.next_element = nextElements

    def getNextEventTime():
        pass
    
    def get_failure(self):
        return self.failure 
    
    def get_queue(self):
        return self.queue 
    
    def set_queue(self, queue: int):
        self.queue = queue 
    
    

    def get_maxqueue(self)-> int:  
        return self.max_queue 
    
    def set_maxqueue(self, maxqueue:int):
        self.max_queue = maxqueue 
    
    def print_info(self):
        
        print(self.name + " states= " + str(self.states) +
                " quantity = " + str(self.quantity) +
                " tnext= " + str(self.tnext))
        print("failure = " + str(self.failure) )
    

    def do_stats(self, delta: float):
        self.mean_queue = self.get_mean_queue() + self.queue * delta 
        for i in range(self.channels):
            self.busy_time = self.get_busy_time()+ delta * self.states[i]
        self.busy_time = self.busy_time / self.channels

    def get_busy_time(self):
        return self.busy_time     
    
    def get_mean_queue(self):
        return self.mean_queue 