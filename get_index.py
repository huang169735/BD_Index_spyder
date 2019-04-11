from config import COOKIES
from urllib.parse import urlencode
from collections import defaultdict
import datetime
import requests
import json
import baidu_city_info
import os
import time
import random


headers = {
    'Host': 'index.baidu.com',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
}

parentPath = os.path.abspath(os.path.dirname(os.getcwd()))

class BaiduIndex:
    """
        百度搜索指数
    """

    def __init__(self, keywords, start_date, end_date, type, idList):
        self._keywords = keywords if isinstance(keywords, list) else keywords.split(',')
        self.provinces = baidu_city_info.getProvinces()
        self.citys = baidu_city_info.getAllCitys()
#        self._startdate = datetime.datetime.strptime(start_date, '%Y-%m-%d')
#        self._enddate = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        self._time_range_list = self.get_time_range_list(start_date, end_date)
#       self._all_kind = ['all', 'pc', 'wise']
        self._all_kind = ['all']
#        self.result = {keyword: defaultdict(list) for keyword in self._keywords}
        if type is None:
            self.get_result()
        elif type == 'province':
            self.get_province_result(idList)
        elif type == 'city':
            self.get_city_result(idList)
        print('数据抓取完成......在data文件夹中查看数据')
    def get_result(self):
        #按照全国省市遍历
        for provinceId in  self.provinces:
            provinceName = self.provinces[provinceId];
            for city in self.citys[provinceId]:
                cityName = city['label'];
                cityId = city['value'];
                result = {keyword: defaultdict(list) for keyword in self._keywords}
                self.grab_data(result, cityId, provinceName, cityName);

    def get_province_result(self,provinces):
        #按照需求省市遍历
        for provinceId in provinces:
            provinceName = self.provinces[provinceId];
            for city in self.citys[provinceId]:
                cityName = city['label'];
                cityId = city['value'];
                result = {keyword: defaultdict(list) for keyword in self._keywords}
                self.grab_data(result, cityId, provinceName, cityName);

    def get_city_result(self,citys):
        #按照需求市遍历
        for cityId in citys:
            cityName, provinceName = baidu_city_info.getProvinceName4City(cityId,self.provinces,self.citys)
            result = {keyword: defaultdict(list) for keyword in self._keywords}
            self.grab_data(result, cityId, provinceName, cityName);

    def grab_data(self,result,cityId,provinceName,cityName):
        for start_date, end_date in self._time_range_list:
            # 每次请求后随机休眠1-5秒(数值，精度)
            sleepTime = random.uniform(1, 5)
            encrypt_datas, uniqid = self.get_encrypt_datas(start_date, end_date, cityId)
            key = self.get_key(uniqid)
            for encrypt_data in encrypt_datas:
                for kind in self._all_kind:
                    encrypt_data[kind]['data'] = self.decrypt_func(key, encrypt_data[kind]['data'])
                self.format_data(result, encrypt_data)
            time.sleep(round(sleepTime, 2));
        # 生成数据文件
        self.createFile(result, provinceName, cityName);

    def createFile(self, result, provinceName, cityName):
        for keyword in result:
            path = parentPath + r'/data/' + keyword + '/' + provinceName + '/';
            # 如果不存在则创建相应目录
            if not os.path.exists(path):
                os.makedirs(path)
            #将数据写出
            f = open(path + cityName + '.txt', 'w+')
            for data in result[keyword]['all']:
                f.write(data['date'] + "    " + data['index'] + '\n');
            f.close();
            print("数据抓取成功===> "+keyword+"("+provinceName+'-'+cityName+')');

    def get_encrypt_datas(self, start_date, end_date, area):
        """
        :start_date; str, 2018-10-01
        :end_date; str, 2018-10-01
        """
        request_args = {
            'word': ','.join(self._keywords),
            'startDate': start_date,
            'endDate': end_date,
            'area': area,
        }
        url = 'http://index.baidu.com/api/SearchApi/index?' + urlencode(request_args)
        html = self.http_get(url)
        datas = json.loads(html)
        uniqid = datas['data']['uniqid']
        encrypt_datas = []
        for single_data in datas['data']['userIndexes']:
            encrypt_datas.append(single_data)
        return (encrypt_datas, uniqid)

    def get_key(self, uniqid):
        """
        """
        url = 'http://index.baidu.com/Interface/api/ptbk?uniqid=%s' % uniqid
        html = self.http_get(url)
        datas = json.loads(html)
        key = datas['data']
        return key

    def format_data(self, result, data):
        """
        """
        keyword = data['word']
        time_len = len(data['all']['data'])
        start_date = data['all']['startDate']
        cur_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        for i in range(time_len):
            formated_data = {
                'date': cur_date.strftime('%Y-%m-%d')
            }
            for kind in self._all_kind:
                formated_data['index'] = data[kind]['data'][i]
                result[keyword][kind].append(formated_data)

            cur_date += datetime.timedelta(days=1)

    @staticmethod
    def http_get(url):
        cookies = COOKIES[random.choice(list(COOKIES))]
        headers['Cookie'] = cookies
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None

    @staticmethod
    def get_time_range_list(startdate, enddate):
        """
        max 6 months
        """
        date_range_list = []
        startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
        while 1:
            tempdate = startdate + datetime.timedelta(days=300)
            if tempdate > enddate:
                all_days = (enddate-startdate).days
                date_range_list.append((startdate, enddate))
                return date_range_list
            date_range_list.append((startdate, tempdate))
            startdate = tempdate + datetime.timedelta(days=1)

    @staticmethod
    def decrypt_func(key, data):
        """
        decrypt data
        """
        a = key
        i = data
        n = {}
        s = []
        for o in range(len(a)//2):
            n[a[o]] = a[len(a)//2 + o]
        for r in range(len(data)):
            s.append(n[i[r]])
        return ''.join(s).split(',')

if __name__ == '__main__':
    baidu_index = BaiduIndex(['张艺兴', '黄渤'], '2016-08-11', '2018-09-11')
    for data in baidu_index('孙红雷', 'all'):
        print(data)
