# %%
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
import time
import pyautogui
from selenium.webdriver.common.action_chains import ActionChains


def get_urls(urls,titles):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

    response = requests.get("https://www.liaoxuefeng.com/wiki/1016959663602400",headers = headers)  
    soup = bs(response.content, "html.parser")  
    menu_tag = soup.find_all(class_="uk-nav uk-nav-side")[1]

    dep=[0,0,0,0]
    for li in menu_tag.find_all("div"):  
        url = "http://www.liaoxuefeng.com" + li.a.get('href')  
        urls.append(url)
        i=int(li['depth'])
        dep[i]+=1
        for a in range(i+1,4):
            dep[a]=0
        titles.append('{:0=2d}.{}.{}{}'.format(dep[1],dep[2],dep[3],li.a.string))

def download_md(path,browser):
    # path='https://www.liaoxuefeng.com/wiki/1016959663602400/1017639890281664'
    browser.get(path)
    time.sleep(4)

    # pyautogui.click(800, 800)
    # pyautogui.hotkey('ctrl', 'a')
    # pyautogui.hotkey('ctrl', 'q')
    image_path=r'C:\Users\Theigrams\Desktop\aa.png'
    img_location = pyautogui.locateOnScreen(image_path, confidence=0.6)
    image_location_point = pyautogui.center(img_location)
    x, y = image_location_point
    pyautogui.click(x, y)

    anchor_button=browser.find_element_by_xpath('//*[@id="anchor"]')

    ActionChains(browser).move_to_element(anchor_button).perform()

    act_button=browser.find_element_by_xpath('/html/div/sr-read/sr-rd-crlbar/fap/panel-bg/panel/panel-tabs/panel-tab[2]/span')

    ActionChains(browser).move_to_element(act_button).perform()

    md_button=browser.find_element_by_xpath("/html/div/sr-read/sr-rd-crlbar/fap/panel-bg/panel/panel-groups/panel-group[2]/action-bar/sr-opt-gp[3]/actions/a[5]/button-mask/button-span")

    md_button.click()

urls = []
titles=[]
get_urls(urls,titles)

#%% 
option = webdriver.ChromeOptions()
option.add_argument("--user-data-dir="+r"C:/Users/Theigrams/AppData/Local/Google/Chrome/User Data/")
browser = webdriver.Chrome(chrome_options=option)

for url in urls:
    download_md(url,browser)

