from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import json
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename="./spider.log")
logger = logging.getLogger()
option = ChromeOptions()
option.add_argument(r"user-data-dir=D:\AppData\AppData\Local\Google\Chrome\User Data")
option.add_experimental_option("excludeSwitches", ["enable-automation"])
option.add_argument("--disable-blink-features=AutomationControlled")
option.add_experimental_option("useAutomationExtension", False)
browser = webdriver.Chrome(options=option)  # 初始化浏览器对象
browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': 'Object.defineProperty(navigator,"webdriver",{get:() => underfined})'
})


def extract(review_cards):
    all_reviews = []  # 初始化一个列表来存储所有评论的信息
    for card in review_cards:
        try:
            # 提取信息
            user_avatar = card.find_element(By.CSS_SELECTOR, ".user img").get_attribute('src')
            username = card.find_element(By.CSS_SELECTOR, ".info .name").text
            room_type = card.find_element(By.CSS_SELECTOR, ".user-left .other li span").text
            check_in_info = card.find_element(By.CSS_SELECTOR, "i.u-icon-ic_new_calendar_line + span").text
            family_info = card.find_element(By.CSS_SELECTOR, "i.u-icon-beach + span").text
            review_info = card.find_element(By.CSS_SELECTOR, "i.u-icon-game + span").text
            score = card.find_element(By.CSS_SELECTOR, ".m-score_single strong").text
            comment = card.find_element(By.CSS_SELECTOR, ".comment p").text
            useful = card.find_element(By.CSS_SELECTOR, ".favrator .useful").text
            review_date = card.find_element(By.CSS_SELECTOR, ".reviewDate").text
            hotel_reply = card.find_element(By.CSS_SELECTOR, ".reply p").text
            # 提取评论图片链接
            images = card.find_elements(By.CSS_SELECTOR, ".pictures li img")
            image_urls = [img.get_attribute('src') for img in images]

            # 将提取的信息添加到列表中
            all_reviews.append({
                "User Avatar": user_avatar,
                "Username": username,
                "Room Type": room_type,
                "Check-in Info": check_in_info,
                "Family Info": family_info,
                "Review Info": review_info,
                "Score": score,
                "Comment": comment,
                "Image URLs": image_urls,
                "Useful": useful,
                "Review Date": review_date,
                "Hotel Reply": hotel_reply
            })
        except Exception as e:
            logger.error(f"错误提取: {e}")
            # Optionally, append a None or a dict with error details to all_reviews
            all_reviews.append(None)  # or {'error': str(e)}

    return all_reviews


def save2json(data, file_path):
    with open(file_path, 'w') as json_file:
        logger.info(f"保存到{file_path}")
        json.dump(data, json_file, indent=4)


def create_folder(parent_folder_name, folder_name):
    path = os.path.join(parent_folder_name, folder_name)
    try:
        os.makedirs(path, exist_ok=True)
        logger.info(f"文件夹 '{path}' 已创建或已存在")
    except OSError as e:
        logger.error(f"创建文件夹时出错: {e}")
    return path


def main(hotels):
    for hotel in hotels:
        for name, url in hotel.items():
            logger.info(f"正在访问: {name}, 网址: {url}")
            parent_folder_name = "data"
            folder_name = name
            folder_path = create_folder(parent_folder_name, folder_name)
            browser.get(url)
            index = 1
            while True:
                try:
                    file_name = f"index{index}.json"
                    file_path = os.path.join(folder_path, file_name)
                    # 等待页面加载完毕
                    wait = WebDriverWait(browser, 10)
                    # 定位到所有的评论卡片
                    review_cards = wait.until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".m-reviewCard-item")))
                    all_reviews = extract(review_cards)
                    save2json(all_reviews, file_path)
                    index = index + 1
                    time.sleep(5)
                    # 为了演示，让浏览器停留一段时间
                    # 找到"下一页"按钮，它的类名是'forward active'
                    next_page_button = browser.find_element(By.CSS_SELECTOR, "a.forward.active")
                    # 点击"下一页"按钮
                    next_page_button.click()
                except NoSuchElementException:
                    # 如果没有找到"下一页"按钮，我们可能已经在最后一页
                    logger.info("已经到达最后一页。")
                    break
                except Exception as e:
                    # 如果发生其他异常，打印异常信息并退出循环
                    logger.error(f"发生错误：{e}")
                    break
    # 完成后关闭浏览器
    browser.quit()


if __name__ == '__main__':
    hotels = [
        {"合肥融侨皇冠假日酒店": "https://hotels.ctrip.com/hotels/3999801.html?cityid=278"},
    ]
    # 遍历酒店列表
    main(hotels)
