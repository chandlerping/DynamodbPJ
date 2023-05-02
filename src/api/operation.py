import boto3
import time
from threading import Event
from concurrent.futures import ThreadPoolExecutor


# put_item structure class
class WriteOp:
    key = {}
    update_expr = ""
    expr_attr_val = {}
    return_val = ""


# get_item structure class
class ReadOp:
    key = {}


# simple update_item
def update_item_db(table, write_op):
    # print("writer", time.time())
    response = table.update_item(
        Key=write_op.key,
        UpdateExpression=write_op.update_expr,
        ExpressionAttributeValues=write_op.expr_attr_val,
        ReturnValues=write_op.return_val
    )


# simple execution of get_item
def get_item_db(table, read_op):
    response = table.get_item(
        Key=read_op.key,
        ConsistentRead=False
    )
    return response['Item']


# simple execution of checker_db
def checker_db(table, read_op, delay=0):
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_1 = executor.submit(get_item_db, table, read_op)
        time.sleep(delay)
        future_2 = executor.submit(get_item_db, table, read_op)
    return future_1.result() != future_2.result()
