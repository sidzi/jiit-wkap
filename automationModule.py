from bs4 import BeautifulSoup
from utils import excelWriter


def activate(html_page, **kwargs):
    if 'attendancePull' in kwargs:
        wb_name='AttendanceList'
        soup = BeautifulSoup(html_page, "html.parser")
        student_attendance_rows = soup.find(id="table-1").find("tbody").find_all("tr")
        i = 1
        for studentAttendanceRow in student_attendance_rows:
            student_data = studentAttendanceRow.text.splitlines()[1:]
            print student_data
            j = 1
            for data in student_data:
                excelWriter.write(workbook_name=wb_name, row=i, col=j, value=data)
                j += 1
            i += 1
