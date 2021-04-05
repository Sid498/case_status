import requests
from bs4 import BeautifulSoup
import time
import csv

with open('cases_assignment_with_bs.csv', 'w', newline='') as csvfile:
    datawriter = csv.writer(csvfile)
    
    datawriter.writerow(["Diary No.",
                         "Case No.",
                         "Present/Last Listed On",
                         "Status/Stage",
                         "Category",
                         "Act",
                         "Petitioner(s)",
                         "Respondent(s)",
                         "Pet. Advocate(s)",
                         "Resp. Advocate(s)",
                         "U/Section"])
    

for year in range(2020,2019,-1):
    for diary_number in range(1,10):
        print("Diary: {} Year: {}".format(diary_number, year))
        with requests.session() as case_session:

            captcha_url="https://main.sci.gov.in/php/captcha_num.php"
            headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
            }
            r=case_session.get(captcha_url,headers=headers)
            captcha = BeautifulSoup(r.content , 'html.parser').text.strip()


            form_data={
                "d_no": diary_number,
                "d_yr": year,
                "ansCaptcha": str(captcha)
                }
            headers={
            "Referer": "https://main.sci.gov.in/case-status",  
        }

            try:
                url="https://main.sci.gov.in/php/case_status/case_status_process.php"
                r=case_session.post(url,headers=headers,data=form_data)
                soup = BeautifulSoup(r.content, 'html.parser')
                tds = soup.find('table').findAll("td")
                table_data=[]
                for i in range(1,21,2):
                    table_data.append(tds[i].text)
                with open('cases_assignment_with_bs.csv', 'a', newline='') as csvfile:
                    file_writer = csv.writer(csvfile)
                    file_writer.writerow(table_data)
                time.sleep(2)
                case_session.close()
                time.sleep(2)
            except:
                continue