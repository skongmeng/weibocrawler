import requests
import weibo_comment
import weibo_formatter
import os

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
        js = rq.json()
        wb.get_one_page(js)
        page+=1
    print("Done crawling weibo id")
    
    post = 1
    efolder = folder.format(keyword)
    if not os.path.exists(efolder):
        os.makedirs(efolder)
    file = open(efolder + '/post.txt','w+',encoding='utf-8')
    for text in wb.weibo:
        print("Recording post information at post %d" % post)
        etext = wb.cleantext(text['text'])
        file.write(etext + '\n')
        post += 1
    file.close()
    print("Done recording post")
    
    if comment_page > 0:
        wb.comment = weibo_comment.get_coment(keyword,wb.weibo_id_list,comment_page)

    return wb

crawl("外星人",2,2,'2018-01-01')