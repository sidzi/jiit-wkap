from splinter import Browser
from easygui import passwordbox, enterbox
from fileUtils import reader

(memcode, passcode) = reader.read()
if memcode is None:
    memcode = enterbox("Enter Member Code:")
    passcode = passwordbox()
    from fileUtils import writer
    writer.write(memcode, passcode)

with Browser() as browser:
    # Visit URL
    url = "https://webkiosk.jiit.ac.in/"
    browser.visit(url)
    browser.find_by_id('UserType').first.select('E')
    browser.fill('MemberCode', memcode)
    browser.fill('Password', passcode)

    # Find and click the 'search' button
    button = browser.find_by_name('BTNSubmit')
    # Interact with elements
    button.click()
    # if 1:
    # browser.visit("https://webkiosk.jiit.ac.in/StudentFiles/Exam/StudCGPAReport.jsp")
    #     bsParseHtml = BeautifulSoup(browser.html, "html.parser")
    #     gpaTable = bsParseHtml.find(id='table-1')
    #     i=1
    #     for gpaRow in gpaTable.find_all('tr'):
    #         for a in gpaRow.find_all('a', href=True):
    #             writer.write(workbook_name='testData',row=i,col=2,value=search('SGP=([0-9][.][0-9])',str(a['href'])).group(1))
    #             writer.write(workbook_name='testData',row=i,col=3,value=search('CGP=([0-9][.][0-9])',str(a['href'])).group(1))
    #             i+=1
    # else:
    #     print("How the hell ????")
