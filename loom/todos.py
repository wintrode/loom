from datetime import datetime as dt

class ToDo :
    def __init__(self, title, desc, added, labels={}) :
        self.title = title
        self.description = desc
        self.added = added
        self.labels = {}
        if labels :
            if isinstance(labels, list):
                for l in labels :
                    self.labels[l]=1
            else :
                for l in labels :
                    self.lxabels[l]=labels[l]
        
        
    def getAttribute(self, attr) :
        if attr in self.__dict__ :
            return self.__dict__[attr]
        else :
            return ""

    def addLabel(self, label) :
        self.labels[label]=1


    def to_json(self) :
        d = {}
        for n in self.__dict__ :
            if n == "depends_on" :
                d[n]=[]
                if len(self.depends_on) > 0 :
                    for m in self.depends_on :
                        d[n].append([m.idx, m.get_type()])
            else :
                d[n]=self.__dict__[n]        
        return d
        
class Task(ToDo) :

    def __init__(self, title, desc, added, labels={},
                 complete=False, completed=None, deps=[], due=None) :
        super().__init__(title, desc, added, labels=labels)
        self.complete = complete
        self.completed_date = completed
        self.depends_on = [] # can't finish until...
        if deps :
            for d in deps :
                self.depends_on.append(d)
        self.due_date = due

    def new_task() :
        return Task('unk', 'unk', dt.now())

class Habit(ToDo) :
    def __init(self) :
        super().__init__()
        self.frequency = None
        
class Goal(Task) :
    def __init__(self, title, desc, added, labels={},
                 complete=False, completed=None, deps=[], due=None) :
        super().__init__(title, desc, added, labels=labels,
                         complete=complete, completed = completed,
                         deps = deps, due=due)
        
    def new_goal() :
        return Goal('unk', 'unk', dt.now())
    
        
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
        
    
def from_dict(attrs, tp = "Task") :
    name = desc = None
    req = ["id", "title", "description"]
    notreq = ["labels", "depends_on", "completed_date", "due_date"]
    if 'type' in attrs :
        tp  = attrs['type']
    elif tp is None :
        return None

    for a in req :
        if a not in attrs :
            # missing required attribute
            return None
    for a in notreq :
        if a not in attrs:
            attrs[a]=None

    print(attrs);
            
    if tp == "Goal" :
        return Goal(attrs['title'], attrs['description'],
                    attrs['added'], labels=attrs['labels'],
                    complete=(False or attrs['complete']),
                    completed=attrs['completed_date'],
                    deps=attrs['depends_on'], due=attrs['due_date'])

    else :
        return Task(attrs['title'], attrs['description'],
                    attrs['added'], labels=attrs['labels'],
                    complete=(False or attrs['complete']),
                    completed=attrs['completed_date'],
                    deps=attrs['depends_on'], due=attrs['due_date'])

    
