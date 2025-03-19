# Globant Coding Challlenge

This Proof of Concept (PoC) is designed to migrate historical data from CSV files into a PostgreSQL database and provide a REST API to receive new data. The system ensures data integrity, supports batch transactions, and includes backup and restore features using Apache Avro.

## Starting 🚀

These instructions will allow you to get a working copy of the project on your local machine for development and testing purposes.


### Pre-requisites 📋

To a successfull execution of this project you will need to have installed the next stack in your local machine:

#### Python
Check if you have python >= 3.10.
```
python3 --version
```
If not please install depending on your OS following these instructions: https://www.python.org/downloads/

### Installation 🔧
Clone the repository of the project from Github:

```
git clone https://github.com/danielOwl24/coding_challenge.git
```

Move to the local directory where the repo is cloned.

```
cd coding_challenge
```

You should create a Python virtual environment to have all the dependecies of the project installed in an isolated and centralized place within your local machine.

```
source .venv/bin/activate
```

### Execution :runner:
In your local environment move to the directory src/ and execute de main python file:

```
python3 main.py
```

Once the main script is executing you have two options to test the API:

1. Use a tool like Postman to test each route of the API.
2. Open a browser and paste the url of your localhost, you will be able to interact with a basic GUI and test each
feature of the API.
```
http://127.0.0.1:5000
``` 


