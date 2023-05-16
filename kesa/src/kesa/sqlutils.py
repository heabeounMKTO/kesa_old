import psycopg2
import configparser

class SqlUtils():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("configs/dbcfg.ini")
        self.host = str(config["DBCFG"]["HOST"])
        self.dbname = str(config["DBCFG"]["DB_NAME"])
        self.user = str(config["DBCFG"]["USER"])
        self.password = str(config["DBCFG"]["PASSWORD"])
        self.port = str(config["DBCFG"]["PORT"])
        
    def initDBcheck(self):
        conn , cur = self.connect2DB()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS annotation(
                        id VARCHAR(104857),
                        labels VARCHAR(2048),
                        label_count INT,
                        game_type VARCHAR(256)
                        )
                    """)
        conn.commit()
        cur.close()
        conn.close()

    def connect2DB(self):            
        conn = psycopg2.connect(
                host=self.host, dbname=self.dbname, user=self.user, 
                password=self.password, port=self.port
                )
        cur = conn.cursor()
        # self.conn = conn
        # self.cur = cur
        return conn, cur
    def insertData(self, infoDict):
        conn, cur = self.connect2DB()
        cur.execute("""
                    INSERT INTO annotation(id, labels,label_count, game_type) VALUES (%s , %s, %s, %s);
                    """, 
                    (infoDict["labelid"], infoDict["labels"], 
                     infoDict["label_count"], infoDict["game_type"]))         
        conn.commit()
        cur.close()
        conn.close()

