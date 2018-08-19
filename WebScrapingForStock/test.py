import urllib.request

a = urllib.request.urlopen("http://www.daum.net/")
print(a.read())


