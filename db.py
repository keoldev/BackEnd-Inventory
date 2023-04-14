import boto3
import json
import uuid
import os
import base64
import time

db_client = boto3.client('dynamodb')
s3_client = boto3.client('s3')
cf_client = boto3.client('cloudfront')

def get_products():
    response = db_client.scan(
        TableName=os.environ['TABLE_NAME']    
    )
    return response['Items']
    
        
def insert_product(product_name, description, stock, image):
    image_decoded=base64.b64decode(image)
    product_id = str(uuid.uuid4())
    db_client.put_item(
        TableName=os.environ['TABLE_NAME'],
        Item={
            "product_id": {"S": product_id},
            "product_name": {"S": product_name},
            "description": {"S": description},
            "stock": {"N": stock}
        }
    )
    s3_client.put_object(
        Bucket=os.environ['BUCKET_NAME'],
        Key=f"{product_id}.jpg",
        Body=image_decoded
    )
    return product_id

def update_product(product_id, product_name, description, stock, image=None):
    db_client.update_item(
        TableName=os.environ['TABLE_NAME'],
        Key={
            "product_id": {"S": product_id}
        },
        UpdateExpression= "SET #pdct = :product_name, #dsc = :description, #st = :stock",
        ExpressionAttributeNames={
            "#pdct": "product_name",
            "#dsc": "description",
            "#st": "stock"
        },
        ExpressionAttributeValues={
            ":product_name" : {"S": product_name},
            ":description" : {"S": description},
            ":stock" : {"N": stock},
        }
    )
    if image != None:
        image_decoded=base64.b64decode(image)
        s3_client.put_object(
            Bucket=os.environ['BUCKET_NAME'],
            Key=f"{product_id}.jpg",
            Body=image_decoded
        )
        cf_client.create_invalidation(
            DistributionId=os.environ['CLOUDFRONT_ID'],
            InvalidationBatch={
                'Paths': {
                    'Quantity': 1,
                    'Items': [f'{product_id}.jpg']
                },
                'CallerReference': str(time.time()).replace(".", "")
            }
        )
    return product_id
    
def delete_product(product_id):
    db_client.delete_item(
        TableName=os.environ['TABLE_NAME'],
        Key={
            "product_id": {"S": product_id}
        }
    )
    s3_client.delete_object(
        Bucket=os.environ['BUCKET_NAME'],
        Key=f"{product_id}.jpg",
    )
    return product_id