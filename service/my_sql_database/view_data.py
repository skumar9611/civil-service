import base64
import os
import uuid

import pymysql
import wget

from config import config
from logger import logger as logging


def get_data(query_id, query_type):
    csm_database = pymysql.connect(host=config["mysql_host"], user=config["mysql_user"],
                                   database=config["mysql_database"])

    logging.info("Creating cursor for communication with csm database..")
    csm_cursor = csm_database.cursor()
    logging.info("Cursor ready and awaiting commands.....")

    if query_type == "complaint":
        csm_cursor.execute("SELECT * FROM public_complaints WHERE complaint_id = '{}'".format(query_id))

    else:
        csm_cursor.execute("SELECT * FROM public_suggestions WHERE suggestion_id = '{}'".format(query_id))

    detailed_query_data = [list(query_data) for query_data in csm_cursor][0]

    if len(detailed_query_data[11]) > 1:
        document_id = uuid.uuid4()
        wget.download(detailed_query_data[11], "./{}.jpg".format(document_id))

        with open("./{}.jpg".format(document_id), "rb") as uploaded_document:
            document = base64.b64encode(uploaded_document.read())

        os.remove("./{}.jpg".format(document_id))
        return {"detailed_query_data": detailed_query_data, "document": str(document)}

    else:
        return {"detailed_query_data": detailed_query_data}
