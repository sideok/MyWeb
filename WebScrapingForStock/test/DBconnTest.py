'''
Created on 2018. 12. 13.

@author: SIDeok
'''
from ms_access.connectDB import StockDB

DB = StockDB()
cs = DB.getCursor()

cs.execute("delete from test");
cs.commit()
cs.close();