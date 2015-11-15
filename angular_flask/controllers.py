import os
import signal
import sys
import time
import json

from flask import Flask, request, Response
from flask import render_template, url_for, redirect, send_from_directory
from flask import send_file, make_response, abort

from angular_flask import app

####### CUSTOM CLASSES & DATA ######
from learner import Learner
from dbase import DBase
from youtube import Youtube
from suggest import Suggest
from search import Search
from voter import Voter

current_user = None
dbase = DBase()
yt = Youtube()
suggest = Suggest()
searcher = Search()
voter = Voter()

# print dbase.retrieve("select * from modules")

print dbase.retrieve("select * from ModuleTable where module_code=\"UTW1001N\"",False,True)["module_name"]
# print dbase.retrieve("select * from GlobalVideoTable where module_code=\"CS1010\"")
print
print dbase.retrieve("select * from GlobalTagTable where tags=\"socket\"")
# print yt.retrieveVideoInfo("https://www.youtube.com/watch?v=bX3jvD7XFPs")
# print yt.retrieveVideoInfo("https://www.youtube.com/watch?v=eBas9H7VmXA")
# print yt.retrieveVideoInfo("youtube")

# print yt.extractCategory()
# print dbase.retrieve("select * from modules where module_code=\"GEM1902B\"")
# print dbase.retrieve("select * from modules where module_code=\"UTC1102B\"")


# """ use sql styled select statements"""
# dbase.insert(
#         """insert into user (name, links)
#            values ("trish", "yt.com")
#         """)
# #
# print dbase.retrieve(
#         """
#                 select * from user
#                 """)

### SAVE DB BEFORE EXITING #######
def signal_handler(signal, frame):
    dbase.save()
    print 'quit.'
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

########## NOT IN USE ############
# routing for API endpoints, generated from the models designated as API_MODELS
# from angular_flask.core import api_manager
# from angular_flask.models import *

#
# for model_name in app.config['API_MODELS']:
#     model_class = app.config['API_MODELS'][model_name]
#     api_manager.create_api(model_class, methods=['GET', 'POST'])
# session = api_manager.session

####### ROUTING ###########
# routing for basic pages (pass routing onto the Angular app)
@app.route('/')
def index():
    return make_response(open('angular_flask/templates/index.html').read())

@app.route('/loginProxy')
def loggedProxy():
    print "loggedInproxy"
    token = request.args.get('token') #extract token

    global current_user
    current_user = Learner(token)
    return make_response(open('angular_flask/templates/index.html').read())

@app.route('/loggedIn')
def loggedIn():
    print "loggedIn"
    # token = request.args.get('token')
    # print token
    return make_response(open('angular_flask/templates/index.html').read())

@app.route('/getusername', methods=['GET'])
def get_username():
    return current_user.get_username()

@app.route('/getmodulevideos', methods=['GET'])
def get_modvideos():
    print "getting videos.."
    return current_user.get_videoinfo()

@app.route('/suggest', methods=['POST'])
def suggest_video():
    print "suggest - Controllers.py"
    print request.data
    req = json.loads(request.data)
    link = req["link"]
    code = req["code"].upper()
    tags = req["tags"]
    global suggest
    return suggest.validateSuggestion(link, code, tags)

@app.route('/search', methods=['POST'])
def search():
    req = json.loads(request.data)
    searchTerm = req["term"]
    global searcher
    return searcher.look(searchTerm)

@app.route('/upvote', methods=['POST'])
def upvote():
    req = json.loads(request.data)
    print req
    vote = req["upvote"]
    isSearch = req["searchT"]
    global voter

    if voter.upvote(vote):
        if isSearch:
            return searcher.look(isSearch)
        else:
            return current_user.get_videoinfo()


@app.route('/downvote', methods=['POST'])
def downvote():
    req = json.loads(request.data)
    print req
    vote = req["downvote"]
    isSearch = req["searchT"]
    global voter

    if voter.downvote(vote):
        if isSearch:
            return searcher.look(isSearch)
        else:
            return current_user.get_videoinfo()


# special file handlers and error handlers
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.ico')
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
