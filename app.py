import sys

import automationModule
import easygui
from bs4 import BeautifulSoup
from splinter import Browser
from utils import fileReader, fileWriter

urls = list()
jobs = list()
if len(sys.argv) > 1:
    if 'checkAtt' in sys.argv:
        urls.append("https://webkiosk.jiit.ac.in/EmployeeFiles/PersonalInfo/SelfAttendanceDetail.jsp")
        jobs.append('checkAtt')
    elif 'pullAtt' in sys.argv:
        urls.append("https://webkiosk.jiit.ac.in/EmployeeFiles/AcademicInfo/ViewAttendanceSummary11.jsp?SrcType=I")
        jobs.append('pullAtt')
    else:
        print "Enter a valid argument"
        exit()
else:
    print "Provide argument/s\n"
    exit()

(member_code, password) = fileReader.read()
if member_code is None or member_code is '':
    member_code = easygui.enterbox("Enter Member Code:")
    password = easygui.passwordbox()
    fileWriter.write(member_code, password)

with Browser() as browser:
    browser.visit("https://webkiosk.jiit.ac.in/")
    browser.find_by_id('UserType').first.select('E')
    browser.fill('MemberCode', member_code)
    browser.fill('Password', password)
    button = browser.find_by_name('BTNSubmit')
    button.click()
    if "Wrong Member" in browser.html:
        print("Wrong Username/Password")
        exit()
    i = 0
    while i < len(jobs):
        browser.visit(urls[i])
        if jobs[i] is 'pullAtt':
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
                automationModule.activate(browser.html, job=jobs[i], fileNameID=subject_choice_selected)
            i += 1

        if jobs[i] is 'checkAtt':
            button = browser.find_by_value('Show')
            button.click()
            if browser.status_code == 200:
                easygui.msgbox(msg="You've been marked {0} for today !".format(
                    automationModule.activate(browser.html, job=jobs[i])))
            i += 1
