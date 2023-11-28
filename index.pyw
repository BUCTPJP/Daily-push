import requests
import time
import json
from bs4 import BeautifulSoup
import re 



link_pattern = r'<a href="https://www.163.com/dy/article/(.*?)" class="'
url = 'https://www.163.com/dy/media/T1603594732083.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}
TOKEN = 'e00e48376ff9482ca69a01b37e665499'
def pushplus(token,content,title='网易每日早报',template ='html',topic = 'p-l',channel = 'wechat'):
    url = 'http://www.pushplus.plus/send'
    data = {
        "token": token,
        "title": title,
        "content": content,
        "topic":topic,
        "channel":channel,
        "template":template
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=body, headers=headers)
    if response.status_code ==200:
        return 1
    return 0

def get_daily_news():
    res = requests.get(url=url,headers=headers).text
    link_res = re.findall(link_pattern,res)
    today_link = 'https://www.163.com/dy/article/'+link_res[0]
    today_res = requests.get(url=today_link,headers=headers).text
    soup = BeautifulSoup(today_res,'lxml')
    news = []
    targets = soup.find("div", class_="post_body").find_all('p')
    for each in targets:
        news.append(each)
    news = str(news[1])
    news_ = news.split('<br/>')
    #print(news_)
    del news_[0]
    del news_[0]
    del news_[17]
    #print(news_)
    txt = news_[0]+'\n'+news_[1]+'\n'+news_[2]+'\n'+news_[3]+'\n'+news_[4]+'\n'+news_[5]+'\n'+news_[6]+'\n'+news_[7]+'\n'+news_[8]+'\n'+news_[9]+'\n'+news_[10]+'\n'+news_[11]+'\n'+news_[12]+'\n'+news_[13]+'\n'+news_[14]+'\n'+news_[15]+'\n'+news_[16]+'\n'
    #print(txt)
    res = pushplus(TOKEN,txt)
    if res == 1:
        print('推送成功')
        time.sleep(2)
    else:
        print('推送失败，请检查')
        time.sleep(2)
    
def main_handler(*args):  # 腾讯云函数
    get_daily_news()

if __name__ =='__main__':
    get_daily_news()






#另一种解决方案，自行研究，但最后有一些小瑕疵
'''news_ = []
    i = 0
    for new in news:
        if i == 0:
            News = new.split('！')
            for New in News:
                news_.append(New)
                #news_.append('\\n')
            i =+ 1
        else:
            news_.append(new)
'''