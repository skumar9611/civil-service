import pymysql

from config import config
from logger import logger as logging


def check_user_data(user_name, password):
    complaints_assigned = []
    suggestion_assigned = []
    designation = None

    csm_database = pymysql.connect(host=config["mysql_host"], user=config["mysql_user"],
                                   database=config["mysql_database"])

    logging.info("Creating cursor for communication with csm database..")
    csm_cursor = csm_database.cursor()
    logging.info("Cursor ready and awaiting commands.....")

    csm_cursor.execute("SELECT * FROM officials_data")

    government_personnel_data = [list(user_data) for user_data in csm_cursor]

    for personnel in government_personnel_data:
        if personnel[0] == user_name and personnel[1] == password:
            designation = personnel[2]
            break

    if designation is None:
        return "Incorrect user credentials"

    try:
        csm_cursor.execute("SELECT * FROM public_complaints WHERE complaint_to = '{}'".format(designation))
        complaints_assigned = [list(complaint) for complaint in csm_cursor]

        csm_cursor.execute("SELECT * FROM public_suggestions WHERE suggestion_to = '{}'".format(designation))
        suggestion_assigned = [list(suggestion) for suggestion in csm_cursor]

    except Exception as exception:
        logging.error(exception)
        pass

    display_data = complaints_assigned + suggestion_assigned

    return display_data
