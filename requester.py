#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from pymongo import MongoClient
from sodapy import Socrata
#Mongo stores objects in bson format, need this to print
from bson import json_util

def generateJSON(dataSet):
    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("data.colorado.gov", None)
    # First 2000 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get(dataSet, limit=2000)
    # Convert to pandas DataFrame
    # results_df = pd.DataFrame.from_records(results)
    # results_df = pd.DataFrame(results)
    return results

def main():
    #Download JSON
    salesRoomAPI = "ic4i-9zku"
    results = generateJSON(salesRoomAPI)

    with open('salesRoom.json', 'w') as f:
        for row in results:
            f.write("%s\n" % str(row))
        f.close()

    #connect to server
    # Create a connection to the mongodb process
    # on default port of 27017 and localhost
    client = MongoClient()

    #pyMongo will create database if it doesn't exist, else it will connect to this db
    db = client.gocodecoloradodb

    #insert collection data
    # post_id = srCollection.insert_many(results).inserted_id
    result = db.salesRoomsCollection.insert(results)

    #use db, false = keep curser open until program stops
    test = db.salesRoomsCollection.find_one({'location_city': 'Boulder'})

    #For now clear the db out to make sure this process works without cluttering the db
    result = db.salesRoomsCollection.remove({})

    #close connection
    client.close()

if __name__ == '__main__':
  main()