import pathlib
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import datetime

path = Path("drivers","chromedriver.exe")
now = datetime.datetime.now()
log_path = Path("logs",f'log_{now.strftime("%d_%m_%Y_%H%M")}.log')
driver = webdriver.Chrome(executable_path= path)
driver.get('https://www.saucedemo.com')

def save_log(text):
    with open(log_path, "a", encoding="UTF-8") as example_file:
        example_file.write(f'{now.strftime("%d/%m/%Y %H:%M:%S")} - {text}\n')

login_standard_user = 'standard_user'
password_all = 'secret_sauce'
right_url = 'https://www.saucedemo.com/inventory.html'

username = driver.find_element(By.CSS_SELECTOR,'input#user-name')
username.send_keys(login_standard_user)
password = driver.find_element(By.CSS_SELECTOR,'input#password')
password.send_keys(password_all)
password.send_keys(Keys.RETURN)
# --- login attempt ---
assert driver.current_url == right_url, save_log('login failed')
save_log('successful login')
# --- buy 1st product ---
element = driver.find_element(By.CSS_SELECTOR,'a#item_0_title_link')
product1_name = element.text
element = driver.find_element(By.XPATH,'//*[@id="inventory_container"]/div/div[2]/div[2]/div[2]/div') 
product1_price = element.text[1:]
element = driver.find_element(By.CSS_SELECTOR,'button#add-to-cart-sauce-labs-bike-light')
save_log(f'try to put in cart 1st product: {product1_name} - $ {product1_price}')
element.click()

# --- buy 2st product ---
element = driver.find_element(By.CSS_SELECTOR,'a#item_2_title_link')
product2_name = element.text
element = driver.find_element(By.XPATH,'//*[@id="inventory_container"]/div/div[5]/div[2]/div[2]/div') 
product2_price = element.text[1:]
element = driver.find_element(By.CSS_SELECTOR,'button#add-to-cart-sauce-labs-onesie')
save_log(f'try to put in cart 2nd product: {product2_name} - $ {product2_price}')
element.click()

# to cart
element = driver.find_element(By.CSS_SELECTOR,'a.shopping_cart_link')
element.click()

# cart summary
# 1st product
element = driver.find_element(By.CSS_SELECTOR,'a#item_0_title_link')
product1_cart_name = element.text
element = driver.find_element(By.XPATH,'//*[@id="cart_contents_container"]/div/div[1]/div[3]/div[2]/div[2]/div')
product1_cart_price = element.text[1:]
save_log(f'1st product in cart: {product1_cart_name} - $ {product1_cart_price}')
# 2nd product
element = driver.find_element(By.CSS_SELECTOR,'a#item_2_title_link')
product2_cart_name = element.text
element = driver.find_element(By.XPATH,'//*[@id="cart_contents_container"]/div/div[1]/div[4]/div[2]/div[2]/div')
product2_cart_price = element.text[1:]
save_log(f'2nd product in cart: {product2_cart_name} - $ {product2_cart_price}')

#names matching (selected with cart) 
assert product1_name == product1_cart_name, save_log('FAIL. product1 names are different')
save_log('OK. product1 names are similar')
assert product1_price == product1_cart_price, save_log('FAIL. product1 prices are different')
save_log('OK. product1 prices are similar')
assert product2_name == product2_cart_name, save_log('FAIL. product2 names are different')
save_log('OK. product2 names are similar')
assert product2_price == product2_cart_price, save_log('FAIL. product2 prices are different')
save_log('OK. product2 prices are similar')

#checkout
element = driver.find_element(By.CSS_SELECTOR,'button#checkout')
element.click()
element = driver.find_element(By.CSS_SELECTOR,'input#first-name')
element.send_keys('Alexander')
element = driver.find_element(By.CSS_SELECTOR,'input#last-name')
element.send_keys('Lukin')
element = driver.find_element(By.CSS_SELECTOR,'input#postal-code')
element.send_keys('660000')
save_log('trying to checkout')
element = driver.find_element(By.CSS_SELECTOR,'input#continue')
element.click()

#summary
# 1st product
element = driver.find_element(By.CSS_SELECTOR,'a#item_0_title_link')
product1_summary_name = element.text
element = driver.find_element(By.XPATH,'//*[@id="checkout_summary_container"]/div/div[1]/div[3]/div[2]/div[2]/div')
product1_summary_price = element.text[1:]
save_log(f'1st product in summary: {product1_summary_name} - $ {product1_summary_price}')
# 2nd product
element = driver.find_element(By.CSS_SELECTOR,'a#item_2_title_link')
product2_summary_name = element.text
element = driver.find_element(By.XPATH,'//*[@id="checkout_summary_container"]/div/div[1]/div[4]/div[2]/div[2]/div')
product2_summary_price = element.text[1:]
save_log(f'2nd product in cart: {product2_summary_name} - $ {product2_summary_price}')


#final check
element = driver.find_element(By.CSS_SELECTOR,'a#item_0_title_link')
product1_final = element.text
element = driver.find_element(By.XPATH,'//*[@id="checkout_summary_container"]/div/div[1]/div[3]/div[2]/div[2]/div')
product1_final_price = element.text[1:]
save_log(f'1st final product: {product1_final} - $ {product1_final_price}')

element = driver.find_element(By.CSS_SELECTOR,'a#item_2_title_link')
product2_final = element.text
element = driver.find_element(By.XPATH,'//*[@id="checkout_summary_container"]/div/div[1]/div[4]/div[2]/div[2]/div')
product2_final_price = element.text[1:]
# checking sum in cart and in final summary
final_sum = float(product1_final_price) + float(product2_final_price)

save_log(f'2nd final product: {product2_final} - $ {product2_final_price}. Total price without tax: $ '
    f'{final_sum}')

assert (float(product1_cart_price) + float(product2_cart_price)) == final_sum, save_log(
    f'FAIL. products sum in cart and in final are different')
save_log(f'OK. products sum in cart and in final are similar')

#last check with tax
element = driver.find_element(By.XPATH,'//*[@id="checkout_summary_container"]/div/div[2]/div[6]')
tax_value = element.text[6:]
final_sum_with_tax = final_sum + float(tax_value)
save_log(f'tax value: $ {tax_value} final sum with tax: $ {final_sum_with_tax}')

element = driver.find_element(By.XPATH,'//*[@id="checkout_summary_container"]/div/div[2]/div[7]')
final_screen_sum = element.text[8:]
save_log(f'final screen sum: $ {final_screen_sum}')

assert final_sum_with_tax == float(final_screen_sum), save_log(
    f'FAIL. final sum with tax are different')
save_log(f'OK. products final sum with tax are similar')
save_log(f'Test OK')

#finish
element = driver.find_element(By.CSS_SELECTOR,'button#finish')
element.click()