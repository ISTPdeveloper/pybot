from bs4 import BeautifulSoup
import re
import requests
import datetime
import time

now = str(datetime.datetime.now())
day = now[:4] + now[5:7] + now[8:10]
num = int(time.strftime("%w"))
print(day)

req = requests.get("http://stu.sen.go.kr/sts_sci_md01_001.do?schulCode=B100000662&schulCrseScCode=4")
#print(req.text)
soup = BeautifulSoup(req.text, "html.parser")
#print(soup)
element = soup.find_all('tr')
#print(element[2])
element = element[2].find_all('td')

element = element[num]  # num
element = str(element)
element_filter = ['[', ']', '<td class="textC last">', '<td class="textC">', '</td>', '&amp;', '(h)', '.']
for element_string in element_filter :
    element = element.replace(element_string, '')
    #줄 바꿈 처리
    element = element.replace('<br/>', '\n')
    #모든 공백 삭제
    element = re.sub(r"\d", "", element)

print(element)