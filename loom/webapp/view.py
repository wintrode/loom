import sys
import click
from datetime import datetime, timedelta

class View :
    def __init__(self, ttype) :
        self.headers=[('Done', 'complete'), ('Title','title'), ('Added', 'added'),
                      ('Due','due_date'), ('Description', 'description'),
                      ('Labels', 'labels')]
        self.ttype = ttype;
        
    def getHeaders(self) :
        return self.headers;


    def getNavItem(self, active, target, text) :
        if active == target :
            return '<li class="active"><a href="/dashboard?view=%s">%s <span class="sr-only">(current)</span></a></li>' % (target, text)
        else :
            return '<li><a href="/dashboard?view=%s">%s</a></li>' % (target, text)

    def getLabelList(self, data) :
        labels = data.getLabels()

        return str(labels)

    def get_filter_list(self, data) :
        flist = []
        print(data)
        for l in data.getLabels() :
            l = l.replace(" ", "_")
            flist.extend(["LBL:" + l, "#"+ l])

        for l in data.getFilters() :
            l = l.replace(" ", "_")
            flist.extend(["FLT:" + l, l])

        return str(flist)
        
    
    def today(self) :
        td = datetime.now()
        return td.strftime("%Y-%m-%d")

    def calendar_max(self):
        td = datetime.now()
        td += timedelta(weeks=52*3)
        return td.strftime("%Y-%m-%d")


    def get_style(self, field) :
        if field == "added" or field == "due_date" :
            return "white-space: nowrap;"
        else :
            return ""

    def get_checked_style(self, task) :
        if task.complete:
            return "taskcomplete"
        

    def as_bool(self, val) :
        if val:
            return "true"
        else :
            return "false"
        
    def format(self, field, value, idx) :
        if field == "added" or field == "due_date":
            today = datetime.today()
            if value is None or value == "" :
                return ""

            if  value.date() == today.date():
                return "Today"
            elif today.year == value.year :
                return value.strftime("%b %d")
            else :
                return value.strftime("%b %y")

        elif field == "labels" :
            s = ""
            for k in value :
                if value[k]>0 :
                    s += '<span class="tasklabel">' + k + '</span>'
            return s
        elif field == "title" :
            return '<a class="node-title" href="#" onclick="edit_node(\'%s\', \'%s\')">%s</a>' % (idx, self.ttype, value)
        elif field == "complete" :
            if value is None or value == "" or not value :
                return "N"
            else :
                return "Y"
        elif field == "description" :
            x = len(str(value))
            if x > 40 :
                x = 40
            return str(value)[:x]+'...'
        else :
            return str(value)
            
