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
import os

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
counter = 0

try:
  con = lite.connect(vars.libraryDB)
  with con:
    con.row_factory = lite.Row  # Use a dictionary cursor, the data is sent in the form of Python dictionaries.
    cur = con.cursor()  # This way we can refer to the data by their column names.
    
    # OK, my first REAL query...
    # One at a time, return the path to an image that has an assigned person (name).
    
    print "\n\nPhotos tagged with any name...\n"
    q = "SELECT p.name AS name, m.imagePath AS path FROM RKMaster m JOIN RKFace f ON (f.imageModelId = m.modelId) " \
        "JOIN RKPerson p ON (p.modelId = f.personId) WHERE ((p.name IS NOT NULL) AND (p.name != ''))"
    
    # q = "SELECT p.name AS name, m.imagePath AS path FROM RKMaster m JOIN RKFace f ON (f.imageModelId = m.modelId) " \
    #    "JOIN RKPerson p ON (p.modelId = f.personId) WHERE (p.name LIKE 'Ian M%')"
    
    for name, path in cur.execute(q):
      counter += 1
      # print row[0], row[1]
      image = "/Volumes/files/" + path
      person = name
      
      print " %d. %s %s" % (counter, person, image)
      
      # Check that the file still exists!
      if os.path.isfile(image):
        metadata = pyexiv2.ImageMetadata(image)
        try:
          metadata.read()
        except:
          print "There was a problem reading metadata from file " + image + "!"
          input("Press ENTER to bypass this file and continue...")
          continue
        
        newkeywords = [person]
        keyword_tag = 'Iptc.Application2.Keywords'
        
        # Check if tag is already exists in the file
        if keyword_tag in metadata.iptc_keys:
          tag = metadata[keyword_tag]
          oldkeywords = tag.value
          print "        Existing tags:", oldkeywords
          if not newkeywords:
            sys.exit(0)
          for newkey in newkeywords:
            if newkey not in oldkeywords:
              oldkeywords.append(newkey)
          tag.value = oldkeywords
          
        # No keys in the file yet...add them
        else:
          print "        No IPTC tags set yet"
          if not newkeywords:
            sys.exit(0)
          metadata[keyword_tag] = pyexiv2.IptcTag(keyword_tag, newkeywords)
        
        # Print the new tags and write them into the file
        tag = metadata[keyword_tag]
        print "        New tags:", tag.value
        
        metadata.write()
      
      # The file referenced in the database was not found!  Report and move on.
      #else:
      #  print "File " + image + " could not be found!"
      #  input("Please make a note of this and press ENTER to bypass this file and continue...")

# An SQLite error was encountered.
except lite.Error, e:
  print "Error: %s" % e.args[0]
  sys.exit(1)

# All done with the database.  Close it up.
finally:
  if con:
    con.close()
    sys.exit(1)


