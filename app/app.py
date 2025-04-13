import os
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify


app = Flask(__name__)


@app.route("/")
def index():
  return render_template("index.html")