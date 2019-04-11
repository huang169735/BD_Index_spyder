import json
import os
import random

Path = os.getcwd()+r"\bd_index_info.json"

def resolveJson():
    file = open(Path, "rb")
    return (json.load(file));

def getProvinces():
    fileJson = resolveJson();
    province = fileJson["provinces"];
#    for key in province:
#        print(key);
    return province;

def getProvinceName(id):
    province = getProvinces();
    name = province[id];
#    print(name);
    return name;

def getAllCitys():
    fileJson = resolveJson();
    cityList = fileJson["cityShip"];
    return cityList;

def getCitys(id):
    allCity = getAllCitys();
    citys = allCity[id];
    return citys;

def getProvinceName4City(cityId, provinces, citys):
    for privinceId in citys:
        for city in citys[privinceId]:
            if city['value'] == cityId:
                return city['label'], provinces[privinceId]
    return None;

#getProvinces(path);
#getCitys("901",path);
#getProvinceName("901",path)
#getProvinceName4City('94',getProvinces(),getAllCitys());