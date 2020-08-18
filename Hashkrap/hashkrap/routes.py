from hashkrap import app
import os
from flask import Flask, render_template, request, session
from hashkrap import get_hashtags
import sqlite3
from flask_paginate import Pagination, get_page_args
from hashkrap.db_utils import *
from hashkrap.util import *


@app.route("/", methods=['GET', 'POST'])
def main_page():
    return render_template("layouts/main-page.html", username_flag=1)


def create_cookie(form, session):
    if form['username'] is not None and form['keyword'] is not None:
        username = form['username'].strip("@")
        if not session or form['username'] != session['username']:
            session['username'] = username
            session['profile_engagements'] = get_hashtags.profile_engagements(username)
        try:
            if session['profile_engagements'] is not None:
                pass
            else:
                session['profile_engagements'] = get_hashtags.profile_engagements(username)
        except:
            session['profile_engagements'] = get_hashtags.profile_engagements(username)
        session['keyword'] = form.get("keyword").strip("#")
        try:
            if form.get("options"):
                session["sort_by"] = form.get("options")
            if not session["sort_by"] and not form.get("options"):
                session["sort_by"] = "top"
        except:
            session["sort_by"] = "top"


@app.route('/response', methods=['POST', 'GET'])
def show_hashtag_data():
    if request.method == 'POST':
        create_cookie(request.form, session)
    username = session['username']
    keyword = session['keyword']
    profile_engagements = session['profile_engagements']

    if profile_engagements == "not found":
        return render_template("main-page.html", username_flag=0, keyword=keyword)

    sort_by = session["sort_by"]

    send_telegram_msg(username, keyword, sort_by)

    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    per_page = 100
    hashtag_list = get_hashtags_from_db(keyword, profile_engagements, sort_by)
    total = len(hashtag_list)
    not_found_flag = False
    if total < 20:
        not_found_flag = not_found(keyword, profile_engagements, username)
    pagination_users = get_table_hashtags(hashtag_list, offset, per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('main-page.html',
                           rows=pagination_users,
                           username=username,
                           keyword=keyword,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           order_by=sort_by,
                           not_found_flag=not_found_flag,
                           username_found=1)


@app.route("/contact-us")
def contact_us():
    return render_template("contact-us.html")


@app.route("/<int:filename>")
def show_data_not_found(filename=None):
    filename = str(filename) + ".txt"
    if os.path.exists(filename):
        with open(filename, "r+") as f:
            line = f.read()
            keyword = line.split(",")[0]
            username = line.split(",")[1]
            engagements = line.split(",")[2]
        page, per_page, offset = get_page_args(page_parameter='page',
                                               per_page_parameter='per_page')
        per_page = 100
        sort_by = "top"
        hashtag_list = get_hashtags_from_db(keyword, engagements, sort_by)
        total = len(hashtag_list)
        pagination_users = get_table_hashtags(hashtag_list, offset, per_page)
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
        return render_template('main-page.html',
                               rows=pagination_users,
                               username=username,
                               keyword=keyword,
                               page=page,
                               per_page=per_page,
                               pagination=pagination,
                               order_by=sort_by)
    return render_template("error-404.html")




