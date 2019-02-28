import csv
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Frame, PageTemplate, NextPageTemplate
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from functools import partial
styles = getSampleStyleSheet()

ROOM_CAPACITY = None
ROOM_INDEX = None
ROOM_CAPACITY_INDEX = None
VACANCY_INDEX = None

EXAM_SCHEDULE = None
COURSE_CODE_INDEX = None
COURSE_NAME_INDEX = None
DATE_INDEX = None
SESSION_INDEX = None
ALLOTEMENT_INDEX = None
REGISTERED_STUDENTS_COUNT_INDEX = None
ROOMRANGE_INDEX = None
REMAINDER_STUDENT_INDEX = None
ROOMS_ALLOT_COUNT_INDEX = None

STUDENT = None
STUDENT_ID_INDEX = None
COURSE_ID_INDEX = None
ROOM_ALLOT_INDEX = None

ROOM_HEADERS , STUDENT_HEADERS, EXAM_HEADERS = [], [], []
ROOMS, STUDENTS, EXAMS, LABS = [], [], [], []
DATES, SESSIONS = [], []
SLOT_EXAM, EXAM_STUDENTS, EXAM_ROOMS = [], [], []
SEATING = []
ERROR = []

# #######################TESTING
# for l in ["BITSF110","MEF244","MFF244","CHEF242","MFF421","CHEF342"]:
# 	LABS.append(l)

for header in ["courseID", "courseName", "date", "session","roomsAlloted","noOfStudents","roomRange", "remainderStudentsCount","noOfRoomsAlloted"]:
	EXAM_HEADERS.append(header)

SEATING.append(["Course ID", "Course name", "Date", "Session", "Room", "Number", "Starting ID", "Ending ID"])

