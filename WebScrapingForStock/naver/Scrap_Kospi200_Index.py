import urllib.request
from bs4 import BeautifulSoup
import pyodbc

#주식정보 페이지 숫자만큼 range를 정해준다.
conn = pyodbc.connect(Driver='{Microsoft Access Driver (*.mdb)}'
                      ,DBQ='C:\\Users\\SIDeok\\git\\WebscrapingForStock\\WebscrapingForStock\\ms_access\\StockDB.mdb')
cs = conn.cursor()

for i in range(1,20) :
    pageCont = urllib.request.urlopen('https://finance.naver.com/sise/sise_index_day.nhn?code=KPI200&page=' + str(i));
    soup_m = BeautifulSoup(pageCont.read(), "html.parser");
    soup_tab = soup_m.find("table", {"class" : "type_1"});
    
    #tr태그를 읽어온뒤 date가 있는 항목만 처리한다.
    print(soup_tab.findAll("tr"))
    for j in soup_tab.findAll("tr") : 
        if(j.td != None and j.td['class'][0] == 'date') :
            date = j.find("td",{"class" : "date"}).contents[0];
            val = j.find("td",{"class" : "number_1"}).contents[0];
            print(str(i) + ", " + date.replace(".","-") + " ,  " + val);
            #print(j)
            cs.execute("INSERT INTO TB_KOSPI200_INDEX VALUES(" + date.replace(".","-") + "," + val + ")")

cs.commit()
cs.close()
