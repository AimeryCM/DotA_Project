import mysql.connector
from mysql.connector import errorcode


class DatabaseManager():

    # The object to handle the creation of the database and adding,
    # accessing, and removing data from it

    def __init__(self, password, user = 'root', host = 'localhost', auth_plugin = 'mysql_native_password'):
        self.user = user
        self.password = password
        self.host = host
        self.auth_plugin = auth_plugin
        self.sql_connection = None
        self.cursor = None

    def connect(self):
        self.sql_connection = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            auth_plugin = self.auth_plugin
        )
        self.cursor = self.sql_connection.cursor()
    
    def open_database(self, database_name, create_new = False):
        if self.sql_connection is None:
            self.connect
        
        if create_new:
            self.cursor.execute("CREATE DATABASE " + database_name)
        
        self.sql_connection.database = database_name
    
    def disconnect(self):
        self.cursor.close()
        self.cursor = None
        self.sql_connection.close()
        self.sql_connection = None
    
    def create_table(self, table_name, table_description):
        if self.cursor is None or self.sql_connection is None:
            return False
        try:
            self.cursor.execute("CREATE TABLE " + table_name + table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print(table_name + "already exists.")
            else:
                print(err.msg)
        else:
            print(table_name + " created")
        return True

    def execute_sql_statement(self, sql_statement):
        if self.cursor is not None and self.sql_connection is not None:
            return self.cursor.execute(sql_statement)



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