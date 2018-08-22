import urllib.request
from bs4 import BeautifulSoup
import pyodbc

#주식정보 페이지 숫자만큼 range를 정해준다.
conn = pyodbc.connect(Driver='{Microsoft Access Driver (*.mdb, *.accdb)}'
#                      ,DBQ='C:\\Users\\SIDeok\\git\\WebscrapingForStock\\WebscrapingForStock\\ms_access\\StockDB.mdb')
                      ,DBQ='C:\\Users\\SIDeok\\git\\WebscrapingForStock\\WebScrapingForStock\\ms_access\\StockDB.mdb')
cs = conn.cursor()

for i in range(1,1250) :
    pageCont = urllib.request.urlopen('https://finance.naver.com/sise/sise_index_day.nhn?code=KOSPI&page=' + str(i));
    soup_m = BeautifulSoup(pageCont.read(), "html.parser");
    soup_tab = soup_m.find("table", {"class" : "type_1"});
    
    #tr태그를 읽어온뒤 date가 있는 항목만 처리한다.
    tdArray = soup_tab.findAll("td");
    idx = 0;
    for j in tdArray : 
        if(j['class'][0] == 'date' and j.contents[0].replace('\xa0', '') != "") :
            date = j.contents[0];
            val = tdArray[idx+1].contents[0];
            print(str(i) + ", " + date.replace(".","") + " ,  " + val);
            cs.execute("INSERT INTO TB_KOSPI_INDEX VALUES('" + date.replace(".","-") + "'," + val.replace(",","") + ")")
        idx+=1;
        

cs.commit()
cs.close()

print("complete!!!")