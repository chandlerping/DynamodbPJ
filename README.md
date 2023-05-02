# A Framework to Fuzz DynamoDB
## Introduction
[DynamoDB](https://aws.amazon.com/dynamodb) is a NoSQL database provided by AWS.
There are two types of read operations:
* Strongly consistent reads: require more resource and time but provide the most up-to-date result
* Eventually consistent reads: require less resource but may return stale result, will be consistent eventually

We want to see in which circumstances eventually consistent reads will be inconsistent.

In this project, we develop a configurable framework to reveal such inconsistencies based on 
[Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html), which is the AWS SDK for python.
It generates a seed file and apply mutations to it to raise the inconsistency rate. /
The output file shall contain many inconsistent situations.

## Configuration
In order to run this project, you need to have an AWS account and set authentication credentials.
1. Log in or sign up for AWS, here is the [entrance](https://portal.aws.amazon.com/).
2. Create a IAM user, see [Creating IAM users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console).
3. Create access key for this IAM user, see [Managing access keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey).
4. Install [AWS CLI](https://aws.amazon.com/cli/).
5. Run ```aws configure``` in terminal, and fill in the key id and key (from step 3) to complete configuration.

After these steps, you should be able to use Boto3 and create connections with AWS. 
For more detailed tutorial, please refer to [Configuration](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration).

## Preparation
1. Git clone this project and get into the ```DynamodbPJ``` dir.
2. Install Python3.x.
3. Create a new "user" table.
```shell
python create_table.py
```

## Running
1. Set up the configurations in ```src/config.py```
```python
#################################
# seed file configuration       #
#################################

# original length of the strings to be written in seed
string_len = 10

# seed workflow, composed of a list of item [#writers, #readers, #threads],
# each item refers to a concurrent block in seed file
seed_flow = [
    [1, 1, 2],
    [1, 1, 2]
]


#################################
# fuzzing configuration         #
#################################

# range of replacing string length
string_len_new_l = 10000
string_len_new_h = 20000

# range of mutating thread number
thread_num_new_l = 1
thread_num_new_h = 10

# operations to be performed at a single fuzzing stage
# [#replaces, #threading, #swap, #writer, #checker]
fuzz_ops = [0, 1, 0, 0, 0]

# number of iterations
# A iteration refers to the process of generating a new version of file that has a higher
# inconsistency rate than the previous version
num_itr = 10


#################################
# checking configuration        #
#################################

# number of times to run while calculating the inconsistency rate of a file
# the inconsistency rate will be calculated by taking the average of these executions
check_itr = 50
```
2. run ```main.py```.
```shell
python main.py
```
3. The seed file will be ```./demo/seed.py```, the tmp file used for fuzzing is ```./demo/mutation_tmp.py``` and the output file is ```./demo/mutation_fuzz.py```.

## Output format
The final output file is ```./demo/mutation_fuzz.py```.
The output on stdout has the format as
```text
..................................................initial  0.09
..................................................1  -  0.12
mutated  0.12
..................................................2  -  0.14
mutated  0.14
................
```
* A dot refers to a single execution while calculating the inconsistency rate of a file.
* From the second line, the first number after the dots is the count of mutations that have been performed so far.
* The last number in a row is the inconsistency rate of this file.
* If a file has the highest inconsistency rate so far, "mutated \<inconsistency rate\>" will be printed and this file serves as the input in the following fuzzing processes.

## Design
* ```src/api``` defines the transactions with the database
* ```src/generate``` defines the seed template and the way to generate a seed file.
* ```src/mutate``` defines the mutations which can be performed during the fuzzing process.
* ```src/parse``` is a simple file parser.
* ```src/fuzzer.py``` is the main fuzzer.
This framework is open to extensions. Users can add other mutations or construct the seed file in some new ways.

