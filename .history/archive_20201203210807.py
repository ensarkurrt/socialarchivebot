#coding: utf-8
from selenium.webdriver.common.by import By
from selenium import webdriver
import unittest
import time

def setup_module(module):
    WebKitFeatureStatusTest.driver = webdriver.Safari()

def teardown_module(module):
    WebKitFeatureStatusTest.driver.quit()

