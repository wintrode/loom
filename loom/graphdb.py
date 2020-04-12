from py2neo import Graph, Node, Relationship, NodeMatcher
import sys
import datetime
import uuid
from functools import cmp_to_key
from datetime import datetime as dt

import loom.todos as ltd
import loom

SHELF = "shelf"

class GraphDB :

    def __init__(self, host, port, user, passwd) :
        self.url = "http://%s:%s@%s:%d/db/data" % (user, passwd, host, port)
        self.graph = Graph(self.url)
        self.bolt = "bolt://%s:7687" % (host)
        #"http://neo4j:neo123@localhost:7474/db/data")
        self.user = user
        self.passwd = passwd
        self.labels = {}
        self.filters = {}
        
    def getBolt(self) :
        return self.bolt

    def getCreds(self) :
        return (self.user, self.passwd)

    def addLabels(self, todo, labels) :
        for l in labels :
            todo.addLabel(l)
            if l not in self.labels :
                self.labels[l]=1
            else:
                self.labels[l] += 1


    def getLabels(self) :
        print(self.labels)
        return list(self.labels)

    def getFilters(self) :
        return list(self.filters)

    def getNode(self, ttype, uid) :
        matcher = NodeMatcher(self.graph)
        m = matcher.match(ttype, id=uid)
        if len(m)>0 :
            d = {}
            n = m.first()
            for attr in list(n) :
                d[attr]=n[attr]
            return ltd.from_dict(d, tp=ttype)
        return None

    def updateNode(self, ttype, uid, content) :
        matcher = NodeMatcher(self.graph)
        m = matcher.match(ttype, id=uid)
        print("updating node ", uid, content)
        if len(m)>0 :
            n = m.first()
            for c in content : # do some checking here
                if c == "idx" : continue
                n[c] = content[c]
            self.graph.push(n)

    def node_cmp(self, a, b) :
        # complete at bottom
        if a.complete and not b.complete :
            return 1
        elif b.complete and not a.complete :
            return -1

        if SHELF in a.labels and SHELF not in b.labels :
            return 1
        elif SHELF in b.labels and SHELF not in a.labels :
            return -1
        
        if a.due_date and b.due_date :
            if a.due_date == b.due_date :
                if a.added < b.added :
                    return -1
                elif a.added > b.added :
                    return 1
                else :
                    return 0
            elif a.due_date > b.due_date :
                return 1
            else :
                return -1
        elif a.due_date and not b.due_date :
            return -1
        else :
            return 1
        
            
    def getTopTasks(self, ttype = "Task") :
        matcher = NodeMatcher(self.graph)
        m = matcher.match(ttype)
        nodes = []
        for (i,n) in enumerate(m) :
            #print("%d: " % (i+1), format(n))
            if ttype== "Goal" :
                td = ltd.Goal.new_goal()
            else :
                td = ltd.Task.new_task()

            td.idx = i
            if "id" not in n :
                n["id"]= "unk"
            td.id = n['id'] 
            td.title=n['title']
            td.complete = n['complete']
            td.description=n['description']
            if "labels" in n :
                self.addLabels(td, n['labels'])
            if 'added' in n :
                td.added = dt.strptime(n['added'], loom.ISOFMT)
            if 'due_date' in n :
                td.due_date = dt.strptime(n['due_date'], loom.ISOFMT)
                
            nodes.append(td)

        return sorted(nodes, key=cmp_to_key(self.node_cmp))


    def addTask(self, title, type="Task", description="", labels=[], due=None) :
        task  = Node(type, title=title, description=description)
        sys.stderr.write("Creating %s: '%s %s'\n" % (type, title, str(due)))
        if len(labels) > 0 :
            task["labels"]=labels

        task["added"] = dt.now().strftime(loom.ISOFMT)
        if due is not None and isinstance(due, datetime.date) :
            task["due_date"] = due.strftime(loom.ISOFMT)

        task["complete"]=False

        # create UID
        task["id"] = uuid.uuid1().hex[:16]
        
        self.graph.create(task)
