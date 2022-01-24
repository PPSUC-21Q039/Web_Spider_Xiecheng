import requests
from lxml import etree
from fake_useragent import UserAgent
import os, re, json, traceback, random, time
from openpyxl import workbook  # 写入Excel表所用
from fnmatch import fnmatch

# 启用时间
start = time.time()

# 构建数组存储数据
hotel_name = []  # 酒店名称
hotel_address = []  # 酒店地址
hotel_iphone = []  # 酒店电话
hotel_brand = []  # 酒店品牌
hotel_business = []  # 酒店所属集团

# 构建请求头
url = "https://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx"
headers = {
    'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://hotels.ctrip.com',
    'Referer': 'https://hotels.ctrip.com/hotel/beijing1',
    'accept': '*/*',
    'user-agent': str(UserAgent().random)
}

# 主代码
for i in range(1, 10):
    print("爬取第%d页" % i)
    proxy = ["202.108.22.5:80"]
    proxies = {"http": str(random.choice(proxy))}

    # page是页码（翻页），广州cityID是32（北京cityID是1）
    formData = {
        'cityId': 1,
        'page': i
    }

    # 发起网络请求
    r = requests.post(url, data=formData, headers=headers, proxies=proxies)
    r.raise_for_status()
    r.encoding = r.apparent_encoding  # 防止出现乱码现象

    # 解析 json 文件，提取酒店数据
    js = json.loads(r.text)
    json_data = json.loads(r.text)['hotelPositionJSON']

    for item in json_data:
        hotelName = item['name']
        hotelAdress = item['address']
        hotelUrl = item['url']

        hotel_name.append(hotelName)
        hotel_address.append(hotelAdress)

        # 在首页打开酒店url，获取电话号码，其中电话隐藏了，因此用正则直接提取
        new_hotelUrl = "https://hotels.ctrip.com" + item['url']
        req = requests.get(new_hotelUrl, headers=headers)
        page = req.text
        pattern = re.compile('<span id="J_realContact" data-real="(.*?)&nbsp;&nbsp', re.S)
        item_iphone = pattern.findall(page)
        hotel_iphone.append(item_iphone)  # 正则写入数据的形式是列表,这里再次把列表数据写入列表

        # xpath解析酒店品牌+集团
        html = etree.HTML(page)
        hotelBrand = html.xpath('//*[@id="base_bd"]/div[2]/a[3]/text()')

        if fnmatch(str(hotelBrand), "*区*"):
            hotel_brand.append("无")
        elif len(hotelBrand) == 0:
            hotel_brand.append("无")
        else:
            hotel_brand.append(hotelBrand)

        hotelBusiness = html.xpath('//*[@id="hotel_info_comment"]/div/span/text()')

        if len(hotelBusiness) == 0:
            hotel_business.append("无")
        else:
            hotel_business.append(hotelBusiness)

# 储存
wb = workbook.Workbook()
ws = wb.active
ws.append(["酒店名称", "地址", '电话号码', '酒店品牌', '酒店集团'])

for i in range(0, len(hotel_name)):
    ws.append([hotel_name[i], hotel_address[i], hotel_iphone[i][0], hotel_brand[i][0], hotel_business[i][0]])
# 存储位置：C:\Users\Administrator
wb.save("携程酒店数据.xlsx")

# 结束
end = time.time()
print("耗时(分钟)：", (end - start) / 60)
print("爬取页数：", len(hotel_name) / 25)
