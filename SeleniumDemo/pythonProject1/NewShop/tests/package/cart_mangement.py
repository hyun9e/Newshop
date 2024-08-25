import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# For chrome config: disable notification and maximize window
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
# For hover function
from selenium.webdriver.common.action_chains import ActionChains
# For login exceptions
from selenium.common.exceptions import NoSuchElementException


option = Options()
option.add_argument("--disable-notifications")
option.add_argument("start-maximized")

# Initiate Chrome WebDriver (Open Chrome)
driver = webdriver.Chrome(options=option)
# Define Impliticity wait time
wait = WebDriverWait(driver, 10)
# For Hovering Function
actions = ActionChains(driver)


# Initialize WebDriver if needed, rediredt to homepage_url

# Find an element by XPATH
def find_by_xpath(element_path):
    return driver.find_element(By.XPATH, element_path)


# Find an element by XPATH and Click it
def find_and_click_by_xpath(element_path):
    find_by_xpath(element_path).click()


# Hover cursor to the element by XPATH
def hover_by_xpath(element_path):
    elem = actions.move_to_element(find_by_xpath(element_path))
    elem.perform()


# Wait for an element to be clickable
def wait_until_clickable_xpath(element_path):
    WebDriverWait(driver, 10).until(ec.element_to_be_clickable(
        (By.XPATH, element_path))).click()


# Wait for the element presence
def wait_for_presence_xpath(element_path):
    return WebDriverWait(driver, 10).until(ec.presence_of_element_located(
        (By.XPATH, element_path)))


# Return price_text as an integer
def sanitize_price(element_xpath_or_price_text):
    price_text = element_xpath_or_price_text
    # If input is element_xpath, convert to price_text
    if not element_xpath_or_price_text[0].isdigit():
        price_text = find_by_xpath(element_xpath_or_price_text).text
    # Remove 'đ' and '.' in price_text (ex: 67.500đ)
    cleaned_text = price_text.replace('đ', '').replace('.', '')
    return int(cleaned_text)


# Compare expected total price and Cart actual total price
def compare_expected_and_actual_price(expected_total_price):
    cart_total_price = driver.find_element(By.CLASS_NAME, "cart-total").text
    return expected_total_price == sanitize_price(cart_total_price)


# Add n items to cart (Set n to blank or 0 to add a random number of items)
def add_items_to_cart(n):
    total_price_expected = 0
    # Sách Văn Học Category
    find_and_click_by_xpath("//a[@id='menu-item-95']")


    # Add a random number of items
    if n==0 or n=='':
        number_of_items_to_add = random.randint(1, 10)
    else:
        if n > 0:
            number_of_items_to_add = n
            print("Đang thêm %d sản phẩm (có thể trùng) vào giỏ hàng!" % number_of_items_to_add)
        else:
            print("Invalid number of items value!")
            exit()
    # Add n item(s) to the cart
    for i in range(1,number_of_items_to_add+1):
        # 1.1 Randomly add an item with position X from 1 to 24
        # counting from left to right, up to down
        # Maximum items displayed per category page: 24
        position = random.randint(1, 24)

        # 1.2 Add item to cart, Add price to total_price_expected
        item_xpath = f"(//span[@class='button-buy-now '])[{position}]"
        item_sale_price = f"(//div[@class='price-group']//span[@class='price sale-price'])[{position}]"

        hover_by_xpath(item_xpath)
        total_price_expected += sanitize_price(item_sale_price)
        find_and_click_by_xpath(item_xpath)

        # 1.3 Close the Cart pop-up screen and continue the loop
        continue_shopping_button = "//span[contains(text(),'Tiếp tục mua hàng')]"
        wait_until_clickable_xpath(continue_shopping_button)

    # 2. Cart report
    # 2.1 Open cart
    cart_button_xpath = "//a[contains(@class,'get-cart-box')]"
    wait_until_clickable_xpath(cart_button_xpath)

    # 2.2 Read cart details
    print(find_by_xpath("//div[contains(text(),'Giỏ hàng của bạn')]").get_attribute("innerText"))
    cart_total_price = driver.find_element(By.CLASS_NAME, "cart-total").text
    print("Tạm tính:", cart_total_price)
    # print('total_price_expected:',total_price_expected)
    # print('cart_total_price: ',sanitize_price(cart_total_price))
    return total_price_expected == sanitize_price(cart_total_price)


# def increase_first_items_quantity():
#     # Get the total price from the cart
#     total_price =  add_items_to_cart(1)
#     # Increse the quantity of item and Add
#     wait_for_presence_xpath("//td[@class='item-price']//span[@class='price sale-price'][1]")
#     first_item_price = sanitize_price("//td[@class='item-price']//span[@class='price sale-price'][1]")
#     find_and_click_by_xpath("(//td[@class='item-quantity']//button[contains(text(), '+')])[1]")
#     total_price += first_item_price
#     cart_total_price = driver.find_element(By.CLASS_NAME, "cart-total").text
#     time.sleep(2)
#     return total_price == sanitize_price(cart_total_price)
def increase_first_item_quantity(n):
    add_items_to_cart(1)
    for i in range(n):
        wait_until_clickable_xpath("(//td[@class='item-quantity']//button[contains(text(), '+')])[1]")
        time.sleep(1)

def decrease_first_item_quantity(n):
    increase_first_item_quantity(n*2-1)
    for i in range(n):
        wait_until_clickable_xpath("(//td[@class='item-quantity']//button[contains(text(), '-')])[1]")
        time.sleep(1)


def delete_first_item():
    add_items_to_cart(3)
    for i in range(3):
        first_item_delete_button = "(//a[@class='event-remove-item'])[1]"
        wait_until_clickable_xpath(first_item_delete_button)
        time.sleep(1)


def login(username, password):
    print(f'Tài khoản: {username} \nMật khẩu: {password}')
    wait.until(ec.element_to_be_clickable((By.LINK_TEXT, "Đăng nhập"))).click()

    login_username_field_xpath = "(//input[@name='email'])[2]"
    login_username_field = wait.until(ec.visibility_of_element_located(
        (By.XPATH, login_username_field_xpath)))
    login_username_field.clear()
    login_username_field.send_keys(username)
    print("Đã nhập tk")

    login_password_field_xpath = "(//input[@name='password'])[1]"
    login_password_field = find_by_xpath(login_password_field_xpath)
    login_password_field.clear()
    login_password_field.send_keys(password)
    print("Đã nhập mk")
    login_password_field.send_keys(Keys.ENTER)

    if is_login_successful():
        print("Đăng Nhập thành công!")
        return True
    else:
        print('Đăng nhập thất bại, sai tài khoản/mật khẩu!')


def is_login_successful():
    try:
        # wait.until(ec.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Đăng xuất")))
        driver.find_element(By.PARTIAL_LINK_TEXT, "Đăng xuất")
        return True
    except NoSuchElementException:
        return False


# Log out
def logout():
    if is_login_successful():
        driver.find_element(By.LINK_TEXT, "Đăng xuất").click()
    print("Đăng Xuất thành công!")


def get_homepage():
    global driver
    if driver is None or not driver.session_id:
        driver = webdriver.Chrome(options=option)
    homepage_url = "https://newshop.vn/"
    driver.get(homepage_url)


# Quit driver. Set driver to None after quitting to ensure reinitialization
def quit_driver():
    time.sleep(2)
    global driver
    if driver is not None:
        driver.quit()
        driver = None




def main():
    # Open Newshop homepage
    get_homepage()
    add_items_to_cart(2)
    quit_driver()


if __name__ == "__main__":
    main()
