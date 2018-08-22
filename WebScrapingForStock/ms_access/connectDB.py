'''
Created on 2018. 8. 22.

@author: SIDeok
'''
import pyodbc;

conn = pyodbc.connect(Driver='{Microsoft Access Driver (*.mdb)}'
                      ,DBQ='C:\\Users\\SIDeok\\git\\WebscrapingForStock\\WebscrapingForStock\\ms_access\\StockDB.mdb')
cs = conn.cursor()

cs.execute("INSERT INTO TB_KOSPI200_INDEX VALUES(2,2,3)")

cs.commit()
cs.close()