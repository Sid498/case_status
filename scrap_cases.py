from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import requests as re
import time
import csv



PATH = r"chromedriver.exe"
options = Options()
options.headless = True
driver = webdriver.Chrome(executable_path=PATH, options=options)


def scrap_data(csv_path, from_year):
    with open(csv_path, 'w', newline='') as fp:
        datawriter = csv.writer(fp)
        datawriter.writerow(["Diary No.",
                             "Case No.",
                             "Present/Last Listed On",
                             "Status/Stage",
                             "Disp.Type",
                             "Category",
                             "Act",
                             "Petitioner(s)",
                             "Respondent(s)",
                             "Pet. Advocate(s)",
                             "Resp. Advocate(s)",
                             "U/Section"])

    for year in range(from_year, 2001, -1):
        for diary_number in range(1, 100):
        	print("Diary : {} Yeat: {}".format(diary_number, year))
        	driver.get("https://main.sci.gov.in/case-status")
        	time.sleep(3)
        	text = driver.find_element_by_id("ansCaptcha").send_keys(driver.find_element_by_id("cap").text.strip())
        	text = driver.find_element_by_id("CaseDiaryNumber").send_keys(str(diary_number))
        	driver.find_element_by_xpath("//select[@name='CaseDiaryYear']/option[text()=" + str(year) + "]").click()
        	driver.find_element_by_id("getCaseDiary").click()
        	time.sleep(3)
        	data = driver.find_element_by_class_name("container_cs")
        	td = data.find_elements_by_tag_name("td")
        	table_data = []
        	for i in range(1, 21, 2):
        		table_data.append(td[i].text)
        	with open(csv_path, 'a', newline='') as csvfile:
        		file_writer = csv.writer(csvfile)
        		file_writer.writerow(table_data)

    print('Finished')


scrap_data(csv_path='case_assignment.csv', from_year=2020)
