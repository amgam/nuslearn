import os
import signal
import sys
import time

from flask import Flask, request, Response
from flask import render_template, url_for, redirect, send_from_directory
from flask import send_file, make_response, abort

from angular_flask import app

####### CUSTOM CLASSES & DATA ######
from learner import Learner
from dbase import DBase

class Youtube:
    def __init__(self):

    def validation(self, videolink):
