# This program scraps data from job postings on the website workinstartups.com and appends it to an excel worksheet.

import os
from datetime import datetime, timedelta
from selenium import webdriver
from app import web_scraper
from app import excel

URL = "https://workinstartups.com/job-board/jobs-in/london"
soup = web_scraper.soup_creator(URL, max_retry=1, sleep_time=0)

driver = webdriver.Chrome('./chromedriver')
driver.get(URL)
driver.find_element_by_link_text('Close').click()

current_date = datetime.today()
date_fortnight_ago = current_date - timedelta(weeks=2)
last_recent_date = date_fortnight_ago.replace(hour=0, minute=0, second=0, microsecond=0)  # default to midnight

job_list, hyperlink_list, company_link_list = [], [], []
job_list, hyperlink_list, company_link_list = web_scraper.search_for_jobs(soup, last_recent_date, driver)
driver.close()

workbook, worksheet = excel.init_workbook(worksheet_title="Job Openings")
table_headers = ("Job Openings", "Company", "Job Type", "Date Posted", "Deadline", "Salary Range")
excel.setup_worksheet(worksheet, job_list, hyperlink_list, company_link_list, table_headers)
file_path = os.path.abspath("main.py").rstrip('/app/main.py') + '//Workbooks' + "//Job_Openings.xlsx"
excel.save_workbook(workbook, file_path)
