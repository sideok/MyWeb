import urllib.request
from bs4 import BeautifulSoup

#주식정보 페이지 숫자만큼 range를 정해준다.
for i in range(1,400) :
    pageCont = urllib.request.urlopen('https://finance.naver.com/sise/sise_index_day.nhn?code=KPI200&page=' + str(i));
    soup_m = BeautifulSoup(pageCont.read(), "html.parser");
    soup_tab = soup_m.find("table", {"class" : "type_1"});
    
    #tr태그를 읽어온뒤 date가 있는 항목만 처리한다.
    for j in soup_tab.findAll("tr") : 
        if(j.td != None and j.td['class'][0] == 'date') :
            date = j.find("td",{"class" : "date"}).contents[0];
            val = j.find("td",{"class" : "number_1"}).contents[0];
            print(date.replace(".","/") + " ,  " + val);
