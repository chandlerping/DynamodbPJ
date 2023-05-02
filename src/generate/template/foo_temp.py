from src.api.operation import *
from src.utils import generate_random_string
from src.config import *

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')


def main():
    counter = 0

    # initial WriteOp object
    write_op = WriteOp()
    write_op.key = {
        'username': 'janedoe',
        'last_name': 'Doe'
    }
    write_op.update_expr = "set account_type=:r"
    write_op.expr_attr_val = {':r': generate_random_string(string_len)}
    write_op.return_val = "UPDATED_NEW"

    # initial ReadOp object
    read_op = ReadOp()
    read_op.key = {
        'username': 'janedoe',
        'last_name': 'Doe'
    }

    # operations

    return counter