def masterFunction():

	with open(ROOM_CAPACITY, 'r') as room:
		roomReader = csv.reader(room)
		ROOM_HEADERS = next(roomReader)
		ROOM_HEADERS.append("vacancy")

		for row in roomReader:
			row[ROOM_CAPACITY_INDEX] = int(row[ROOM_CAPACITY_INDEX])
			row.append(row[ROOM_CAPACITY_INDEX])
			ROOMS.append(row)

	with open(STUDENT, 'r') as student:
		studentReader = csv.reader(student)
		STUDENT_HEADERS = next(studentReader)
		STUDENT_HEADERS.append("room")

		for row in studentReader:
			row.append("")
			row[COURSE_ID_INDEX] = row[COURSE_ID_INDEX].replace(" ","")
			STUDENTS.append(row)		

	with open(EXAM_SCHEDULE, 'r') as exam:
		examReader = csv.reader(exam)

		for row in examReader:
			row[COURSE_CODE_INDEX] = row[COURSE_CODE_INDEX].replace(" ","")
			if not row[DATE_INDEX] == "*":
				row[DATE_INDEX] = row[DATE_INDEX].replace(" ","")
				row[SESSION_INDEX] = row[SESSION_INDEX].replace(" ","")
				row[ALLOTEMENT_INDEX] = row[ALLOTEMENT_INDEX].replace(" ", "")
				row[REGISTERED_STUDENTS_COUNT_INDEX] = int(row[REGISTERED_STUDENTS_COUNT_INDEX].replace(",",""))
				row[ALLOTEMENT_INDEX] = row[ALLOTEMENT_INDEX].split(",")
				row.append([])
				row.append(row[REGISTERED_STUDENTS_COUNT_INDEX])
				row.append(sum(1 for r in row[ALLOTEMENT_INDEX]))
				EXAMS.append(row)
			else:
				LABS.append(row[COURSE_CODE_INDEX])
	EXAMS.sort(key = lambda x:x[DATE_INDEX])

	for e in EXAMS:
		if not e[DATE_INDEX] in DATES:
			DATES.append(e[DATE_INDEX])
		if not e[SESSION_INDEX] in SESSIONS:
			SESSIONS.append(e[SESSION_INDEX])

	def studentCount(courseId, room):
		count = sum(1 for student in STUDENTS if student[COURSE_ID_INDEX] == courseId and student[ROOM_ALLOT_INDEX] == room)
		return count

	def refresh():
		SLOT_EXAM.clear()
		for room in ROOMS:
			room[VACANCY_INDEX] = room[ROOM_CAPACITY_INDEX]

	def allotStudents(e,r,es,f,rr):
		for stu in es:
			if e[REGISTERED_STUDENTS_COUNT_INDEX]==0 or r[VACANCY_INDEX]==0:
				break
			if stu[COURSE_ID_INDEX] == e[COURSE_CODE_INDEX] and stu[ROOM_ALLOT_INDEX] == "":
				stu[ROOM_ALLOT_INDEX] = r[ROOM_INDEX]
				r[VACANCY_INDEX] -= 1
				e[REMAINDER_STUDENT_INDEX] -= 1

				if f == 0:
					startStudent = stu[STUDENT_ID_INDEX]
					f = 1

				if e[REMAINDER_STUDENT_INDEX] == 0 or r[VACANCY_INDEX] ==0:
					rr.append([e[COURSE_CODE_INDEX], r[ROOM_INDEX], startStudent, stu[STUDENT_ID_INDEX]])
					e[ROOMRANGE_INDEX].append(rr)
					break

	def roomOrderGenerator(exam, slotExams):
		ROOMSET, EXCLUSIVE, COMMON, EXCLUSIVE_SET, COMMON_SET = [], [], [], [], []
		for e in slotExams:
			if not e[COURSE_CODE_INDEX] == exam[COURSE_CODE_INDEX]:
				for r in e[ALLOTEMENT_INDEX]:
					if not r in ROOMSET:
						ROOMSET.append(r)
		
		for r in exam[ALLOTEMENT_INDEX]:
			if not r in ROOMSET:
				EXCLUSIVE.append(r)
			else:
				COMMON.append(r)
		for r in ROOMS:
			if r[ROOM_INDEX] in EXCLUSIVE:
				EXCLUSIVE_SET.append(r)
			elif r[ROOM_INDEX] in COMMON:
				COMMON_SET.append(r)

		EXCLUSIVE_SET.sort(key = lambda x:x[ROOM_INDEX])
		COMMON_SET.sort(key = lambda x:x[ROOM_INDEX])
		return EXCLUSIVE_SET + COMMON_SET

	def seating():
		for date in DATES:
			for session in SESSIONS:
				refresh()
				
				for exam in EXAMS:
					if exam[DATE_INDEX] == date and exam[SESSION_INDEX] == session:
						SLOT_EXAM.append(exam)
				SLOT_EXAM.sort(key = lambda x:x[ROOMS_ALLOT_COUNT_INDEX])

				for e in SLOT_EXAM:
					EXAM_STUDENTS.clear()
					# EXAM_ROOMS.clear()
					# e[ALLOTEMENT_INDEX] = sorted(e[ALLOTEMENT_INDEX])

					for student in STUDENTS:
						if student[COURSE_ID_INDEX] == e[COURSE_CODE_INDEX]:
							EXAM_STUDENTS.append(student)
					EXAM_STUDENTS.sort(key = lambda x:x[STUDENT_ID_INDEX])

					if e[COURSE_CODE_INDEX] == "BIOF111":
						for flag in EXAM_STUDENTS:
							print(flag)

					EXAM_ROOMS = roomOrderGenerator(e, SLOT_EXAM)
					# for r in ROOMS:
					# 	if r[ROOM_INDEX] in e[ALLOTEMENT_INDEX]:
					# 		EXAM_ROOMS.append(r)
					# EXAM_ROOMS.sort(key = lambda x:x[ROOM_INDEX])

					for r in EXAM_ROOMS:
						flag = 0
						roomRange = []
						if e[REMAINDER_STUDENT_INDEX] == 0:
							break
						if r[VACANCY_INDEX] == 0:
							continue
						if e[REGISTERED_STUDENTS_COUNT_INDEX]<=r[VACANCY_INDEX]:
							allotStudents(e,r,EXAM_STUDENTS,flag,roomRange)
							break
						else:
							allotStudents(e,r,EXAM_STUDENTS,flag,roomRange)
		
		EXAMS.sort(key = lambda x:x[COURSE_CODE_INDEX])

		for e in EXAMS:
			for rr in e[ROOMRANGE_INDEX]:
				if studentCount(e[COURSE_CODE_INDEX], rr[0][1]) == e[REGISTERED_STUDENTS_COUNT_INDEX]:
					rr[0][2] = "All students"
					rr[0][3] = "All students"
				SEATING.append([e[COURSE_CODE_INDEX], e[COURSE_NAME_INDEX], e[DATE_INDEX], e[SESSION_INDEX], rr[0][1], str(studentCount(e[COURSE_CODE_INDEX], rr[0][1])), rr[0][2], rr[0][3]])
		
		repeat = []
		for ex in SEATING:
			if ex[0] == "Course ID":
				continue
			if ex[0] in repeat:
				ex[0], ex[1], ex[2], ex[3] = "", "", "", ""
			else:
				repeat.append(ex[0])

	def pdfCreate():
		doc = SimpleDocTemplate(("seating-arrangement.pdf"), pagesize=A4)
		t = Table(SEATING_DICTIONARY, repeatRows= 1, 
			style= [('GRID',(0,0),(-1,-1),1,colors.black),
					('FONTSIZE',(0,0),(-1,-1),6)])
		elements = []
		elements.append(t)
		doc.build(elements)
		print("The file is created as sitting-arrangement.pdf.")

	def csvCreate():
		file = open("seating.csv", "w")
		with file:
			writer = csv.writer(file)
			writer.writerows(SEATING)

	def errorLog():
		for stu in STUDENTS:
			if stu[ROOM_ALLOT_INDEX] == "" and not stu[COURSE_ID_INDEX] in LABS:
				ERROR.append(stu)
		ERROR.sort(key = lambda x:x[COURSE_ID_INDEX])

		file1 = open("error.csv", "w")
		with file1:
			writer = csv.writer(file1)
			writer.writerows(ERROR)

	def generate():
		seating()
		csvCreate()
		errorLog()

	generate()

