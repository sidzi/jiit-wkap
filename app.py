from splinter import Browser
from easygui import passwordbox
from bs4 import BeautifulSoup
from re import search

from excelUtils import writer

passwd = passwordbox("Enter Passsword : ")

if not passwd:
    exit()
with Browser() as browser:
    # Visit URL
    url = "https://webkiosk.jiit.ac.in/"
    browser.visit(url)
    # browser.find_by_id('UserType').first.select('E')
    browser.fill('MemberCode', '12103417')
    browser.fill('DATE1', '18/07/1993')
    browser.fill('Password', passwd)

    # Find and click the 'search' button
    button = browser.find_by_name('BTNSubmit')
    # Interact with elements
    button.click()
    if 1:
        browser.visit("https://webkiosk.jiit.ac.in/StudentFiles/Exam/StudCGPAReport.jsp")
        bsParseHtml = BeautifulSoup(browser.html, "html.parser")
        gpaTable = bsParseHtml.find(id='table-1')
        i=1
        for gpaRow in gpaTable.find_all('tr'):
            for a in gpaRow.find_all('a', href=True):
                writer.write(workbook_name='testData',row=i,col=2,value=search('SGP=([0-9][.][0-9])',str(a['href'])).group(1))
                writer.write(workbook_name='testData',row=i,col=3,value=search('CGP=([0-9][.][0-9])',str(a['href'])).group(1))
                i+=1
    else:
        print("How the hell ????")