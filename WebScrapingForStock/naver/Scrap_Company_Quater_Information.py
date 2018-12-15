'''
Created on 2018. 12. 11.

@author: SIDeok
'''
import re
import urllib.request;

from bs4 import BeautifulSoup;

from ms_access.connectDB import StockDB


# db 커넥션 설정
DB = StockDB()
cs = DB.getCursor()

# 회사 목록 조회
cs.execute("select COMPANY_CODE from Stock_Company_Info") 
rows = cs.fetchall()
for cmp in rows :

    # step1 주식종목코드 세팅 및 변수 초기화
    print("start step1-------------------------")
    StockCd = cmp[0]
    dataArr = {} # 입력 데이터 dictionary
    #헤더정보 세팅
    hdr = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
           , "Referer" : "https://companyinfo.stock.naver.com/v1/company/c1030001.aspx?cmp_cd=" + StockCd       
            }
    # steap1 end--------------------------------------
    
    # step2 id값 및 encParam 수집
    try:
        req = urllib.request.Request('https://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd=' + StockCd, headers=hdr);
        soup_m = BeautifulSoup(urllib.request.urlopen(req).read(), "html.parser")
        soup_cont = soup_m.select("#wrapper > #cTB00 + div") # ctb00 태그 다음에 있는 div태그 가져오기
        id = soup_cont[0].get('id') # id
        p = re.compile("encparam\\s*:\\s*'([^']+)'") # encparam: 으로 시작하고 '가 중간에 2개 있는 문자열 탐색
        m = p.search(soup_m.find(type="text/javascript", src = "").contents[0]) # 불필요문자 제거
        encParam = re.sub("\s|encparam:\s|'","",m.group()) # encparam
    except Exception as e:
        # 미존재종목 에러시 브라우저 종료
        print(e)
        continue
    # steap2 end--------------------------------------



    # step2 웹상에 게제된 년도 정보 가져오기
    print("start step2------------------------- " + StockCd)
    
    try:
        req = urllib.request.Request('https://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd=' + StockCd + '&fin_typ=0&freq_typ=Q&encparam=' + encParam + '&id=' + id, headers=hdr);
        soup_m = BeautifulSoup(urllib.request.urlopen(req).read(), "html.parser")
        soup_cont = soup_m.select("thead tr + tr > th.bg")
        index = 0;
        for th in soup_cont :
            txt = th.contents[0].strip()
            if "E" in txt :
                # 추정치 여부가 Y일경우
                est = "Y"
            else :
                est = "N"
            if txt.__len__() > 0 :
                dataArr[txt.split("(")[0]] = [est]
            index += 1
    except Exception as e:
        # 미존재종목 에러시 브라우저 종료
        print(e)
        continue
    # step2 end-----------------------------------
    
    # step3 데이터 생성
    print("start step3------------------------- " + StockCd)
    req = urllib.request.Request('https://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd=' + StockCd + '&fin_typ=0&freq_typ=Y&encparam=' + encParam + '&id=' + id, headers=hdr);
    soup_m = BeautifulSoup(urllib.request.urlopen(req).read(), "html.parser")
    soup_cont = soup_m.select("tbody:nth-of-type(2) tr")
     
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
    tmpHeader = ["COMPANY_CD", "기준년월", "Estimate_YN"]
    for tr in soup_cont :
        tempBs = BeautifulSoup(tr.__str__(), "html.parser")
        headerBs = tempBs.select("th")
         
        if headerBs.__len__() > 0 :
            tmpHeader.append(headerBs[0].contents[0].replace('\xa0', ''))
     
    dataArr["header"] = tmpHeader
    # step3 end------------------------------------------------
    
    # step4 데이터 입력
    print("start step4------------------------- " + StockCd)
    # 추정치 클리어
    cs.execute("delete from Stock_Summary_Quater where COMPANY_CD = ? AND Estimate_YN = ?" , StockCd, "Y") 
     
    # query 헤더 조립
    tmpQUery_head = "insert into Stock_Summary_Quater(";
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
        cs.execute("select 기준년월, Estimate_YN from Stock_Summary_Quater where COMPANY_CD = ? AND 기준년월  = ?" , StockCd, data) 
        rows = cs.fetchall() 
        if rows.__len__() > 0 :
            continue
     
        tmpQUery_tail = "values('" + StockCd + "', '" + data + "', "
        for val in dataArr[data] :
            tmpQUery_tail += "'" + val +"',"
        tmpQUery_tail = tmpQUery_tail[0:-1]
        tmpQUery_tail += ")"
         
        query = tmpQUery_head + tmpQUery_tail
        cs.execute(query)
     
    # step4 end-----------------------------------
    print(dataArr)    
    cs.commit()
# 후처리
cs.close()

print("finish")


