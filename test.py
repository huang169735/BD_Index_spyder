import os
import random
from config import COOKIES



def createFile(provinceName, cityName):
    #keyword = data['word']
    parentPath = os.path.abspath(os.path.dirname(os.getcwd()))
    path = parentPath + r'/data/' + 'test' + '/' + provinceName + '/';
    # 如果不存在则创建相应目录
    if not os.path.exists(path):
        os.makedirs(path)
    f = open(path + cityName + '.txt', 'a+')
    f.write("aaaa\n")
    f.write("bbbb\n")
    f.close();

#createFile('广东','广州');
#print(COOKIES[random.choice(list(COOKIES))])