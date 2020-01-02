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

app = Flask(__name__)

def get_db() :
    if "db" not in g :
        g.db = GraphDB("localhost", 7474, "neo4j", "neo123")
    return g.db


def parseAddTask(args) :
    title = None
    desc = None
    labels = None

    title = request.form.get("title")
    description=request.form.get("desc")
    labels = request.form.getlist("labels")
    #click.echo(title + " " + description)
    #click.echo(labels)
    return (title, description , labels)
    
@app.route('/', methods=["GET","POST"])
@app.route('/dashboard', methods=["GET", "POST"])
def index():
    active = request.args.get("view")
    if active is None :
        active = request.form.get("view")
    if active is None or active.strip() == "" :
        active="dashboard"

    action = request.form.get("action")
    #click.echo("ACTION " + str(action))
    #click.echo("TITLE " + str(request.form.get("title")))
    data=get_db()    
    if action is not None and action == "addtask" :
        (title, description, labels) = parseAddTask(request.args)
        data.addTask(title, description=description, labels=labels)
        
        
    #click.echo("ACTIVE " + active)
    return render_template('index.html', view=View(),
                           data=data, active=active,
                           curreq=request.path)

@app.route('/profile', methods=["GET"])
def profile():
    return render_template('profile.html', view=View(), data=get_db())

@app.route('/settings', methods=["GET"])
def settings():
    return render_template('settings.html', view=View(), data=get_db())

@app.route('/help', methods=["GET"])
def help():
    return render_template('help.html', view=View(), data=get_db())


@app.route('/graph', methods=["GET"])
def graphview():
    return render_template('graph.html', view=View(), data=get_db())

    
    
