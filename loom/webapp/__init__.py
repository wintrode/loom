from flask import Flask, render_template, send_from_directory, make_response, request, redirect, Response, g, send_file
import click
import re
from os.path import exists
import base64
import json
import redis
import os
import ssl,urllib
import random
from loom.webapp.view import View
from loom.graphdb import GraphDB
import loom
import sys
from datetime import datetime as dt


app = Flask(__name__)

def get_db() :
    if "db" not in g :
        g.db = GraphDB("localhost", 7474, "neo4j", "neo123")
    return g.db


def parseAddTask(args) :
    title = None
    desc = None
    labels = None
    ttype = "Task"
    due = None

    for x in request.form :
        click.echo("GOT: %s : %s" % (x, request.form.get(x)))


    title = request.form.get("title")
    description=request.form.get("desc")
    labels = request.form.getlist("labels")
    ttype = request.form.get("nodeType")

    newlabel = request.form.get("newlabel")
    if newlabel is not None and len(newlabel.strip()) > 0 :
        labels.append(newlabel)

    
    if ttype is None : ttype = "Task"
    due = request.form.get("due_date")
    if due :
        due = dt.strptime(due, "%Y-%m-%d")
    else :
        due = None
        
    return (ttype, title, description , labels, due)
    
@app.route('/', methods=["GET","POST"])
@app.route('/dashboard', methods=["GET", "POST"])
def index():
    active = request.args.get("view")
    if active is None :
        active = request.form.get("view")
    if active is None or active.strip() == "" :
        active="dashboard"

    filters = request.args.get("filters")
    if filters is None :
        filters = ""

    newfilter = request.args.get("newfilter")
    if newfilter is not None :
        filters += "+" + newfilter

    # break up filters into list
    action = request.form.get("action")

    if active == "goals" :
        ttype = "Goal";
    elif active == "ideas" :
        ttype = "Idea";
    else :
        ttype = "Task";
        
    data=get_db()
    if action is not None and action == "addnode" :
        (ttype, title, description, labels, due) = parseAddTask(request.args)

        click.echo("Adding task: '%s','%s','%s'" % (ttype, title, description))
        data.addTask(title, type=ttype,description=description, labels=labels, due=due)
        
        
    #click.echo("ACTIVE " + active)
    return render_template('index.html', view=View("Task"),
                           data=data, active=active,
                           curreq=request.path,
                           curfilters=filters)

@app.route('/profile', methods=["GET"])
def profile():
    return render_template('profile.html', view=View("Task"), data=get_db())

@app.route('/settings', methods=["GET"])
def settings():
    return render_template('settings.html', view=View("Task"), data=get_db())

@app.route('/help', methods=["GET"])
def help():
    return render_template('help.html', view=View("Task"), data=get_db())


@app.route('/graph', methods=["GET"])
def graphview():
    return render_template('graph.html', view=View("Task"), data=get_db())

    
    
@app.route('/task/<id>', methods=["GET", "POST"])
def node_task(id):
    data=get_db()
    if request.method == "GET" :
        n = data.getNode("Task", id) 
        return Response(json.dumps(n.to_json()), mimetype='application/json')
    elif request.method == "POST" :
        content = request.get_json()
        data.updateNode("Task", id, content)
        print("POST updating", id, content);
        return Response(json.dumps({"status": "ok"}), mimetype='application/json')

@app.route('/goal/<id>', methods=["GET", "POST"])
def node_goal(id):
    data=get_db()
    if request.method == "GET" :
        n = data.getNode("Goal", id) 
        return Response(json.dumps(n.to_json()), mimetype='application/json')
    elif request.method == "POST" :
        content = request.get_json()
        data.updateNode("Task", id, content)
        return Response(json.dumps({"status": "ok"}), mimetype='application/json')
