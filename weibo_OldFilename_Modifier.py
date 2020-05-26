import os

m = "C:/Users/meng/Desktop/weibo/"
kw = os.listdir(m)

for k in kw:
    um = m + k
    i = os.listdir(um)
    for ea in i:
        name,dot = ea.split('.')
        os.rename(um + '/' + ea, um+ '/weibo_20200526_' + k + '.' + dot)
        print(um + '/weibo_20200526_' + k + '.' + dot)
        