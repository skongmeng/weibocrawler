import requests
import weibo_formatter
import math

"""===================================配置============================================="""
filter = 1  #1:原创 0:包括转发
since_date = '2018-01-01'  # 起始时间，即爬取发布日期从该值到现在的微博，形式为yyyy-mm-dd
user_id_list = ['1669879400']
                #Sample:
                #1223178222 胡歌
                #1669879400 迪丽热巴
                #1729370543 郭碧婷
"""==================================================================================="""

def get_json(params):
    """获取网页中json数据"""
    url = 'https://m.weibo.cn/api/container/getIndex?'
    r = requests.get(url, params=params)
    return r.json()

def get_weibo_json(user_id,page):
    """获取网页中微博json数据"""
    params = {'containerid': '107603' + str(user_id), 'page': page}
    js = get_json(params)
    return js

def main():
    wb = weibo_formatter.Weibo()
    wb.user_id_list = user_id_list
    
    for user_id in user_id_list:         
        params = {'containerid': '100505' + str(user_id)}
        js = get_json(params)
        wb.get_user_info(js)
        weibo_count = wb.user['statuses_count']
        page_count = int(math.ceil(weibo_count / 10.0))
        for page in range(1,page_count):
            js = get_weibo_json(user_id,page)
            wb.get_one_page(js)
            print("Crawling %d pages" % page)
    print(wb.weibo_id_list)
    return wb
    
if __name__ == '__main__':
    main()

			