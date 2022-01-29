##################################################################
# 功能：根据酒店名称及地点获取酒店最低价格
# 作者：胡文强
# E-mail：huwenqiang.hwq@protonmail.com

##################################################################

import urllib
import json
import requests

##################################################################
# 读取并处理json，将所得结果以dict的形式返回
def pre_process_info():
    try:
        with open('./hotel_dict.json', 'r') as previous_file:
            previous_data = previous_file.read()
    except:
        print ("Error: load input json file (hotel_dict.json) failed, check your file!")
    json_data = json.loads(previous_data)
    return json_data

##################################################################
# 获取网页，直接返回网页全部内容
def get_web_data(keywords):
    init_url = 'https://hotels.ctrip.com/hotels/list?city=1&optionType=Hotel&directSearch=0&optionName=' + str(keywords).strip()
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}
    try:
        material_resource = requests.get(init_url,headers=headers)
        return material_resource.text
    except:
        return -1

##################################################################
# 处理网页中获得的信息，并且返回此信息
def process_web_data(keywords):
    unprocessed_data = get_web_data(keywords)
    return


##################################################################
if __name__ == "__main__":
    for each in pre_process_info():
        print (each, pre_process_info()[each])
    # print(get_web_data('北京海兴大酒店'))
    # , get_web_data(pre_process_info()[each])