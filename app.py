import json
import os
import pathlib
import uuid

from flask import Flask, request, jsonify

from aws_client import aws_client
from config import config
from service.MySQL_database.insert_data import insert_data_to_database
from service.MySQL_database.my_sql_client import database_connect
from service.MySQL_database.verify_user import check_user_data
from service.MySQL_database.view_data import get_data

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


@app.route("/csm/public/complaint", methods=["POST"])
def complaint():
    if "complaint_data" not in request.form:
        return "No data entered", 400

    complaint_data = json.loads(request.form["complaint_data"])

    complaint_id = str(uuid.uuid4())

    if "document" not in request.files:
        complaint_data["s3_file_link"] = ""

    else:
        uploaded_file = request.files["document"]

        file_name = uploaded_file.filename
        extension = str(file_name).rsplit(".", 1)[-1]
        file_name = complaint_id + "." + extension

        documents_directory = os.path.join(os.getcwd(), "uploaded_documents")
        pathlib.Path(documents_directory).mkdir(parents=True, exist_ok=True)
        documents_save_path = os.path.join(documents_directory, file_name)

        uploaded_file.save(documents_save_path)

        aws_client.file_upload(upload_path=file_name, file_path=documents_save_path)

        s3_file_link = aws_client.get_url(key=file_name)

        complaint_data["s3_file_link"] = s3_file_link

    complaint_data["complaint_id"] = complaint_id
    complaint_data["submission_type"] = "complaint"

    database_connect()

    complaint_data_submitted = tuple([str(data) for data in complaint_data.values()])
    insert_data_to_database(table_name="public_complaints", consumer_data=complaint_data_submitted)

    return "Complaint registered successfully", 200


@app.route("/csm/public/suggest", methods=["POST"])
def suggestion():
    if "suggestion_data" not in request.form:
        return "No data entered", 400

    suggestion_data = json.loads(request.form["suggestion_data"])

    suggestion_id = str(uuid.uuid4())

    if "document" not in request.files:
        suggestion_data["s3_file_link"] = ""

    else:
        uploaded_file = request.files["document"]

        file_name = uploaded_file.filename
        extension = str(file_name).rsplit(".", 1)[-1]
        file_name = suggestion_id + "." + extension

        documents_directory = os.path.join(os.getcwd(), "uploaded_documents")
        pathlib.Path(documents_directory).mkdir(parents=True, exist_ok=True)
        documents_save_path = os.path.join(documents_directory, file_name)

        uploaded_file.save(documents_save_path)

        aws_client.file_upload(upload_path=file_name, file_path=documents_save_path)

        s3_file_link = aws_client.get_url(key=file_name)

        suggestion_data["s3_file_link"] = s3_file_link

    suggestion_data["suggestion_id"] = suggestion_id
    suggestion_data["submission_type"] = "suggestion"

    database_connect()

    suggestion_data_submitted = tuple([str(data) for data in suggestion_data.values()])
    insert_data_to_database(table_name="public_suggestions", consumer_data=suggestion_data_submitted)

    return "Suggestion submitted successfully", 200


@app.route("/csm/govt_official/login", methods=["GET"])
def assigned_complaints():
    if "user_name" not in request.form:
        return "Please enter the Username", 400

    if "password" not in request.form:
        return "Please enter the Password", 400

    items_to_display = check_user_data(user_name=request.form["user_name"], password=request.form["password"])

    if type(items_to_display) == 'str':
        return items_to_display, 400

    return jsonify(items_to_display), 200


@app.route("/csm/complaint_details", methods=["GET"])
def get_complaint_details():
    if "query_id" not in request.form and "query_type" not in request.form:
        return "Error", 400

    return jsonify(get_data(query_id=request.form["query_id"], query_type=request.form["query_type"])), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config["port"])
