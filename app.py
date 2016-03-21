from splinter import Browser
from utils import fileReader, fileWriter
import easygui
import automationModule
from bs4 import BeautifulSoup

(member_code, password) = fileReader.read()
if member_code is None or member_code is '':
    member_code = easygui.enterbox("Enter Member Code:")
    password = easygui.passwordbox()
    fileWriter.write(member_code, password)

with Browser() as browser:
    url = "https://webkiosk.jiit.ac.in/"
    browser.visit(url)
    browser.find_by_id('UserType').first.select('E')
    browser.fill('MemberCode', member_code)
    browser.fill('Password', password)
    button = browser.find_by_name('BTNSubmit')
    button.click()

    if browser.status_code == 200 and "Wrong Member" not in browser.html:
        browser.visit("https://webkiosk.jiit.ac.in/EmployeeFiles/AcademicInfo/ViewAttendanceSummary11.jsp?SrcType=I")

        exam_choices = BeautifulSoup(browser.html, "html.parser").find(id='Exam').find_all("option")
        exam_choices_list = list(exam_choice.attrs['value'] for exam_choice in exam_choices)
        exam_choice_selected = easygui.choicebox(choices=exam_choices_list)
        browser.find_by_id('Exam').first.select(exam_choice_selected)

        subject_choices = BeautifulSoup(browser.html, "html.parser").find(id='Subject').find_all("option")
        subject_choices_list = list(choice.attrs['value'] for choice in subject_choices)
        subject_choice_selected = easygui.choicebox(choices=subject_choices_list)
        browser.find_by_id('Subject').first.select(subject_choice_selected)

        button = browser.find_by_value('Show/Refresh')
        button.click()

        if browser.status_code == 200:
            automationModule.activate(browser.html, attendancePull=True, fileNameID=subject_choice_selected)
    else:
        print("Error!?!?!?")
