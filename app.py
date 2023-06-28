!/usr/bin/env python3

from flask import Flask, render_template, request, render_template, url_for, abort, jsonify
import os, pytz, json, logging, time, jwt
import clientdocmi
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from models import db
import vault
import config
#HOST="0.0.0.0"
#PORT=8080

app = Flask(__name__)
app.config.from_object('config.config')

def getting_secrets_db():
    DBSECRET = None
    DBSECRET = vault.secretGetVault_db()
    return DBSECRET

DB_URL = 'postgresql+psycopg2://{user}:{pw}@HOST:5432/ef-support-tools'.format(user=getting_secrets_db()['data']['dblogin'],pw=getting_secrets_db()['data']['dbPassword'])

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

from models import Users, Dosc
from auth_middleware import token_required

logging.basicConfig(
    format='%(levelname) -5s %(asctime)s %(funcName)- -20s: %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    level=logging.INFO)

@app.route('/searchDocument/<uuid:MASTERID>')
@token_required
def search_files(CURRENT_USER, MASTERID): 
    EXECUTOR_NAME=CURRENT_USER.__dict__['login']
    OUT=clientdocmi.searceFiles(str(MASTERID))
    app.logger.info('User: ' + EXECUTOR_NAME + ' requested to search client files, masterid: ' + str(MASTERID))
    return jsonify(OUT)

@app.route('/documentDeleted/CLIENTDOC_MI',  methods=('GET', 'POST'))
@token_required
def file_deleted(CURRENT_USER):
#    try:
        if request.method == 'POST':
            BODY = request.json
            if not BODY:
                return {
                    "message": "Please provide user details",
                    "dody": None,
                    "error": "Bad request"
                }, 400
            DOCID=BODY["id"]
            ClientID=BODY["masterid"]
            TAIL=BODY["name"].split('_')[-1]
            NAME=BODY["name"].split(TAIL)[0][:-1]
            CreateDate=BODY["createDate"]
            REASON=BODY["reason"]
            INITIATOR=BODY["initiator"]
            EXECUTOR=CURRENT_USER.__dict__['id']
            EXECUTOR_NAME=CURRENT_USER.__dict__['login']
            if (len(REASON) < 1 or REASON.isspace() or len(INITIATOR) < 1 or INITIATOR.isspace()):
                return {
                    "message": "no required data",
                    "data": None,
                    "error": "Bad Request"
                }, 400
            D1=Dosc(uuidDocs=DOCID, createDate=CreateDate, masterid=ClientID, docType=NAME, initiator=INITIATOR, reason=REASON, executor=EXECUTOR)
            db.session.add(D1)
            OUT=clientdocmi.deleteFile(str(DOCID))
            app.logger.info('User: ' + EXECUTOR_NAME + ' deleted file: ' + str(DOCID))           
            if OUT == 200:                            
                db.session.commit()                
                return ('User: ' + EXECUTOR_NAME + ' deleted file: ' + str(DOCID))
            if OUT == 404:
                db.session.rollback()
                return {
                "message": "Document not found",
                "data": None,
                "error": "not found"
            }, 404
            if OUT == 401:
                db.session.rollback()
                return {
                "message": "No access BCSFS",
                "data": None,
                "error": "Unauthorized"
            }, 401
            else:
                db.session.rollback()
                return {
                    "message": "Something went wrong",
                    "data": None,
                    "error": str(e)
                }, 500
        return OUT

@app.route('/CLIENTDOC_MI/<uuid:DOCID>')
@token_required
def getting_file(CURRENT_USER, DOCID):
    EXECUTOR_NAME=CURRENT_USER.__dict__['login']
    if request.method == 'GET':
        OUT=clientdocmi.getFile(str(DOCID))
        if not OUT:
            abort(404)
        app.logger.info('User: ' + EXECUTOR_NAME + ' download file: ' + str(DOCID))
    return OUT

if __name__ == "__main__":
#    app.run(host=HOST, port=PORT)
    app.run(host=app.config["HOST"], port=int(app.config["PORT"]))

