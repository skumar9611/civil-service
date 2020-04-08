import os

import boto3
from botocore.exceptions import ClientError

from config import config
from logger import logger as logging


class AWSClient:
    def __init__(self, **kwargs):
        try:
            self.session = boto3.Session(
                aws_access_key_id=kwargs.get("aws_access_key_id", config['aws_access_key_id']),
                aws_secret_access_key=kwargs.get("aws_secret_access_key", config['aws_secret_access_key'])
            )
            self.bucket_name = config['bucket_name']
            self.bucket_location = config['bucket_location']
            self.s3 = None
            self.s4 = None
            self.create_session()
            self.bucket_creation()
        except ClientError as e:
            logging.error("AWS client Error occurred while initializing aws client. "
                          "Specified records not found={}".format(str(e)))
            raise Exception(e)

    def create_session(self):
        logging.debug("===============================================================================================")
        logging.debug("Creating session.")
        self.s3 = self.session.resource('s3')
        self.s3.Bucket('test') in self.s3.buckets.all()  # validate credentials
        self.s4 = self.session.client('s3')
        logging.info("Session created.")

    def bucket_creation(self):
        """
        :description: This module allows s3 bucket creation
        """
        try:
            logging.debug("Checking if bucket with name {} exists.".format(self.bucket_name))
            if self.s3.Bucket(self.bucket_name) in self.s3.buckets.all():
                logging.info("Bucket already exists.")
                logging.info("Bucket ready for file operations")
            else:
                logging.info("Bucket with name {} does not exist. Creating bucket..".format(self.bucket_name))
                self.s3.create_bucket(Bucket=self.bucket_name,
                                      CreateBucketConfiguration={'LocationConstraint': self.bucket_location})
                logging.info('Bucket with name {} created.'.format(self.bucket_name))
        except Exception as e:
            logging.error("Client Error occurred, bucket name might not be unique.{}".format(str(e)))
            raise Exception(e)

    def file_download(self, destination_folder, file_name, folder_name):
        """
        :description: This module allows for file download from s3 buckets
        :param destination_folder: Path to the folder where the file has to be downloaded
        :param file_name: File to be downloaded
        :param folder_name: Name of the project folder from which the file needs to be downloaded
        """
        file_path = os.path.join(folder_name, file_name)

        destination_folder = os.path.join(destination_folder, file_name)
        if not os.path.exists(destination_folder.rsplit(os.sep, 1)[0]):
            # If zip containing directory doesn't exists create one
            os.makedirs(destination_folder.rsplit(os.sep, 1)[0])
        logging.debug("Destination_folder = {}. File_path={}".format(destination_folder, file_path))
        logging.debug("Fetching and downloading file...")
        try:
            self.s3.Bucket(self.bucket_name).download_file(file_path, destination_folder)
            logging.info("File {} downloaded to {}.".format(file_name, destination_folder))
        except Exception as e:
            logging.error("Client Error occurred, File not found in the specified path. {}".format(str(e)))
            raise Exception(e)

    def file_upload(self, upload_path, file_path):
        """
        :description: This module allows for file upload into specific folders within an s3 bucket
        :param upload_path: The desired key that has to be assigned to the file
        :param file_path: Path to the file that needs to be uploaded
        """
        logging.debug("Checking and uploading file...")
        try:
            logging.debug("Uploading from {} to bucket with destination {}".format(file_path, upload_path))
            self.s4.upload_file(file_path, self.bucket_name, upload_path, ExtraArgs={'ACL': 'public-read'})
            logging.info("File uploaded to {}".format(upload_path))
        except Exception as e:
            logging.error("Client Error occurred, File not found or bucket does not exist.{}".format(str(e)))
            raise Exception(e)

    def get_url(self, key):
        """
        :description: This module generates the file URL for a file uploaded to s3
        :param key: The key that is assigned to the file (file path in bucket)
        :return: file URL
        """

        return "https://{}.s3.amazonaws.com/{}".format(self.bucket_name, key)


aws_client = AWSClient()
