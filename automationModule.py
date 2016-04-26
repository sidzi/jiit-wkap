from bs4 import BeautifulSoup
from utils import excelWriter, excelReader

def activate(html_page, job, **kwargs):
    if 'pullAtt' in job:
        if 'fileNameID' in kwargs:
            wb_name = 'AttendanceList' + kwargs.get('fileNameID')
        else:
            wb_name = 'AttendanceListDefault'
        soup = BeautifulSoup(html_page, "html.parser")
        student_attendance_rows = soup.find(id="table-1").find("tbody").find_all("tr")
        excel_writer = excelWriter.ExcelWriter(wb_name)
        i = 1
        for studentAttendanceRow in student_attendance_rows:
            student_data = studentAttendanceRow.text.splitlines()[1:]
            j = 1
            for data in student_data:
                excel_writer.write(row=i, col=j, value=data)
                j += 1
            i += 1
            del student_data
        excel_writer.close()
        del student_attendance_rows
        return True
    elif 'checkAtt' in job:
        soup = BeautifulSoup(html_page, "html.parser")
        att_status = soup.find(id="table-1").find("tbody").find("tr").find_all("td")
        return att_status[1].text
    elif 'markAtt' in job:
        soup = BeautifulSoup(html_page, "html.parser")
        student_attendance_rows = soup.find(id="table-1").find("tbody").find_all("tr")
        student_data = excelReader.read("AttListDef.xls")
        for studentAttendanceRow in student_attendance_rows:
            for data in student_data:
                print data
        return False
