from django.shortcuts import render
from django.http import JsonResponse
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv
import requests
from requests.exceptions import RequestException, JSONDecodeError
import json

dotenv_path = 'env_var.env'
load_dotenv(dotenv_path)
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

def sql_res(query):
    """
    Args:
        query (str): Query in SQL

    Returns:
        sqlalchemy.engine.Connection: Returns table from database based on query.  
    """

    try:
        engine = create_engine(f'mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')
    except SQLAlchemyError as e:
        print(f'SQL ALCHEMY ERROR: {e}')
    with engine.connect() as connection:
            return connection.execute(text(query))


def order_details(request):
    """Create json from whole orders table from database. Main key in json is row_id.

    Args:
        request: Obligatory from Django

    Returns:
        json: Orders table in json format.
    """

    query = f'SELECT * FROM orders'
    res = sql_res(query)
    # row_id, order_id, customer_id, product_id, quantity, order_date, status
    orders = {row[0]: {'order_id': row[1], 'customer_id': row[2], 'product_id': row[3], 'quantity': row[4], 'order_date': row[5], 'status': row[6] } for row in res}
    return JsonResponse(orders)


def money_details(request, c_id):
    """Create json with two fields - overall money spent and items bought.

    Args:
        request: Obligatory from Django
        c_id: Customer id for customer we need info. about.

    Returns:
        json: Money spent and items bought in json format.
    """

    query = f'SELECT SUM(quantity) as items_bought, ROUND(SUM(quantity * price), 2) as money_spent FROM orders JOIN products USING (product_id) WHERE customer_id = {c_id};'
    res = sql_res(query)
    overall = dict()
    for row in res:
        overall = {'items': row[0], 'money': row[1]}
    return JsonResponse(overall)


def customers_details(request):
    """Create json storing name and adress of all customers from customers table. Main key in json is a customer_id.

    Args:
        request: Obligatory from Django

    Returns:
        json: Name and adress of all customers in json format.
    """

    query = f'SELECT * FROM customers'
    res = sql_res(query)
    customers = {row[0]: {'name': row[1], 'address': row[-1]} for row in res}
    return JsonResponse(customers)


def get_specific_customer(request, c_id):
    """Find information about orders of specific customer

    Args:
        request: Obligatory from Django
        c_id (int): ID of customer you want info about.

    Returns:
        json: Orders table for specifi customer in json format.
    """
    
    try:
        engine = create_engine(f'mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')
    except SQLAlchemyError as e:
        print(f'SQL ALCHEMY ERROR: {e}')
    query = f'SELECT * FROM orders WHERE customer_id = {c_id} ORDER BY order_date'
    with engine.connect() as connection:
        res = connection.execute(text(query))
    orders = {row[0]: {'order_id': row[1], 'customer_id': row[2], 'product_id': row[3], 'quantity': row[4], 'order_date': row[5], 'status': row[6] } for row in res}
    return JsonResponse(orders)

def project_general(request):
    try:
        customers_response = requests.get('http://127.0.0.1:8000/dashboard/data/customers', [])
        customers = customers_response.json()
    except RequestException as e:
        print(f"Request error: {e}")
    except JSONDecodeError:
        print("Failed to decode JSON from response.")
    return render(request, 'dashboard.html', {'customers': customers})