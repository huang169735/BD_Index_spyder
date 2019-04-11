from get_index import BaiduIndex
if __name__ == "__main__":
    """
        最多一次请求5个关键词
        抓取全国地级市全部数据
    """
    baidu_index = BaiduIndex([ '故宫','天坛','长城','天安门','颐和园'], '2017-09-30', '2018-10-01')

    """
        根据指定省份编码抓取省份相关地级市关键词
    """
#    province = ["931", "933", "934"]
#    baidu_index = BaiduIndex(['故宫', '天坛'], '2017-09-30', '2018-10-01', 'province', province)

    """
        根据指定市区编码抓取关键词
    """
#    city = ["678", "691"]
#    baidu_index = BaiduIndex(['故宫', '天坛'], '2017-09-30', '2018-10-01', 'city', city)