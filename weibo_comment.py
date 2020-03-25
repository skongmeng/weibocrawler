import re
import requests
import time
import json
from bs4 import BeautifulSoup as bs
import html
import csv
from datetime import datetime, timedelta

#def get_tid():
#    """
#    获取tid,c,w
#    :return:tid
#    """
#    tid_url = "https://passport.weibo.com/visitor/genvisitor"
#    data = {
#        "cb": "gen_callback",
#        "fp": {
#            "os": "3",
#            "browser": "Chrome69,0,3497,100",
#            "fonts": "undefined",
#            "screenInfo": "1920*1080*24",
#            "plugins": "Portable Document Format::internal-pdf-viewer::Chrome PDF Plugin|::mhjfbmdgcfjbbpaeojofohoefgiehjai::Chrome PDF Viewer|::internal-nacl-plugin::Native Client"
#        }
#    }
#    req = requests.post(url=tid_url, data=data, headers=headers)
#
#    if req.status_code == 200:
#        ret = eval(req.text.replace("window.gen_callback && gen_callback(", "").replace(");", "").replace("true", "1"))
#        return ret.get('data').get('tid')
#    print("No tide")
#    return None
#
#
#def get_cookie():
#    """
#    获取完整的cookie
#    :return: cookie
#    """
#    tid = get_tid()
#    if not tid:
#        return None
#
#    cookies = {
#        "tid": tid + "__095"  # + tid_c_w[1]
#    }
#    url = "https://passport.weibo.com/visitor/visitor?a=incarnate&t={tid}" \
#          "&w=2&c=095&gc=&cb=cross_domain&from=weibo&_rand={rand}"
#    req = requests.get(url.format(tid=tid, rand=random.random()),
#                       cookies=cookies, headers=headers)
#    if req.status_code != 200:
#        print("!=200")
#        return None
#
#    ret = eval(req.text.replace("window.cross_domain && cross_domain(", "").replace(");", "").replace("null", "1"))
#
#    try:
#        sub = ret['data']['sub']
#        if sub == 1:
#            print("sub==1")
#            return None
#        subp = ret['data']['subp']
#    except KeyError:
#        print("KeyError")
#        return None
#    return sub,subp

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
#    cookievalue = get_cookie()
#    if cookievalue == None:
#        cookievalue = ('_2AkMqhVYDf8NxqwJRmfwRz23rZYl-yAnEieKc2afYJRMxHRl-yT83qk0jtRB6AQV468GPDFxyosrB_iJJ_KmWQuABBSfr', '0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhPk-nIbZ4cCK_7PAAb_nDH')
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
                    name,comment = match.group(1),match.group(4)
                    dateNTime = re.sub(r'<.*?>|\n','',d)
                    dateNTime = standardize_date(dateNTime)
                    all_comment.append([dateNTime[0],dateNTime[1],Curl,name,comment,'None'])
            else:
                print('The comments are missing time')
        else:
            break
        time.sleep(3)
    return all_comment

def get_coment(word,weibo_id_list,comment_page):
    folder = "weibo/{}/{}"
    commentFile = open(folder.format(word,"allcomment.csv"),'w+',encoding='utf-8',newline="")
    fieldnames = ['date','time','url','author', 'comment', 'emotion']
    #date; time; url links: person who post; label emotions if have, else label as None
    writer = csv.DictWriter(commentFile, fieldnames=fieldnames)
    writer.writeheader()
    commentFile.close()     
    

    for id in weibo_id_list:
#            efolder = folder.format(word,id)
#            file = open(efolder + '/comment.txt','w+',encoding='utf-8')
        commentFile = open(folder.format(word,"allcomment.csv"),'a',encoding='utf-8',newline="")
        writer = csv.DictWriter(commentFile, fieldnames=fieldnames)
        print("Crawling comment of post {}".format(id))
        commentlist = get_one_comment(id,comment_page)
        for comment in commentlist:
#                file.write(comment[0] + ":" + comment[1] + '\n')
            writer.writerow({'date':comment[0],'time':comment[1],'url':comment[2],'author':comment[3],'comment':comment[4],'emotion':'None'})
#            file.close()
        commentFile.close()

    print("Done crawling comment")    
    return commentlist
