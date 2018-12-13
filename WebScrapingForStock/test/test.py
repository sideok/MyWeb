'''
Created on 2018. 12. 13.

@author: SIDeok
'''
import re

str = "        sdfg \n              encparam: 'TS9XTVliaE4vcXJpWXROaU5aa2ZFUT09' \r\n\r\n"
# str = str.replace(" ", "")
print(str)
 
p = re.compile("encparam\\s*:\\s*'([^']+)'") # re 내장모듈 내(.) compile 메서드를 사용. 
                         # compile 메서드는 "패턴 객체"를 반환한다. 
  
m = p.search(str)    # 패턴 객체(p)에는 또다시 검색 메서드가 있다. 
print(m.group())