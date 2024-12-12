import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class TestGoingtocatalogsettingparameters:
    def setup_method(self, method):
        # Инициализация браузера
        self.driver = webdriver.Firefox()
        self.vars = {}

    def teardown_method(self, method):
        # Закрытие браузера
        self.driver.quit()

    def test_goingtocatalogsettingparameters(self):
        # Открытие сайта
        self.driver.get("https://plati.market/")
        self.driver.set_window_size(550, 692)

        # Клик по элементу на странице
        self.driver.find_element(By.CSS_SELECTOR, ".adds_product_images > a:nth-child(1) > img").click()

        # Работа с выпадающим списком "Валюта"
        self.driver.find_element(By.CSS_SELECTOR, "#GoodsBlock_3566 .goods-table select").click()
        dropdown = self.driver.find_element(By.CSS_SELECTOR, "#GoodsBlock_3566 .goods-table select")
        dropdown.find_element(By.XPATH, "//option[. = 'USD']").click()

        # Работа с выпадающим списком "Фильтр по рейтингу"
        self.driver.find_element(By.CSS_SELECTOR, "#GoodsBlock_3566 > .table_header select").click()
        dropdown = self.driver.find_element(By.CSS_SELECTOR, "#GoodsBlock_3566 > .table_header select")
        dropdown.find_element(By.XPATH, "//option[. = '▼ рейтинг продавца']").click()

        # Наведение на элемент
        element = self.driver.find_element(By.CSS_SELECTOR, "#GoodsBlock_3566 .product-title span")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

        # Клик по элементу
        self.driver.find_element(By.CSS_SELECTOR, "#GoodsBlock_3566 .product-title-marked").click()

        # Закрытие браузера
        self.driver.close()
