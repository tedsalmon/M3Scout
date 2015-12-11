#!/usr/bin/python
# -*- coding: utf-8 -*-
from bottle import abort, Bottle, redirect, response, request, static_file, jinja2_template as template
from m3scout.lib.db.m3scout_db import M3ScoutDB
from hashlib import md5
import logging
logging.basicConfig()
M3ScoutWebApp = Bottle()
db = M3ScoutDB()

@M3ScoutWebApp.route('/')
def index():
    new_posts = db.Items.query.filter(db.Items.status==1).all()
    saved_posts = db.Items.query.filter(db.Items.status==2).all()
    return template('main', new_posts=new_posts, saved_posts=saved_posts)

# API v1
@M3ScoutWebApp.route('/api/v1/post')
def api_get_posts():
    return db.Items.query.order_by(db.Items.id)

@M3ScoutWebApp.route('/api/v1/post/<post_id>', method='DELETE')
def api_remove_post(post_id):
    post = db.Items.query.filter(
        db.Items.id==post_id
    ).first()
    post.status = 0
    db.commit()
    return {"success": True}

@M3ScoutWebApp.route('/api/v1/post/<post_id>', method='PUT')
def api_save_post(post_id):
    post = db.Items.query.filter(
        db.Items.id==post_id
    ).first()
    post.status = 2
    db.commit()
    return {"success": True}
