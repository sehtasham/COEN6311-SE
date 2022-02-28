#!/usr/bin/python

from __future__ import print_function

hostname = 'localhost'
username = 'besticke'
password = 'Coen6311!!!'
database = 'besticke_db'

# Simple routine to run a query on a database and print the results:
def doQuery( conn ) :
    cur = conn.cursor()

    cur.execute( "SELECT firstname, lastname FROM user" )

    for firstname, lastname in cur.fetchall() :
        print( firstname, lastname )

print( "Using pymysql:" )
import pymysql
myConnection = pymysql.connect( host=hostname, user=username, passwd=password, db=database )
doQuery( myConnection )
myConnection.close()