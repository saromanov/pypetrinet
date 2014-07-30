import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import sqlite3
import numpy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

@app.route("/", methods=("GET", "POST"))
def index():
	dataset = [1,2,3,4,5,6,7,8,9]
	return render_template("index.html", dataset=dataset)


if __name__ == '__main__':
	app.run()