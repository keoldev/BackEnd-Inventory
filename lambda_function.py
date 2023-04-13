import traceback
import json
import os
from db import insert_product, get_products, update_product, delete_product

response_body = {
    'statusCode': 200,
    'headers': {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Amz-Date, X-Api-Key, X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'GET, OPTIONS, POST, PUT, DELETE'
    }
}

def handler(event, context):
    if event["httpMethod"] == 'GET':
        try:
            response = get_products()
            response_body['body'] = json.dumps(response)
            return response_body
        except Exception as e:
            response_body['statusCode'] = 400
            response_body['body'] = json.dumps({'message': str(e)})
            return response_body
            
    if event['httpMethod'] == 'POST':
        try:
            product_data=json.loads(event['body'])
            product_name=product_data['product_name']
            description=product_data['description']
            stock=product_data['stock']
            if 'image' in product_data: 
                image=product_data['image']
                response = update_product(product_id, product_name, description, stock, image)
            else: response = update_product(product_id, product_name, description, stock)
            response_body['body'] = json.dumps(response)
            return response_body
        except Exception as e:
            error_info = traceback.format_exc()
            response_body['statusCode'] = 400
            response_body['body'] = json.dumps({'message': error_info})
            return response_body
    
    if event['httpMethod'] == 'PUT':
        try:
            product_data=json.loads(event['body'])
            product_id=product_data['product_id']
            product_name=product_data['product_name']
            description=product_data['description']
            stock=product_data['stock']
            if 'image' in product_data: 
                image=product_data['image']
                response = update_product(product_id, product_name, description, stock, image)
            else: response = update_product(product_id, product_name, description, stock)
            response_body['body'] = json.dumps(response)
            return response_body
        except Exception as e:
            error_info = traceback.format_exc()
            response_body['statusCode'] = 400
            response_body['body'] = json.dumps({'message': error_info})
            return response_body
        
    if event['httpMethod'] == 'DELETE':
        try:
            product_data=json.loads(event['body'])
            product_id=product_data['product_id']
            response = delete_product(product_id)
            response_body['body'] = json.dumps(response)
            return response_body
        except Exception as e:
            error_info = traceback.format_exc()
            response_body['statusCode'] = 400
            response_body['body'] = json.dumps({'message': error_info})
            return response_body