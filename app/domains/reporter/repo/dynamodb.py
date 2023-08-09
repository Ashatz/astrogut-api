from ..repo import *
from ..entities import *

import boto3

class DynamoDBRepository(ReporterRepository):
    def __init__(self, table_name, region_name: str = 'us-east-1'):
        self.table_name = table_name
        dynamodb = boto3.resource('dynamodb', region_name)
        self.table = dynamodb.Table(table_name)

    def add_reporter(self, reporter: Reporter):
        # Assuming reporter is an instance of a Schematics Model class and has a method to export to dict
        reporter_dict = reporter.to_primitive()

        # Put the item in the DynamoDB table
        response = self.table.put_item(Item=reporter_dict)

        return response