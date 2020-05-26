import re
import requests
import time
import json
from bs4 import BeautifulSoup as bs
import html
import csv
from datetime import datetime, timedelta

date = datetime.now().strftime("%Y%m%d")

def standardize_date(created_at):
    """标准化微博发布时间"""
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M")
    if u"分钟" in created_at:
        minute = created_at[:created_at.find(u"分钟")]
        minute = timedelta(minutes=int(minute))
        time = (datetime.now() - minute).strftime("%H:%M")
    if created_at.count('-') != 0:
        date = created_at
    if ':' in created_at:
        time = created_at[created_at.find(":") - 2:created_at.find(":") + 3]
    if u'月' in created_at and u'日' in created_at:
        year = datetime.now().strftime("%Y")
        mon = created_at[:created_at.find(u"月")]
        day = created_at[created_at.find(u"月")+1:created_at.find(u"日")]
        date = '{}-{}-{}'.format(year,mon,day)
    return date,time

def get_one_comment(weibo_id,page_comment):
    user_agent  = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    cookie = "SINAGLOBAL=7709568831519.718.1550467270621; UOR=play.163.com,widget.weibo.com,www.google.com; SCF=AjnVMF2NVle1sS37tOVegLDNzQJt7IKpuDcAXhOk3VjSRhJTBYxeMn5fMyMytY7ntj9dgvKG0hIXOvdZGs6Zq3c.; SUHB=0k1SUBMSFfWfu2; ALF=1604417551; SUB=_2AkMqn30Sf8NxqwJRmPAdz2jka4t-zwvEieKcw4zJJRMxHRl-yT9kqlE6tRB6AR9T-7RvgO8AiZiK090GNPegYQjrWBcO; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W51K.JWxZD2Qko.R.jZSzgl; _ga=GA1.2.159240723.1574268374; __gads=ID=3b022267889b1b58:T=1574268376:S=ALNI_MaPx-vnrFDN4-czTF8YFz1xjA17gQ; ULV=1574536369407:18:10:1:4463290382838.025.1574536369236:1574311981042; TC-V5-G0=595b7637c272b28fccec3e9d529f251a"
    Headers = {'User-agent':user_agent,'Cookie':cookie}
    all_comment = []
    for p in range(1,page_comment+1):
        print("Crawling page {}".format(p))
        Curl = 'https://www.weibo.com/aj/v6/comment/big?ajwvr=6&id=%s&page=%s' % (weibo_id,p)
        r = requests.get(Curl,headers=Headers)
        t = r.text
        json_to_dict = json.loads(t)
        if json_to_dict['code'] == '100000':  # 如果该条微博有评论
            n_html = html.unescape(json_to_dict['data']['html'])
            soup = bs(n_html,'lxml')
            commentlist = soup('div',attrs={'class' : 'WB_text'})
            datetime = soup('div',attrs={'class' : 'WB_from S_txt2'})
            if(len(commentlist) == len(datetime)):
                for n in range(0,len(commentlist)):
                    c = str(commentlist[n])
                    d = str(datetime[n])
                    stripComment = re.sub(r'(<img.*?alt=)"(.*?)"(.*>)',r'\2',c)
                    stripComment = re.sub(r'<.*?>|\n','',stripComment)
                    match = re.search(r'(^.*?)(:|：)(.*:|：)?(.*$)',stripComment)
                    try:
                        name,comment = match.group(1),match.group(4)
                        dateNTime = re.sub(r'<.*?>|\n','',d)
                        dateNTime = standardize_date(dateNTime)
                        all_comment.append([dateNTime[0],dateNTime[1],Curl,name,comment,'None'])
                    except:
                        print("Cannot find information in comment")
                        
            else:
                print('The comments are missing time')
        else:
            break
        time.sleep(3)
    return all_comment

def get_coment(word,weibo_id_list,comment_page,stopper,time_sleep):
    filename = "weibo_" + date + "_" + word
    folder = "weibo/{}/{}"
    
    index = 0
    commentlist = []
    for id in weibo_id_list:
        commentFile = open(folder.format(word,filename + '.csv'),'a',encoding='utf-8',newline="")
        fieldnames = ['date','time','url','author', 'comment', 'emotion']
        writer = csv.DictWriter(commentFile, fieldnames=fieldnames)
        print("Crawling comment of post {}".format(id))
        commentlist = get_one_comment(id,comment_page)
        for comment in commentlist:
            writer.writerow({'date':comment[0],'time':comment[1],'url':comment[2],'author':comment[3],'comment':comment[4],'emotion':'None'})
        commentFile.close()
        index += 1
        
        if index % stopper == 0:
            time.sleep(time_sleep)


    print("Done crawling comment")    
    return commentlist

