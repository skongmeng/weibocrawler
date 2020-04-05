import requests
import weibo_comment
import weibo_formatter
import os
import csv

def export_data(keyword,alist):
    folder = "weibo/{}/{}"
    commentFile = open(folder.format(keyword,"allcomment.csv"),'w+',encoding='utf-8',newline="")
    fieldnames = ['date','time','url','author', 'comment', 'emotion']
    writer = csv.DictWriter(commentFile, fieldnames=fieldnames)
    writer.writeheader()
    commentFile.close() 
    commentFile = open(folder.format(keyword,"allcomment.csv"),'a',encoding='utf-8',newline="")
    writer = csv.DictWriter(commentFile, fieldnames=fieldnames)
    for comment in alist:
        writer.writerow({'date':comment[0],'time':comment[1],'url':comment[2],'author':comment[3],'comment':comment[4],'emotion':'None'})
    commentFile.close()

def crawl(keyword,post_page,comment_page,since_date):
    url='https://m.weibo.cn/api/container/getIndex?type=all&queryVal={}&featurecode=20000320&luicode=10000011&lfid=106003type%3D1&title={}&containerid=100103type%3D1%26q%3D{}'.format(keyword,keyword,keyword)
    folder = "weibo/{}"
    wb = weibo_formatter.Weibo(since_date)
    page=1
    while page <= post_page:
        print("Crawling keyword at page %d" % page)
        url_1=url+'&page='+str(page)
        rq = requests.get(url_1)
        if not rq.ok:
            print("Error occurred")
            break
        try:
            js = rq.json()
            wb.get_one_page(js,url_1)
        except:
            print("Abnormal website")
            print(rq.content)
        page+=1
    print("Done crawling weibo id")
    
    post = 1
    efolder = folder.format(keyword)
    if not os.path.exists(efolder):
        os.makedirs(efolder)
    file = open(efolder + '/post.txt','w+',encoding='utf-8')
        #date; time; url links: person who post; label emotions if have, else label as None
    for text in wb.weibo:
        print("Recording post information at post %d" % post)
        etext = wb.cleantext(text['text'])
        file.write(etext + '\n')
        wb.formatted.append([text['created_at'],"",wb.url[post-1],text['screen_name'],etext,"None"])
        post += 1
    file.close()
    print("Done recording post")
    export_data(keyword,wb.formatted)
    wb.comment = weibo_comment.get_coment(keyword,wb.weibo_id_list,comment_page,5,10*60)
    #here to change the crawling interval at the last two parameter
    #last second parameter is the number of post crawl to stop for a while, note that 1 post has many comment
    #last parameter is the time in second of the interval
    return wb

#crawl(keyword searching,post page(1post has about 20 post,comment page(1 page has unknown comment),since what date))
wb = crawl("杂菜",5,10,'2018-01-01')