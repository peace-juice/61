#   todo 本代码文件只爬取了女生类的小说
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
import csv
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains


url='https://www.zongheng.com/books?'
#   添加参数，阻止自动关闭浏览器
options = Options()
options.add_experimental_option("detach", True)  # 阻止自动关闭

#   创建微软浏览器的浏览器驱动
driver=webdriver.Edge(options=options)
#   创建一个用于缓慢滑动的
actions = ActionChains(driver)

#   打开网页
driver.get(url)

#   网页全屏
driver.maximize_window()
time.sleep(5)

#   todo 点击女生类型的小说
girl_button=driver.find_element(By.XPATH,'/html/body/div[1]/div/section/section/section/section[1]/div[1]/div[2]')
girl_button.click()
time.sleep(2)

#   todo 循环爬取页数
for u in range(1,120):
    print("当前在第",u,"页爬取数据")
    #   滑到页面的底部
    # 缓慢滚动到页面底部
    for _ in range(10):  # 分10步滚动
        actions.scroll_by_amount(0, 500).perform()  # 每次滚动500像素
        time.sleep(0.3)  # 控制滚动速度

    #   拿到网页的html源码
    html_str = driver.page_source
    #   将字符串转化为xml格式，方便下面使用xpath拿到数据
    html = etree.HTML(html_str)

    """
    数据结构是div嵌套div
    """
    #   todo 拿到最外层的div
    max_div = html.xpath('/html/body/div[1]/div/section/section/section/section[2]/div[2]')

    #   todo 定义集合，存放数据
    rows = []

    #   通过最外层div进行循环遍历  拿到
    for div in max_div:
        #   todo 拿到小说的名字集合
        names = div.xpath('//div[@class="nav-content--main-item-content"]/a[1]/text()')
        #   列表推导式
        names = [name.strip() for name in names]
        print("小说名字集合长度:", len(names))
        print(names)

        #   todo 拿到读取小说的页面的url
        info_urls = div.xpath('//div[@class="nav-content--main-item-content"]/a[1]/@href')
        print("小说的页面的url长度:", len(info_urls))
        print(info_urls)

        #   todo 拿到小说图片的连接
        images = div.xpath('//a[@class="nav-content--main-item-img-cover global-radius global-book--frame"]/img/@src')
        print("小说图片的连接集合长度:", len(images))
        print(images)

        #   todo 拿到小说作者的用户名
        user_names = div.xpath('//div[@class="nav-content--main-item-keywords ellipsis"]/a[1]/text()')
        print("小说作者的用户名集合长度:", len(user_names))
        print(user_names)

        #   todo 拿到小说作者的主页的url
        user_urls = div.xpath('//a[@class="nav-content--main-item-title ellipsis global-hover"]/@href')
        print("作者的主页的url集合长度:", len(user_urls))
        print(user_urls)

        #   todo 拿到小说的类型
        book_class = div.xpath('//div[@class="nav-content--main-item-keywords ellipsis"]/span[2]/text()')
        print("小说的类型集合长度:", len(book_class))
        print(book_class)

        #   todo 拿到目前小说的状态(是连载还是已经完结)
        book_status = div.xpath('//div[@class="nav-content--main-item-keywords ellipsis"]/span[4]/text()')
        print("目前小说的状态集合长度:", len(book_status))
        print(book_status)

        #   todo 拿到小说目前的字数
        number_words = div.xpath('//div[@class="nav-content--main-item-keywords ellipsis"]/span[6]/text()')
        print("小说目前的字数集合长度:", len(number_words))
        print(number_words)

        #   todo 拿到小说的简介
        jianjies = div.xpath('//a[@class="nav-content--main-item-desc ellipsis-two-lines global-hover"]/text()')
        jianjies = [x.strip().replace("\n", "") for x in jianjies]
        print("小说简介集合长度:", len(jianjies))
        print(jianjies)

        #   todo chapter(章节)拿到目前小说最新的章节
        chapters = div.xpath('//a[@class="chapter-left ellipsis"]/span/text()')
        print("小说章节集合长度:", len(chapters))
        print(chapters)

        #   todo 拿到最新章节的url
        new_chapter_urls = div.xpath('//a[@class="chapter-left ellipsis"]/@href')
        print("最新章节集合长度:", len(new_chapter_urls))
        print(new_chapter_urls)

        #   todo 拿到小说最新更新的时间
        times = div.xpath('//div[@class="chapter-right"]/span/text()')
        print("最新更新时间集合长度:", len(times))
        print(times)

        #   todo 将这一页的数据汇总到一个列表里面
        for x in range(0, 20):
            rows.append(
                [
                    names[x], info_urls[x], images[x], user_names[x], user_urls[x],
                    book_class[x], book_status[x], number_words[x], jianjies[x],
                    chapters[x], new_chapter_urls[x], times[x],"女"
                ]
            )

        for j in rows:
            print(j)

        # #   todo 将这一页的数据追加到ods
        with open('source.csv','a',newline='',encoding='utf-8') as file:
            #   创建csv写入对象
            writer=csv.writer(file)
            #   写入数据
            writer.writerows(rows)

        #   todo 点击下一页  由于button按钮存在元素遮挡,所以点击不了
        # next_button=driver.find_element(By.XPATH,'//*[@id="__layout"]/section/section/section/section[2]/div[2]/div[21]/div/button[2]')
        # driver.execute_script("arguments[0].scrollIntoView();", next_button)
        # next_button.click()
        #   todo 定位到切换页面的输入框
        next_input_button = driver.find_element(By.XPATH,
                                                '//*[@id="__layout"]/section/section/section/section[2]/div[2]/div[21]/div/span[3]/div/input')
        #   todo 清空输入框（可选）
        next_input_button.clear()
        #   todo 在输入框输入要翻页的页码
        next_input_button.send_keys(str(u +1))
        #   todo 模拟键盘的回车
        next_input_button.send_keys(Keys.RETURN)
        time.sleep(5)




driver.quit()


