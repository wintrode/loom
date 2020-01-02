from datetime import datetime as dt

class ToDo :
    def __init__(self) :
        self.title = "Unknown"
        self.description = "Unknown"
        self.added = dt.now()#
        self.labels = {}

    def getAttribute(self, attr) :
        if attr in self.__dict__ :
            return self.__dict__[attr]
        else :
            return ""

    def addLabel(self, label) :
        self.labels[label]=1
        
        
class Task(ToDo) :
    def __init__(self) :
        super().__init__()
        self.complete = False
        self.completedDate = None
        self.dependsOn = [] # can't finish until...
        self.dueDate = None


class Habit(ToDo) :
    def __init(self) :
        super().__init__()
        self.frequency = None
        
class Goal(Task) :
    def __init(self) :
        super().__init__()
        # also has depends on and completed

class Mission :
    # supported by goals, chores, habits
    # 
    def __init__(self, name) :
        self.name = name
        self.description = None

class Label :
    def __init__(self, name) :
        self.name = name
        self.notes = []
        
    
