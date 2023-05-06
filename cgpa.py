import csv
from bs4 import BeautifulSoup
import requests

def get_regno(branch, start, end, dual=False):
    ids = []
    for i in range(start, end+1):
        if i < 10:
            regno = "19"+branch+"0100"+str(i)
        else:
            regno = "19"+branch+"010"+str(i)
        if(dual):
            regno = regno[:5] + "2" + regno[6:]
        ids.append(regno)
    return ids

def get_dates():
    dates = []
    years = [2002, 2001, 2000, 1999, 2003, 1998]
    for year in years:
        for month in range(1, 13):
            for day in range(1, 32):
                if month == 2 and day > 28:
                    break
                elif month in [4, 6, 9, 11] and day > 30:
                    break
                else:
                    date = str(year) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2)
                    dates.append(date)
    dates.append("2000-02-29")
    return dates

def get_results(branch, start, end, dual=False):
    login_url = "https://webapps.iitbbs.ac.in/Result/login.php"
    redirect_url = "https://webapps.iitbbs.ac.in/Result/Results_menu.php"
    result_url = "https://webapps.iitbbs.ac.in/Result/result.php"
    file_name = branch.lower()+".csv"
    if(dual):
        file_name = branch.lower()+"_dual.csv"

    ids = get_regno(branch, start, end, dual)
    for id in ids:
        dates = get_dates()
        for date in dates:
            data = {
                'regno': id,
                'dob': date,
                'submit': 'Submit'
            }
            r = requests.post(login_url, data=data)
            if r.url == redirect_url:
                with requests.session() as s:
                    s.post(login_url, data=data)
                    r = s.get(result_url)
                    soup = BeautifulSoup(r.text, 'html.parser')
                    name = soup.findAll('h1')[1].text[6:]
                    soup = str(soup)
                    index = soup.rfind("CGPA:")
                    cgpa = soup[index + 5: index + 9]
                    index = soup.rfind("SGPA:")
                    sgpa = soup[index + 5: index + 9]
                    print(id, date, cgpa)
                    with open(file_name, 'a', newline='') as csv_file:
                        csv_writer = csv.writer(csv_file)
                        csv_writer.writerow([id, name, date, sgpa, cgpa])
                    break
            else:
                print(id, date, "NOT FOUND")

def update_results(branch, dual=False):
    login_url = "https://webapps.iitbbs.ac.in/Result/login.php"
    result_url = "https://webapps.iitbbs.ac.in/Result/result.php"
    file_name = branch.lower()+".csv"
    if(dual):
        file_name = branch.lower()+"_dual.csv"
    
    with requests.session() as s:
        with open(file_name, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for row in csv_reader:
                regno = row[0]
                name = row[1]
                dob = row[2][1:]
                data = {
                    'regno': regno,
                    'dob': dob,
                    'submit': 'Submit'
                }
                r = s.post(login_url, data=data)
                r = s.get(result_url)
                soup = BeautifulSoup(r.text, 'html.parser')
                name = soup.findAll('h1')[1].text[6:]
                soup = str(soup)
                index = soup.rfind("CGPA:")
                cgpa = soup[index + 5: index + 9]
                index = soup.rfind("SGPA:")
                sgpa = soup[index + 5: index + 9]
                print(id, dob, cgpa)
                with open(file_name, 'a', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow([id, name, dob, sgpa, cgpa])

get_results("EE", 68, 68)
