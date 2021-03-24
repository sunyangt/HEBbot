import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

first_name = 'MaDong'
last_name = 'Qiu'
email = 'ma@ma.com' ## 邮箱用于收确认信
phone = '8119995566'
birthDate = '11/11/1991'
zipcode = '78613' ## 你家的zipcode
distance = 50 ## 最远可接受的HEB距离，单位mile，一般在城里 40miles以内 20分钟找到， 20mile 以内2-3小时， 10mile以内一天时间
types = ["moderna", "pfizer"] ## 要打的疫苗品种



def Book(driver):
    # start booking
    try:
        driver.get('https://vaccine.heb.com/scheduler?q=' + zipcode)
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'View times')))
        root_div = driver.find_element_by_id('root')
        firstBlock = root_div.find_elements_by_link_text('View times')

        if isinstance(firstBlock, list):
            parentElement = firstBlock[0].find_element_by_xpath('../..')
            info_list = parentElement.text.lower().split('\n')
            dis = float(info_list[len(info_list) - 1].split(' ')[0])
            ok_type = False
            for type in types:
                if type in info_list:
                    ok_type = True
            if ok_type and dis < distance:
                parentElement.find_element_by_link_text('View times').click()
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//lightning-base-combobox[@class="slds-combobox_container"]')))
                if len(driver.find_elements_by_xpath('//lightning-base-combobox[@class="slds-combobox_container"]')) <= 0:
                    return False
                driver.find_elements_by_xpath('//lightning-base-combobox[@class="slds-combobox_container"]')[1].click()
                driver.find_element_by_xpath('//lightning-base-combobox-item[@id="input-14-0-14"]').click()
                driver.find_elements_by_xpath('//lightning-base-combobox[@class="slds-combobox_container"]')[2].click()
                driver.find_element_by_xpath('//lightning-base-combobox-item[@id="input-18-0-18"]').click()
                driver.find_element_by_xpath('//button[@title="Continue"]').click()
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@name="First_Name__c"]')))
                driver.find_element_by_xpath('//input[@name="First_Name__c"]').send_keys(first_name)
                driver.find_element_by_xpath('//input[@name="Last_Name__c"]').send_keys(last_name)
                driver.find_element_by_xpath('//input[@name="Email_Address__c"]').send_keys(email)
                driver.find_element_by_xpath('//input[@data-type="tel"]').send_keys(phone)
                driver.find_element_by_xpath('//input[@data-type="birthdate"]').send_keys(birthDate)
                driver.find_element_by_xpath('//lightning-base-combobox[@class="slds-combobox_container"]').click()
                driver.find_element_by_xpath('//lightning-base-combobox-item[@id="input-37-0-37"]').click()
                driver.find_elements_by_xpath('//lightning-base-combobox[@class="slds-combobox_container"]')[1].click()
                driver.find_element_by_xpath('//lightning-base-combobox-item[@id="input-45-1-45"]').click()
                driver.find_element_by_xpath('//button[@title="Schedule Appointment"]').click()
            else:
                return False;

        print('success')
        return True
    except:
        return False;


if __name__ == "__main__":

    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.set_page_load_timeout(100)


##    Login(driver, email, password)

    while(True):
        try:
            time.sleep(4)
            if Book(driver):
                break
        except KeyboardInterrupt:
            break
        except:
            pass
