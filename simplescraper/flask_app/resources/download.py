import boto3
import botocore
from flask import Response
from flask_restful import Resource

from ..credentials import AWS_BUCKET_NAME, AWS_ACCESS_KEY_ID, \
    AWS_SECRET_ACCESS_KEY, AWS_REGION_NAME
from ..database import Database


class Download(Resource):
    __slots__ = ("DEFAULT_HEADERS",)

    def __init__(self):
        self.DEFAULT_HEADERS = {'Content-Type': 'text/html'}
        self.database = Database()

    @staticmethod
    def get_client():
        return boto3.client(
            's3',
            AWS_REGION_NAME,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

    def get(self, code_number, filename):
        if self.database.find_one(code_number) is not None:
            s3 = self.get_client()

            FILE_KEY = f'files/{code_number}/{filename}'

            try:
                file = s3.get_object(Bucket=AWS_BUCKET_NAME,
                                     Key=FILE_KEY)
                return Response(
                    file['Body'].read(),
                    mimetype='application/octet-stream',
                    headers={
                        "Content-Disposition":
                            f"attachment;filename={filename}"}
                )
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "NoSuchKey":
                    print("The object does not exist.")
                    return None
                else:
                    raise Exception
            except Exception as e:
                raise e
        else:
            return None
