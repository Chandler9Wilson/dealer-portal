import psycopg2
import sys

# TODO add some keyword stuff here
db = 'acmonitor'

def nuclear():
    # Drop all tables from a given database

    try:
        conn = psycopg2.connect("dbname=acmonitor user='catalog' password='catalog' host='localhost' port=5432")
        conn.set_isolation_level(0)
    except:
        print "Unable to connect to the database."

    cur = conn.cursor()

    try:
        cur.execute("SELECT table_schema,table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_schema,table_name")
        rows = cur.fetchall()
        for row in rows:
            print "dropping table: ", row[1]   
            cur.execute("drop table " + row[1] + " cascade") 
        cur.close()
        conn.close()        
    except:
        print "Error: ", sys.exc_info()[1]


def interactive():
    # displaying options to the user
    print(30 * '-')
    print('   WARNING THIS WILL NUKE YOUR DB')
    print(30 * '-')
    print("1. Type 'DELETE ALL MY TABLES' to nuke it")
    print('2. Type anything else for a Hell No')
    print(30 * '-')

    # captures user input
    answer = raw_input('Which option: ')
    
    if answer == 'DELETE ALL MY TABLES':
        print(30 * '-')
        print('   Results')
        print(30 * '-')
        print(nuclear())
    else:
        return "Cyber Peace Achieved"


interactive()