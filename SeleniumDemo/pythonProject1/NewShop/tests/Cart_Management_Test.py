import time

import pytest
from package import cart_mangement as cm

price_conflict_error = "Giá tiền ước tính mâu thuẫn với tổng tiền trong giỏ hàng"

@pytest.fixture
def setup_and_teardown():
    # Setup code
    cm.get_homepage()
    yield
    # Teardown code
    cm.quit_driver()


def test_add_1_items_to_cart(setup_and_teardown):
    assert True == cm.add_items_to_cart(1), price_conflict_error

def test_add_many_items_to_cart(setup_and_teardown):
    assert True == cm.add_items_to_cart(5), price_conflict_error

def test_increase_item_quantity(setup_and_teardown):
    cm.increase_first_item_quantity(3)

def test_increase_decrease_item_quantity(setup_and_teardown):
    cm.decrease_first_item_quantity(5)

def test_delete_1_item(setup_and_teardown):
    cm.delete_first_item()

def test_saving_cart_satus(setup_and_teardown):
    cm.login('fakemail@gmail.com','123456')
    cm.add_items_to_cart(5)
    cm.driver.get("https://newshop.vn/")
    time.sleep(2)
    cm.logout()
    cm.login('fakemail@gmail.com','123456')
    cm.wait_until_clickable_xpath("//a[contains(@class,'get-cart-box')]")

