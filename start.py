# 1. "Make Sure to have an Active and Fast Speed Internet Connection on your Device"
# 2. Set Chrome Driver to path
# 3. Don't minimize the browser window

from selenium import webdriver
import time
import pandas as pd

driver = webdriver.Chrome()
driver.set_window_size(1080, 1020)
driver.set_window_position(0,0)

driver.get("https://www.propertiesguru.com/residential-search/2bhk-residential_apartment_flat-for-sale-in-new_delhi")



print(
    "\n\t -> Wait for a while, the site is being scraped for data \n\t -> Excel file will get saved at this python script's location named 'Output_Web_Scrap.xlsx'")

print("—————————————————————————————————————————————————————————————————————————————————————————")

# Web scrapper to scroll to the bottom - for full content load


def scrolltobottom():
    time.sleep(3)  # Allow 2 seconds for the web page to open
    scroll_pause_time = 4  # You can set your own pause time. My laptop is a bit slow so I use 1 sec
    screen_height = driver.execute_script(
        "return window.screen.height;")  # get the screen height of the web
    i = 1

    while True:
        # scroll one screen height each time
        driver.execute_script(
            "window.scrollTo(0, {screen_height}*{i});".format(
                screen_height=screen_height, i=i))
        i += 1
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script(
            "return document.body.scrollHeight;")
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height) * i > scroll_height:
            break

    time.sleep(5)


#calling function to scroll to load full content
scrolltobottom()

#Locating elements

heading = driver.find_elements_by_class_name("filter-pro-heading")

price = driver.find_elements_by_class_name("property-price")

area = driver.find_elements_by_class_name("col-4")

facing = driver.find_elements_by_class_name("col-3")

status = driver.find_elements_by_class_name("col-5")

seller = driver.find_elements_by_class_name("owner-name")

details = driver.find_elements_by_class_name("pro-list")

# List to store location
loc_list = []

cat_list = []

# *********** Functions to fetch data and text *********


def headingfnc():
    data_list = []
    for single in heading:
        new = single.text
        index_loc = new.index('\n')

        # try:
        #     index_cat = new.index('/')
        # except:
        #     cat_list.append(new[(index_cat-3) : index_loc])
        # else:
        #     cat_list.append(new[index_cat + 1: index_loc])

        loc_list.append(new[index_loc + 1:])
        new = new[0:(index_loc)]
        data_list.append(new)
    return data_list


def areafnc():
    data_list = []
    for single in area:
        new = single.text[4:]  #to get text and slice 'Area'
        data_list.append(new[1:])  #to slice \n
    return data_list


def facingfnc():
    data_list = []
    for single in facing:
        refined_facing = single.find_elements_by_class_name("block")
        #get only col-4 which has block class in sub element
        for two in refined_facing:
            new = single.text[6:]  #to get text and slice 'Facing'
            data_list.append(new[1:])  #to slice \n
    return data_list


def pricefnc():
    data_list = []
    for single in price:

        data_list.append(single.text[2:])  #to slice \n
    return data_list


def statusfnc():
    data_list = []
    for single in status:
        new = single.text[6:]  #to get text and slice 'Area'
        data_list.append(new[1:])  #to slice \n
    return data_list


def sellerfnc():
    data_list = []
    for single in seller:
        data_list.append(single.text)
    return data_list


def detailsfnc():
    data_list = []
    for single in details:

        new = single.text
        new = new.replace(
            '\n', ', '
        )  #to replace \n which are in between the text and separating them with comma
        data_list.append(new)

    return data_list


#Dictionary

data = {
    'Title': headingfnc(),
    'Location': loc_list,
    'Area': areafnc(),
    'Facing': facingfnc(),
    'Details': detailsfnc(),
    'Price': pricefnc(),
    'Status': statusfnc(),
    'Seller': sellerfnc(),
}

# Data To Excel file

df = pd.DataFrame(data,
                  columns=[
                      'Title', 'Location', 'Area', 'Facing', 'Details',
                      'Price', 'Status', 'Seller'
                  ])

df.to_excel('Output_Web_Scrap.xlsx',
            sheet_name='Properties Guru Search - 1 by Pranjal')
print("\n Your Excel file is Saved !!")



loc_list=[]

print(
    "—————————————————————————————————————————————————————————————————————————————————————————"
)

print("Note: If you don't get the data of all the elements on the webpage :\n\n 1. Fix your Internet Connection\n 2. Increase the scroll_pause_time in this code")

print("—————————————————————————————————————————————————————————————————————————————————————————")

inputkey = input(
    "\n—> Enter '1' to apply 3BHK and 4BHK filter and get the data in New File (named 'Filtered_Output_Web_Scrap.xlsx') or\n\t '2' to exit the program\n\t\t:" 
)

if inputkey == '1':
    #increasing window size because site is not mobile friendly (small screen) and elements aren't getting located by xpath
    driver.set_window_size(1440, 1020)
    
    
    print(
        "Wait for a While.. Data is being Scrapped after applying the filters")
    
    # driver.get("https://www.propertiesguru.com/residential-search/2bhk-residential_apartment_flat-for-sale-in-new_delhi")
    
    driver.refresh()
    
    time.sleep(10) #to load the webpage
    
    element = driver.find_element_by_xpath('//*[@id="properties"]/div/div[1]/h1')
    driver.execute_script("return arguments[0].scrollIntoView(true);", element)
    
    time.sleep(3)
    filterapply = driver.find_element_by_class_name('bedroomdropdown').click()

    #applying 3 bhk and 4 bhk Filter
    

    bhk_3 = driver.find_element_by_xpath('//*[@id="navbarNavDropdown"]/ul[1]/li[3]/ul/li/div/ul/li[3]/label/span').click()
    bhk_4 = driver.find_element_by_xpath('//*[@id="navbarNavDropdown"]/ul[1]/li[3]/ul/li/div/ul/li[4]/label/span').click()

    #calling function to scroll to load full content
    scrolltobottom()
    time.sleep(5)

    #Locating Elements Once Again..

    heading = driver.find_elements_by_class_name("filter-pro-heading")
    price = driver.find_elements_by_class_name("property-price")
    area = driver.find_elements_by_class_name("col-4")
    facing = driver.find_elements_by_class_name("col-3")
    status = driver.find_elements_by_class_name("col-5")
    seller = driver.find_elements_by_class_name("owner-name")
    details = driver.find_elements_by_class_name("pro-list")

    #Dictionary

    data_new = {
        'Title': headingfnc(),
        'Location': loc_list,
        'Area': areafnc(),
        'Facing': facingfnc(),
        'Details': detailsfnc(),
        'Price': pricefnc(),
        'Status': statusfnc(),
        'Seller': sellerfnc(),
    }

    # Data To Excel file

    df2 = pd.DataFrame(data_new,
                      columns=[
                          'Title', 'Location', 'Area', 'Facing', 'Details',
                          'Price', 'Status', 'Seller'
                      ])

    df2.to_excel('Filtered_Output_Web_Scrap.xlsx',
                sheet_name='Properties Guru Filtered Search - 2 by Pranjal')
    print("\n Your Excel file is Saved !!")
    print("—————————————————————————————————————————————————————————————————————————————————————————")
    print("Note: If you don't get the data of all the elements on the webpage :\n\n 1. Fix your Internet Connection\n 2. Increase the scroll_pause_time in this code")
    
    



driver.quit()