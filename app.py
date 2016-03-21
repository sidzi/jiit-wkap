from easygui import passwordbox, enterbox
from splinter import Browser
from utils import fileReader, fileWriter
import automationModule

(member_code, password) = fileReader.read()
if member_code is None or member_code is '':
    member_code = enterbox("Enter Member Code:")
    password = passwordbox()
    fileWriter.write(member_code, password)

with Browser() as browser:
    # Visit URL
    url = "https://webkiosk.jiit.ac.in/"
    browser.visit(url)
    browser.find_by_id('UserType').first.select('E')
    browser.fill('MemberCode', member_code)
    browser.fill('Password', password)

    # Find and click the 'search' button
    button = browser.find_by_name('BTNSubmit')
    # Interact with elements
    button.click()
    if browser.status_code == 200 and not "Wrong Member" in browser.html:
        browser.visit("https://webkiosk.jiit.ac.in/EmployeeFiles/AcademicInfo/ViewAttendanceSummary11.jsp?SrcType=I")
        browser.find_by_id('Exam').first.select('2016EVESEM')
        browser.find_by_id('Subject').first.select('140076')
        button = browser.find_by_value('Show/Refresh')
        button.click()
        if browser.status_code == 200:
            automationModule.activate(browser.html, attendancePull=True)
    else:
        print("Error!?!?!?")
