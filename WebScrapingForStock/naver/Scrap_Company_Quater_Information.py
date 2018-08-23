'''
Created on 2018. 8. 23.

@author: SIDeok
'''
#https://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd=005930&fin_typ=0&freq_typ=Y

import urllib.request;
from bs4 import BeautifulSoup;
import pyodbc;

conn = pyodbc.connect(Driver='{Microsoft Access Driver (*.mdb, *.accdb)}'
#                      ,DBQ='C:\\Users\\SIDeok\\git\\WebscrapingForStock\\WebscrapingForStock\\ms_access\\StockDB.mdb')
                      ,DBQ='C:\\Users\\SIDeok\\git\\WebscrapingForStock\\WebScrapingForStock\\ms_access\\StockDB.mdb')
cs = conn.cursor()

list_cmp_cd = cs.execute('SELECT COMPANY_CODE FROM TB_COMPANY_INFO')
arrCmpCd = list_cmp_cd.fetchall()

for i in range(arrCmpCd.__len__() - 1, arrCmpCd.__len__()) :
    pageCont = urllib.request.urlopen('https://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd=' + arrCmpCd[i][0] + '&fin_typ=0&freq_typ=Y');
    soup_m = BeautifulSoup(pageCont.read(), "html.parser");
    soup_tab = soup_m.find("table", {"class" : "gHead01 all-width"});
    #print(soup_tab.findAll("th")[2].contents[0].strip())
    print(soup_tab)


#tr태그를 읽어온뒤 date가 있는 항목만 처리한다.
'''
tdArray = soup_tab.findAll("td");
idx = 0;
for j in tdArray : 
    if(j['class'][0] == 'date' and j.contents[0].replace('\xa0', '') != "") :
        date = j.contents[0];
        val = tdArray[idx+1].contents[0];
        print(str(i) + ", " + date.replace(".","") + " ,  " + val);
        cs.execute("INSERT INTO TB_KOSPI_INDEX VALUES('" + date.replace(".","-") + "'," + val.replace(",","") + ")")
    idx+=1;
'''


print("complete!!!")