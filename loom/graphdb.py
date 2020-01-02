from py2neo import Graph, Node, Relationship, NodeMatcher
import sys

import loom.todos as ltd

class GraphDB :

    def __init__(self, host, port, user, passwd) :
        self.url = "http://%s:%s@%s:%d/db/data" % (user, passwd, host, port)
        self.graph = Graph(self.url)
        self.bolt = "bolt://%s:7687" % (host)
        #"http://neo4j:neo123@localhost:7474/db/data")
        self.user = user
        self.passwd = passwd
        self.labels = {}
        
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
        return list(self.labels)
    
    def getTopTasks(self) :
        matcher = NodeMatcher(self.graph)
        m = matcher.match("Task")
        nodes = []
        for (i,n) in enumerate(m) :
            #print("%d: " % (i+1), format(n))
            td = ltd.ToDo()
            td.title=n['title']
            td.description=n['description']
            if "labels" in n :
                self.addLabels(td, n['labels'])
            nodes.append(td)

        return nodes


    def addTask(self, title, type="Task", description="", labels=[]) :
        task  = Node(type, title=title, description=description)
        #click.echo("Creating %s: '%s' " % (type, title))
        if len(labels) > 0 :
            task["labels"]=labels
        self.graph.create(task)
