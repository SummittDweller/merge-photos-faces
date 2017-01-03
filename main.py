#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Portions lifted from...

  http://zetcode.com/db/sqlitepythontutorial/
  https://www.tutorialspoint.com/sqlite/sqlite_using_joins.htm

"""

import sqlite3 as lite
import sys
import vars
import json
import sys
import pyexiv2

con = None

"""
Connect to the Photos 2.0 library.
  'modelId' is the primary key for all tables.
  Tables of interest are:
    RKMaster with columns 'imagePath', 'fileSize', 'width', 'height'
    RKFace with columns 'imageModelId', 'personId', 'qualityMeasure', 'size'
    RKPerson with column 'name'

  Example query...
    SELECT a.*
    FROM Movie m
    LEFT JOIN Cast c on (c.movieID = m.movieID)
    LEFT JOIN Actor a on (a.actorID = c.actorID)
    WHERE m.movieName='Apocalypse Now';

  My first query...
    SELECT m.imagePath
    FROM RKMaster m
    JOIN RKFace f ON (f.imageModelId = m.modelId)
    JOIN RKPerson p ON (p.modelId = f.personId)
    WHERE p.name = "Mark"

"""

print "Target is: " + vars.libraryDB

try:
    con = lite.connect(vars.libraryDB)
    with con:
        con.row_factory = lite.Row  # use a dictionary cursor, the data is sent in the form of Python dictionaries. This way we can refer to the data by their column names.
        cur = con.cursor()

        """
        # Fetch and report the SQLite version.
        # cur.execute('SELECT SQLITE_VERSION()')
        # data = cur.fetchone()
        # print "SQLite version: %s" % data

        # Now fetch some image info.
        # Create an "images" dictionary of uuid:imagePath pairs.

        images = {}
        print "modelId, fingerprint, imagePath\n"

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
        """

        # OK, my first REAL query...
        # One at a time, return the path to an image that has an assigned person (name).

        print "\n\nPhotos tagged with any name...\n"

        q = "SELECT p.name AS name, m.imagePath AS path FROM RKMaster m JOIN RKFace f ON (f.imageModelId = m.modelId) " \
            "JOIN RKPerson p ON (p.modelId = f.personId) WHERE ((p.name IS NOT NULL) AND (p.name != ''))"

        q = "SELECT p.name AS name, m.imagePath AS path FROM RKMaster m JOIN RKFace f ON (f.imageModelId = m.modelId) " \
            "JOIN RKPerson p ON (p.modelId = f.personId) WHERE (p.name = 'Anel')"

        cur.execute(q)
        while True:
            row = cur.fetchone()
            if row == None:
                break
            print "  %s %s" % (row["name"], row["path"])
            # print row[0], row[1]
            image = "/Volumes/files/" + row["path"]
            person = row["name"]

            metadata = pyexiv2.ImageMetadata(image)
            metadata.read()

            newkeywords = person

            keyword_tag = 'Iptc.Application2.Keywords'
            if keyword_tag in metadata.iptc_keys:
                tag = metadata[keyword_tag]
                oldkeywords = tag.value
                print "        Existing keywords:", oldkeywords
                if not newkeywords:
                    sys.exit(0)
                for newkey in newkeywords:
                    oldkeywords.append(newkey)
                tag.value = oldkeywords
            else:
                print "        No IPTC keywords set yet"
                if not newkeywords:
                    sys.exit(0)
                metadata[keyword_tag] = pyexiv2.IptcTag(keyword_tag, newkeywords)

            tag = metadata[keyword_tag]
            print "        New keywords:", tag.value

            metadata.write()

            """
            # Got one.  Now open the corresponding image and check if the metadata already contains this name or not.
            from libxmp.utils import file_to_dict

            try:
                metadata = file_to_dict(image)
                #print json.dumps(metadata, indent=2)
                iptc = metadata[consts.XMP_NS_IPTCCore]
                print json.dumps(iptc, indent=2)

            except:
                print "   This image has NO readable IPTC metadata."

                # Lets open the file read/write and see if we can make something happen.
                from libxmp import XMPFiles, consts
                try:
                    xmpfile = XMPFiles(file_path=image, open_forupdate=True)
                except:
                    print " >>>>> The inage could not be opened for read/write of XMP metadata."
                    sys.exit(1)

                xmp = xmpfile.get_xmp()
                xmp.append_array_item(consts.XMP_NS_DC, 'subject', person,
                    {'prop_array_is_ordered': True, 'prop_value_is_array': True})

                #xmp.set_property(consts.XMP_NS_DC, u'format', u'image/jpeg')
                if xmpfile.can_put_xmp(xmp):
                    xmpfile.put_xmp(xmp)
                    try:
                        xmpfile.close_file()
                    except:
                        print "       Can't close the file after XMP.append_array_item!"
            """
        """
        # rows = cur.fetchall()
        # for row in rows:
        #     print "%s %s %s" % (row["modelId"], row["fileName"], row["imagePath"])
        """

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
"""
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
"""
