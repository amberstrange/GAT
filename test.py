import psycopg2

try:
    conn = psycopg2.connect("dbname='testdb' user='postgres' host='localhost' password='postgres'")
except:
    print("I am unable to connect to the database")