###################################################################################

#CSV TO PDF CONVERTER
SEATING_CSV = None	
SEATING_DICTIONARY= []
TEST_TYPE = None
SEATING_DICTIONARY.append(["Course ID", "Course name", "Date", "Session", "Room", "Number", "Starting ID", "Ending ID"])

def convert():
	with open(SEATING_CSV, 'r') as s:
		seatingReader = csv.reader(s)
		SEATING_HEADERS = next(seatingReader)

		for row in seatingReader:
			if not row == []: 
				SEATING_DICTIONARY.append(row)

	doc = SimpleDocTemplate(("seating-arrangement.pdf"), pagesize=letter)
	t = Table(SEATING_DICTIONARY, repeatRows= 1, 
		style= [('GRID',(0,0),(-1,-1),1,colors.black),
				('FONTSIZE',(0,0),(-1,-1),6)])

	elements = []
	heading1 = "BIRLA INSTITUTE OF TECHNOLOGY AND SCIENCE, PILANI"
	heading2 = "TIMETABLE DIVISION"
	heading3 = "FIRST SEMESTER 2018-2019"

	if TEST_TYPE == "Compre":
		heading4 = "COMPREHENSIVE EXAMINATION SEATING ARRANGEMENT"
	elif TEST_TYPE == "Midsem":
		heading4 = "MID SEMESTER EXAMINATION SEATING ARRANGEMENT"

	head1text = '<para align = "centre"><font size = 15><strong>%s</strong></font></para>' % heading1
	head2text = '<para align = "centre"><font size = 14><strong>%s</strong></font></para>' % heading2
	head3text = '<para align = "centre"><font size = 12><strong>%s</strong></font></para>' % heading3
	head4text = '<para align = "centre"><font size = 12><strong>%s</strong></font></para>' % heading4
    
	elements.append(Paragraph(head1text, styles["Normal"])) 
	elements.append(Spacer(1, 12))

	elements.append(Paragraph(head2text, styles["Normal"])) 
	elements.append(Spacer(1, 12))

	elements.append(Paragraph(head3text, styles["Normal"])) 
	elements.append(Spacer(1, 12))

	elements.append(Paragraph(head4text, styles["Normal"])) 
	elements.append(Spacer(1, 12))

	elements.append(t)
	doc.build(elements)
	print("The file is created as sitting-arrangement.pdf.")

