import sys
import time

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
    elif 'markAtt' in sys.argv:
        urls.append("https://webkiosk.jiit.ac.in/EmployeeFiles/AcademicInfo/NewDailyStudentAttendanceEntry1.jsp")
        jobs.append('markAtt')
    elif 'createAtt' in sys.argv:
        urls.append("https://webkiosk.jiit.ac.in/EmployeeFiles/AcademicInfo/NewDailyStudentAttendanceEntry1.jsp")
        jobs.append('createAtt')
    else:
        print "Enter a valid argument"
        exit(1)
else:
    print "Provide argument/s\n"
    exit(1)

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
        exit(1)
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
                if automationModule.activate(browser.html, job=jobs[i], fileNameID=subject_choice_selected):
                    easygui.msgbox(msg="Debar list created !!")
            i += 1

        elif jobs[i] is 'checkAtt':
            button = browser.find_by_value('Show')
            button.click()
            if browser.status_code == 200:
                easygui.msgbox(msg="You've been marked {0} for today !".format(
                    automationModule.activate(browser.html, job=jobs[i])))
            i += 1
        elif jobs[i] is 'markAtt':
            import datetime

            now = datetime.datetime.now()
            if now.month <= 6:
                sem = "EVE"
            else:
                sem = "ODD"
            exam_choices = BeautifulSoup(browser.html, "html.parser").find(id='Exam').find_all("option")
            exam_choices_list = list(exam_choice.attrs['value'] for exam_choice in exam_choices)
            exam_choice_selected = None
            for choice in exam_choices_list:
                if str(now.year) in choice:
                    if sem in choice:
                        exam_choice_selected = choice
            browser.find_by_id('Exam').first.select(exam_choice_selected)

            subject_choices = BeautifulSoup(browser.html, "html.parser").find(id='Subject').find_all("option")
            subject_choices_list = list(choice.attrs['value'] for choice in subject_choices)
            subject_choice_selected = easygui.choicebox(choices=subject_choices_list)
            browser.find_by_id('Subject').first.select(subject_choice_selected)
            try:
                student_data = automationModule.activate(browser.html, job=jobs[i], fileNameID=subject_choice_selected)
            except IOError:
                student_data = None
                easygui.msgbox('Please put the attendance sheet in the "AttendanceSheets" Folder!')
                exit(1)
            button = browser.find_by_value('Submit')
            button.click()

            checkbox = browser.find_by_id('SubSection1').first
            checkbox.check()

            browser.fill("timepicker1", easygui.enterbox("Enter Class Start Time:"))
            browser.fill("timepicker2", easygui.enterbox("Enter Class End Time:"))

            button = browser.find_by_value('Show/Refresh')
            button.click()

            if browser.status_code == 200:
                soup = BeautifulSoup(browser.html, "html.parser")
                student_attendance_rows = soup.find(id="table-1").find("tbody").find_all("tr")
                j = 1
                browser.find_by_id('allbox1').check()
                for student_attendance_row in student_attendance_rows:
                    try:
                        if student_data[student_attendance_row.contents[1].contents[0]] is True:
                            browser.find_by_id('Present' + str(j)).first.check()
                        else:
                            pass
                        j += 1
                    except IndexError:
                        pass
                        break
                # TODO final submit button click to be added only at Project Completion and final Delivery
                time.sleep(10)
            i += 1

        elif jobs[i] is 'createAtt':
            import datetime

            now = datetime.datetime.now()
            if now.month <= 6:
                sem = "EVE"
            else:
                sem = "ODD"
            exam_choices = BeautifulSoup(browser.html, "html.parser").find(id='Exam').find_all("option")
            exam_choices_list = list(exam_choice.attrs['value'] for exam_choice in exam_choices)
            exam_choice_selected = None
            for choice in exam_choices_list:
                if str(now.year) in choice:
                    if sem in choice:
                        exam_choice_selected = choice
            browser.find_by_id('Exam').first.select(exam_choice_selected)

            subject_choices = BeautifulSoup(browser.html, "html.parser").find(id='Subject').find_all("option")
            subject_choices_list = list(choice.attrs['value'] for choice in subject_choices)
            subject_choice_selected = easygui.choicebox(choices=subject_choices_list)
            browser.find_by_id('Subject').first.select(subject_choice_selected)

            button = browser.find_by_value('Submit')
            button.click()

            checkbox = browser.find_by_id('SubSection1').first
            checkbox.check()

            browser.fill("timepicker1", "09:00")
            browser.fill("timepicker2", "10:00")

            button = browser.find_by_value('Show/Refresh')
            button.click()

            if browser.status_code == 200:
                if automationModule.activate(browser.html, job=jobs[i], fileNameID=subject_choice_selected):
                    easygui.msgbox(msg="Attendance list created !!")

            i += 1

exit(0)
