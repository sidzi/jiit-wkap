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
    elif 'createAtt' in job:
        if 'fileNameID' in kwargs:
            wb_name = 'AttendanceInputList' + kwargs.get('fileNameID')
        else:
            wb_name = 'AttendanceInputListDefault'
        soup = BeautifulSoup(html_page, "html.parser")
        student_attendance_rows = soup.find(id="table-1").find("tbody").find_all("tr")
        excel_writer = excelWriter.ExcelWriter(wb_name)
        excel_writer.write(row=1, col=1, value="Enr. No.")
        excel_writer.write(row=1, col=2, value="Name")
        # excel_writer.write(row=1, col=2, value="Name") TODO Get Attendance Dates According to the timetable <#1>

        i = 2
        for studentAttendanceRow in student_attendance_rows:
            student_data = studentAttendanceRow.text.splitlines()[1:]
            j = 1
            # Preparations
            for data in student_data:
                if j >= 3:  # TODO Remove after <#1> is completed
                    break
                else:
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
        file_id = kwargs.get('fileNameID')
        try:
            student_data = excelReader.read("AttendanceSheets/AttendanceInputList" + str(file_id) + ".xlsx")
        except Exception:
            raise IOError
        return student_data
