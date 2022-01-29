from selenium import webdriver
from time import sleep
import xlwt  # 进行excel操作
#谷歌驱动 告诉电脑在哪打开浏览器
driver=webdriver.Chrome(executable_path="./chromedriver.exe")
#打开网页
driver.get("https://hotels.ctrip.com/hotels/list?countryId=1&city=1&optionId=1&optionType=City&directSearch=0&display=%E5%8C%97%E4%BA%AC&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=1")
#通过xpath点击搜索
driver.find_element_by_xpath("//*[@id='btnSearch']").click()
driver.implicitly_wait(20)#隐式休息20s 登录携程

names=[]
prices=[]
addresses=[]
percents=[]
peoples=[]
for i in range(1,11):
    for j in range(1,26):
        name=driver.find_element_by_xpath("//div[@id='hotel_list']/div["+str(j)+"]/ul[@class='hotel_item']/li[2]/h2/a")
        price=driver.find_element_by_xpath("//div[@id='hotel_list']/div["+str(j)+"]/ul/li[3]//a/span")
        address=driver.find_element_by_xpath("//div[@id='hotel_list']/div["+str(j)+"]/ul[@class='hotel_item']/li[2]/p")
        percent=driver.find_element_by_xpath("//div[@id='hotel_list']/div["+str(j)+"]/ul[@class='hotel_item']/li[4]/div//span[@class='total_judgement_score']/span")
        people=driver.find_element_by_xpath("//div[@id='hotel_list']/div["+str(j)+"]/ul[@class='hotel_item']/li[4]/div//span[@class='hotel_judgement']/span")

        names.append(name.get_attribute("textContent").replace('\n', '').replace('\t', ''))
        prices.append(price.get_attribute("textContent"))
        addresses.append(address.get_attribute("textContent").replace('\n', '').replace('\t', '').replace('【', '').replace("】", ''))
        percents.append(percent.get_attribute("textContent"))
        peoples.append(people.get_attribute("textContent"))
    driver.find_element_by_xpath("//*[@id='downHerf']").click()
    sleep(5)
    print("第"+str(i)+"页")
print("爬取完毕！")

#存数据
book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
sheet = book.add_sheet('携程', cell_overwrite_ok=True)  # 创建工作表
col = ("酒店名称","酒店价格","酒店地址","用户推荐","推荐人数")
for i in range(0, 5):
    sheet.write(0, i, col[i])  # 列名
for i in range(0,250):
    sheet.write(i+1,0,names[i])
for i in range(0,250):
    sheet.write(i+1,1,prices[i])
for i in range(0,250):
    sheet.write(i+1,2,addresses[i])
for i in range(0,250):
    sheet.write(i+1,3,percents[i])
for i in range(0,250):
    sheet.write(i+1,4,peoples[i])
book.save("携程.xls")  # 保存
print("关闭浏览器，保存数据")
