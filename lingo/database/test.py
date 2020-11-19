import psycopg2
from configparser import ConfigParser

config_object = ConfigParser()
config_object.read("../../credentials/config.ini")

database_info = config_object["DATABASE"]

print(database_info["DB_HOST"])

con = psycopg2.connect(
    host=database_info["DB_HOST"],
    database=database_info["DB_NAME"],
    user=database_info["DB_USER"],
    password=database_info["DB_PASS"],
    port=database_info["DB_PORT"]
)

cur = con.cursor()

cur.execute("select * from users")

rows = cur.fetchall()

for r in rows:
    print(f"id: {r[0]} name: {r[1]}")

cur.close()
con.close()
