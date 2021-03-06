from py2neo import Graph, Node, Relationship, NodeMatcher
import sys
import uuid
from datetime import datetime as dt
import loom

def format(n) :
    return str(n)

def list_nodes(graph, type="Task", filter=None) :
    print("Current %ss:" % (type))
    matcher = NodeMatcher(graph)
    m = matcher.match(type)
    nodes = []
    for (i,n) in enumerate(m) :
        print("%d: " % (i+1), format(n))
        nodes.append(n)
    return nodes

def add_property(graph, node, name, value) :
    node[name]=value
    graph.push(node)

def add_task(graph, title, type="Task", description="") :
    task  = Node(type, title=title, description=description)
    print("Creating %s: '%s' " % (type, title))
    graph.create(task)

def prompt() :
    sys.stdout.write("%> ");
    sys.stdout.flush()
    line = sys.stdin.readline()
    if line is None or line.strip() == ""  or line.strip() == "done" :
        return None
    return line.strip()


graph = Graph("http://neo4j:neo123@localhost:7474/db/data")

resp = prompt()
nodes = []
while resp != None :
    args = resp.strip().split()
    if args[0] == "list":
        type="Task"
        if len(args) > 1 :
            type=args[1]
        nodes = list_nodes(graph, type=type)
        for n in nodes :
            if 'id' not in n :
                n['id']=uuid.uuid1().hex[:16]
                graph.push(n)
            if 'added' not in n :
                n['added'] = dt.now().strftime(loom.ISOFMT)
                graph.push(n)
            if 'complete' not in n :
                n['complete'] = False
                graph.push(n)
                
    elif args[0] == "del" :
        if len(args) > 1 and args[1] == "all" :
            sys.stderr.write("Are you sure? (y/n)\n")
            resp=prompt()
            if (resp == "y") :
                graph.delete_all()
        elif len(args) > 1 :                        
            n = int(args[1])-1
            if n < len(nodes) :
                print("Deleting Task('%s')" %(nodes[n]['title']))
                graph.delete(nodes[n])


    elif args[0] == "dep" :
        if len(args) > 1 :
            tgt = int(args[1])-1
            for dep in args[2:] :
                n = int(dep)-1
                if n < len(nodes) and tgt < len(nodes):
                    print("Task('%s') <- Task('%s')" %(nodes[tgt]['title'], nodes[n]['title']))
                    a_dep_b = Relationship(nodes[tgt], "depends_on", nodes[n])
                    graph.create(a_dep_b)

    elif args[0] == "done" :
        if len(args) > 1 :
            id = int(args[1])
            if (id > 0 and id <= len(nodes)) :
                #print(nodes[id-1])
                add_property(graph, nodes[id-1], "Done", True)
                
    elif args[0] == "add" or args[0] == "add-goal" :
        if (args[0]=="add") :
            type= "Task"
        else:
            type = "Goal"
            
        if len(args) < 2 :
            sys.stdout.write("usage: add[-goal] [Title]\n");
            resp = prompt()
            
        title = " ".join(args[1:])
        sys.stdout.write("Enter a description for '%s', end with a single \".\"\n" % (title))
        resp = prompt()
        desc = []
        while (resp != ".") :
            if resp == None : resp=""
            desc.append(resp)
            resp = prompt()

        description = "\n".join(desc)
        add_task(graph, title, type=type, description = description)
        
    elif args[0] == "quit" or args[0] == "exit" :
        break
        
        
    resp=prompt()


#german = Node("Langauge", name="German")
#graph.create(german)
#speaks = Relationship(alice, "SPEAKS", german)
#graph.create(speaks)


