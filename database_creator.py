import mysql.connector
from mysql.connector import errorcode


DATABASE_PASSWORD_SOURCE = "./database_password.txt"
DB_NAME = 'dota_match_data'

tables = {}

tables['players'] = (
    "CREATE TABLE players ("
    " player_id BIGINT(20) UNSIGNED,"
    " display_name TINYTEXT,"
    " mmr_est SMALLINT(4) UNSIGNED,"
    " win_rate DECIMAL(4, 2) UNSIGNED,"
    " PRIMARY KEY (player_id)"
    ")"
)

tables['matches'] = (
    "CREATE TABLE matches ("
    " match_id BIGINT(20) UNSIGNED,"
    " winner BOOLEAN,"
    " date TIMESTAMP,"
    " game_type TINYINT(2) UNSIGNED,"
    " PRIMARY KEY (match_id)"
    ")"
)

tables['heroes'] = (
    "CREATE TABLE heroes ("
    " hero_id TINYINT(3) UNSIGNED,"
    " loc_name TINYTEXT,"
    " PRIMARY KEY (hero_id)"
    ")"
)

tables['player_match'] = (
    "CREATE TABLE player_match ("
    " player_id BIGINT(20) UNSIGNED,"
    " match_id BIGINT(20) UNSIGNED,"
    " role TINYINT(2) UNSIGNED,"
    " kills TINYINT(3) UNSIGNED,"
    " deaths TINYINT(3) UNSIGNED,"
    " assists TINYINT(3) UNSIGNED,"
    " leaver_status TINYINT(2) UNSIGNED,"
    " last_hits SMALLINT(4) UNSIGNED,"
    " denies SMALLINT(4) UNSIGNED,"
    " gpm SMALLINT(4) UNSIGNED,"
    " xpm SMALLINT(4) UNSIGNED,"
    " hero_id TINYINT(3) UNSIGNED,"
    " FOREIGN KEY (player_id) REFERENCES players(player_id),"
    " FOREIGN KEY (match_id) REFERENCES matches(match_id),"
    " FOREIGN KEY (hero_id) REFERENCES heroes(hero_id)"
    ")"
)

db_pass = open(DATABASE_PASSWORD_SOURCE).read()

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'aimery',
    password = db_pass,
    auth_plugin = 'mysql_native_password'
)

db_cursor = mydb.cursor()

db_cursor.execute("CREATE DATABASE " + DB_NAME)

mydb.database = DB_NAME

for table_name in tables:
    table_description = tables[table_name]
    try:
        db_cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print(table_name + "already exists.")
        else:
            print(err.msg)
    else:
        print(table_name + " created")

print(mydb)

db_cursor.close()
mydb.close()