import mysql.connector as connection 

mydb =connection.connect(host='localhost',user="root",passwd='Vishnu@1234567890')
print(mydb)


class database_connection():
    
    def __init__(self):
        self.host='localhost'
        self.user="root"
        self.passwd='Vishnu@1234567890'
        
    def connection(self):
        mydb = connection.connect(host=self.host,user = self.user,passwd = self.passwd)
        print(mydb)
        self.cursor = mydb.cursor()
        print(cursor)
        
    def code_execution(self,table_name,dbname):
        self.table_name = table_name
        self.dbname = dbname
        self.cursor(f"create database if not exists {self.dbname}")
        self.cursor(f"use {self.dbname}")
        self.cursor(f"create table if not exists {self.dbname}.{self.table_name} (cycle float,op1 float,op2 float,sensor2 float,sensor3 float,sensor4 float,sensor5 float,sensor6 float,sensor7 float,sensor8 float,sensor9 float,sensor10 float,sensor11 float,sensor12 float,sensor13 float,sensor14 float,sensor15 float,sensor16 float,sensor17 float,sensor20 float,sensor21 float)") 
    
    def insert_sql(self):
        query = self.cursor(f"insert into {self.dbname}.{self.table_name} values ({self.cycle},{self.op1},{self.op2},{self.sensor2},{self.sensor3},{self.sensor4},{self.sensor5},{self.sensor6},{self.sensor7},{self.sensor8},{self.sensor9},{self.sensor10},{self.sensor11},{self.sensor12},{self.sensor13},{self.sensor14},{self.sensor15},{self.sensor16},{self.sensor17},{self.sensor20},{self.sensor21})")
        return query
    
obj = database_connection()
obj.connection()
obj.code_execution("PM_AERO","AERO_PM")
obj.insert_sql()