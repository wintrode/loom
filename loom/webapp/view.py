class View :
    def __init__(self) :
        self.headers=[('Title','title'), ('Added', 'added'),
                      ('Due','dueDate'), ('Description', 'description'),
                      ('Labels', 'labels')]

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
    
