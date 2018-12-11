'''
Created on 2018. 12. 11.

@author: SIDeok
'''
from bs4 import BeautifulSoup
import pyodbc
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException

# db 커넥션 설정
conn = pyodbc.connect(Driver='{Microsoft Access Driver (*.mdb, *.accdb)}'
                      ,DBQ='C:\\Users\\SIDeok\\git\\WebscrapingForStock\\WebScrapingForStock\\ms_access\\StockDB.mdb')
cs = conn.cursor()

# # 크롬드라이버 위치 지정
# driver = webdriver.Chrome('../chromedriver')
# # 페이지 로딩 시간 지정(미설정시 완전히 뜨면 실행)
# driver.implicitly_wait(3)

# 회사 목록 조회
cs.execute("select COMPANY_CODE from Stock_Company_Info") 
rows = cs.fetchall()
for cmp in rows :
    # 크롬드라이버 위치 지정
    driver = webdriver.Chrome('../chromedriver')
    # 페이지 로딩 시간 지정(미설정시 완전히 뜨면 실행)
    driver.implicitly_wait(3)

    # step1 주식종목코드 세팅 및 변수 초기화
    print("start step1-------------------------")
    StockCd = cmp[0]
    dataArr = {} # 입력 데이터 dictionary
    
    # steap1 end--------------------------------------
    
    
    # step2 웹상에 게제된 년도 정보 가져오기
    print("start step2------------------------- " + StockCd)
    
    try:
        # URL에 접근
        driver.get('https://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd=' + StockCd)
        
        #click 이벤트 실행
        driver.find_element_by_id('cns_Tab21').click()
    except Exception as e:
        # 미존재종목 에러시 브라우저 종료
        print(e)
        driver.close()
#         # 크롬드라이버 위치 지정
#         driver = webdriver.Chrome('../chromedriver')
#         driver.implicitly_wait(3)
        continue
    
    # 년도 배열을 가져온다
    soup_m = BeautifulSoup(driver.page_source, "html.parser")
    soup_cont = soup_m.select("#wrapper > #cTB00 + div thead tr + tr > th.bg") # ctb00 태그 다음에 있는 div태그 가져오기
    
    index = 0;
    for th in soup_cont :
        txt = th.contents[0].strip()
        if "E" in txt :
            # 추정치 여부가 Y일경우
            est = "Y"
        else :
            est = "N"
        if txt.__len__() > 0 :
            dataArr[txt.split("/")[0]] = [est]
        index += 1
    
    # step2 end-----------------------------------
    
    
    # step3 데이터 생성
    print("start step3------------------------- " + StockCd)
     
    soup_m = BeautifulSoup(driver.page_source, "html.parser")
    soup_cont = soup_m.select("#wrapper > #cTB00 + div tbody:nth-of-type(2) tr")
    
    # 입력 데이터 생성
    for tr in soup_cont :
        tempBs = BeautifulSoup(tr.__str__(), "html.parser")
        dataBs = tempBs.select("span")
        index = 0;
        for data in dataArr :
            if dataBs.__len__() > index :
                dataArr[data].append(dataBs[index].contents[0].replace('\xa0', '').replace(',', ''))
            else :
                dataArr[data].append('0')
                
            index += 1
            
    # 입력 헤더 생성
    tmpHeader = ["COMPANY_CD", "기준년도", "Estimate_YN"]
    for tr in soup_cont :
        tempBs = BeautifulSoup(tr.__str__(), "html.parser")
        headerBs = tempBs.select("th")
        
        if headerBs.__len__() > 0 :
            tmpHeader.append(headerBs[0].contents[0].replace('\xa0', ''))
    
    dataArr["header"] = tmpHeader
    
    # step4 데이터 입력
    print("start step4------------------------- " + StockCd)
    # 추정치 클리어
    cs.execute("delete from Stock_Summary_Year where COMPANY_CD = ? AND Estimate_YN = ?" , StockCd, "Y") 
    
    # query 헤더 조립
    tmpQUery_head = "insert into Stock_Summary_Year(";
    for data in dataArr["header"] : 
        tmpQUery_head += "[" + data + "],"
    tmpQUery_head = tmpQUery_head[0:-1]
    tmpQUery_head += ")"
    
    # 정보입력
    for data in dataArr : 
        # header 는 continue
        if data == "header" :
            continue
        
        # 기등록건은 continue
        cs.execute("select 기준년도, Estimate_YN from Stock_Summary_Year where COMPANY_CD = ? AND 기준년도  = ?" , StockCd, data) 
        rows = cs.fetchall() 
        if rows.__len__() > 0 :
            continue
    
        tmpQUery_tail = "values('" + StockCd + "', '" + data + "', "
        for val in dataArr[data] :
            tmpQUery_tail += "'" + val +"',"
        tmpQUery_tail = tmpQUery_tail[0:-1]
        tmpQUery_tail += ")"
        
        query = tmpQUery_head + tmpQUery_tail
        print(query)
        cs.execute(query)
    
    # step4 end-----------------------------------
    cs.commit()
    driver.close() # 브라우저 종료 : 간혹가다 브라우져가 굳는 현상이 있어 매번 종료해줌
# 후처리
# cs.commit()
cs.close()

print("finish")



'''
Selenium은 driver객체를 통해 여러가지 메소드를 제공한다.
URL에 접근하는 api,
get(‘http://url.com’)
페이지의 단일 element에 접근하는 api,
find_element_by_name(‘HTML_name’)
find_element_by_id(‘HTML_id’)
find_element_by_xpath(‘/html/body/some/xpath’)
페이지의 여러 elements에 접근하는 api 등이 있다.
find_element_by_css_selector(‘#css > div.selector’)
find_element_by_class_name(‘some_class_name’)
find_element_by_tag_name(‘h1’)
위 메소드들을 활용시 HTML을 브라우저에서 파싱해주기 때문에 굳이 Python와 BeautifulSoup을 사용하지 않아도 된다.
하지만 Selenium에 내장된 함수만 사용가능하기 때문에 좀더 사용이 편리한 soup객체를 이용하려면 driver.page_source API를 이용해 현재 렌더링 된 페이지의 Elements를 모두 가져올 수 있다.
'''