#!/usr/bin/python
# -*- coding: utf-8 -*-

# Lots of code lifted from http://zetcode.com/db/sqlitepythontutorial/

import sqlite3 as lite
import sys
import vars

con = None

# Connect to the Library.apdb.
# Tables of interest are:
#   RKMaster with columns modelId, fileName and imagePath
#   RKFace with columns modelId, personId, imageId

print "Target is: " + vars.libraryDB

try:
    con = lite.connect(vars.libraryDB)
    with con:
        con.row_factory = lite.Row  # use a dictionary cursor, the data is sent in the form of Python dictionaries. This way we can refer to the data by their column names.
        cur = con.cursor()

        # Fetch and report the SQLite version.
        # cur.execute('SELECT SQLITE_VERSION()')
        # data = cur.fetchone()
        # print "SQLite version: %s" % data

        print "modelId, fingerprint, imagePath\n"

        # Now fetch some image info.
        # Create an "images" dictionary of uuid:imagePath pairs.

        images = {}

        cur.execute("SELECT * FROM RKMaster WHERE modelId < 101")
        while True:
            row = cur.fetchone()
            if row == None:
                break
            print "%s %s %s" % (row["modelId"], row["fingerprint"], row["imagePath"])
            images[row["uuid"]] = row["imagePath"]
            # print row[0], row[1]

        # Fetch and report a count of RKMaster records.
        cur.execute("SELECT count(modelId) FROM RKMaster")
        row = cur.fetchone()
        print "\nThere are " + str(row[0]) + " records in RKMaster.\n"

        # rows = cur.fetchall()
        # for row in rows:
        #     print "%s %s %s" % (row["modelId"], row["fileName"], row["imagePath"])

except lite.Error, e:
    print "Error: %s" % e.args[0]
    sys.exit(1)
    
finally:
    
    if con:
        con.close()
        sys.exit(1)


# Connect to the Person.db.
# Tables of interest are:
#   RKPerson with columns modelId, name
#   RKFace with columns modelId, personId, imageId

print "\n\nTarget is: " + vars.personDB

try:
    con = lite.connect(vars.personDB)
    with con:
        con.row_factory = lite.Row  # use a dictionary cursor, the data is sent in the form of Python dictionaries. This way we can refer to the data by their column names.
        cur = con.cursor()

        print "\n\nmodelId, uuid, name\n"

        # Now fetch some RKPerson info.
        # Create a "people" dictionary of modelId:name pairs.

        people = {}

        cur.execute("SELECT * FROM RKPerson")  # " WHERE modelId < 101")
        while True:
            row = cur.fetchone()
            if row == None:
                break
            print "%s %s %s" % (row["modelId"], row["uuid"], row["name"])
            people[row["modelId"]] = row["name"]
            # print row[0], row[1]

        print "\n\nmodelId, personId, imageId\n"

        # Now fetch some RKFace info.

        cur.execute("SELECT * FROM RKFace WHERE modelId < 101")
        while True:
            row = cur.fetchone()
            if row == None:
                break
            pid = row["personId"]
            # print "%s %s %s" % (row["modelId"], pid, row["imageId"])
            # print row[0], row[1]

            # If personId > 0 attempt to look up the person in people and report any that are found.
            if pid > 0:
                pName = people[pid]
                image = row["uuid"]
                path = images[image]
                print pName + " is identified in the image at " + path


except lite.Error, e:
    print "Error: %s:" % e.args[0]
    sys.exit(1)

finally:

    if con:
        con.close()

