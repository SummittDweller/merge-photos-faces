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

try:
    con = lite.connect(vars.libraryDB)
    with con:
        con.row_factory = lite.Row  # use a dictionary cursor, the data is sent in the form of Python dictionaries. This way we can refer to the data by their column names.
        cur = con.cursor()

        # Fetch and report the SQLite version.
        # cur.execute('SELECT SQLITE_VERSION()')
        # data = cur.fetchone()
        # print "SQLite version: %s" % data

        # Now fetch some image info.
        cur.execute("SELECT * FROM RKMaster") # " WHERE modelId < 101")
        while True:
            row = cur.fetchone()
            if row == None:
                break
            print "%s %s %s" % (row["modelId"], row["fileName"], row["imagePath"])
            # print row[0], row[1]

        # Fetch and report a count of RKMaster records.
        cur.execute("SELECT count(modelId) FROM RKMaster")
        row = cur.fetchone()
        print "There are " + str(row[0]) + " records in RKMaster."

        # rows = cur.fetchall()
        # for row in rows:
        #     print "%s %s %s" % (row["modelId"], row["fileName"], row["imagePath"])

except lite.Error, e:
    print "Error: %s:" % e.args[0]
    sys.exit(1)
    
finally:
    
    if con:
        con.close()


# Connect to the Person.db.
# Tables of interest are:
#   RKPerson with columns modelId, name
#   RKFace with columns modelId, personId, imageId

try:
    con = lite.connect(vars.personDB)
    with con:
        con.row_factory = lite.Row  # use a dictionary cursor, the data is sent in the form of Python dictionaries. This way we can refer to the data by their column names.
        cur = con.cursor()

        # Now fetch some RKPerson info.
        cur.execute("SELECT * FROM RKPerson")  # " WHERE modelId < 101")
        while True:
            row = cur.fetchone()
            if row == None:
                break
            print "%s %s" % (row["modelId"], row["name"])
            # print row[0], row[1]

        # Now fetch some RKFace info.
        cur.execute("SELECT * FROM RKFaces")  # " WHERE modelId < 101")
        while True:
            row = cur.fetchone()
            if row == None:
                break
            print "%s %s %s" % (row["modelId"], row["personId"], row["imageId"])
            # print row[0], row[1]


except lite.Error, e:
    print "Error: %s:" % e.args[0]
    sys.exit(1)

finally:

    if con:
        con.close()

