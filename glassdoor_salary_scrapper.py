import json
import requests
from bs4 import BeautifulSoup

def scrapeSalaryData(url):
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    basePay = soup.find('div', {'data-test': "base-pay"})
    if not basePay:
        basePay = soup.find('span', {"data-test": "pay-period-MONTHLY-label"})
    totalPay = soup.find('div', {'data-test': "total-pay"})
    if not totalPay:
        totalPay = soup.find('div', {"data-test": "pay-period-label"})
    additionalPay = soup.find('div', {'data-test': "additional-pay-breakdown-all"})
    
    # Check if the list returned by find_all has at least 2 elements before accessing index 1
    payPeriodMonthlyLabels = soup.find_all('span', {"data-test": "pay-period-MONTHLY-label"})
    if len(payPeriodMonthlyLabels) >= 2:
        additionalPay = payPeriodMonthlyLabels[1]
    
    data = {
        "title": soup.find('title').text.split('Salaries')[0].strip(),
        "total_pay": totalPay.text.strip(),
        "base_pay": basePay.text.strip().split('Base')[0],
        "additional_pay": additionalPay.text.strip().split('All')[0],
    }
    return data

def main():
    url = 'https://www.glassdoor.com/Salary/Motorola-Solutions-Software-Engineer-Salaries-E427189_D_KO19,36.htm'
    data = scrapeSalaryData(url)
    print(data)
    # Store the data in a JSON file
    with open('salary_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == '__main__':
    main()
