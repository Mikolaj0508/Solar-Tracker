import sqlite3
import re


class Data():
    
    def __init__(self):
        conns = sqlite3.connect('test_2.db')
        cursor = conns.cursor()
        self.cursor = cursor
        self.conns = conns
        print("Connected to database")
        
    def close(self):
        self.conns.close()
        print("Closing database")
        
    def req(self, **kwargs):
        output = list(kwargs.values())
        if len(kwargs)==2:
            return output
        else:
            output.insert(1,1)
            return output
        
    def last_three(self):
        self.cursor.execute('SELECT "POWER [mW]" FROM FIRST_DATA ORDER BY "TIMESTAMP" DESC LIMIT 3;')
        result = self.cursor.fetchall()
        max_val = max(result, key=lambda x: x[0])
        return max_val[0], result.index(max_val)
    
    def last_one(self):
        self.cursor.execute('SELECT "POWER [mW]" FROM FIRST_DATA ORDER BY ID DESC LIMIT 1;')
        result = self.cursor.fetchone()
        return result[0]
        
    
    def max_power(self):
        self.cursor.execute('SELECT MAX("POWER [mW]") FROM FIRST_DATA;')
        result = self.cursor.fetchone()
        return result[0]
    
    def resp(self, mess, *args):
        args = args[0]
        args = args.split(",")
        args = ["".join([s for s in re.findall(r'[\d\.\d]+',x)]) for x in args]
        mess.extend(args)
        self.cursor.execute("INSERT INTO FIRST_DATA VALUES (null,?,?,?,?,?,?,datetime('now','localtime'))",mess)
        self.conns.commit()

'''
d = Data()
maxi = d.last_one()
print(type(maxi))
d.close()
'''
