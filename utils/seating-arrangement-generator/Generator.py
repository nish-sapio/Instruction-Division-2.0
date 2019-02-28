from tkinter import *
from tkinter import ttk, filedialog
import seating
root = Tk()
exam = StringVar()

root.title("SEATING ARRANGEMENT")

def RoomPathBrowseFunction():
	filename = filedialog.askopenfilename()
	RoomPath.config(text=filename)

def StuPathBrowseFunction():
	filename = filedialog.askopenfilename()
	StuPath.config(text=filename)

def ExamPathBrowseFunction():
	filename = filedialog.askopenfilename()
	ExamPath.config(text=filename)

def csvPathBrowseFunction():
	filename = filedialog.askopenfilename()
	csvPath.config(text=filename)

def UPLOAD():
	seating.ROOM_CAPACITY = RoomPath["text"]
	seating.ROOM_INDEX = int(RoomNumberIndex.get())
	seating.ROOM_CAPACITY_INDEX = int(RoomCapacityIndex.get())
	seating.VACANCY_INDEX = seating.ROOM_CAPACITY_INDEX+1

	seating.EXAM_SCHEDULE = ExamPath["text"]
	seating.COURSE_CODE_INDEX = int(CourseId_2_Index.get())
	seating.COURSE_NAME_INDEX = int(CourseNameIndex.get())
	seating.DATE_INDEX = int(DateIndex.get())
	seating.SESSION_INDEX = int(SessionIndex.get())
	seating.ALLOTEMENT_INDEX = int(AllotmentIndex.get())
	seating.REGISTERED_STUDENTS_COUNT_INDEX = int(StrengthIndex.get())
	seating.ROOMRANGE_INDEX = seating.REGISTERED_STUDENTS_COUNT_INDEX+1
	seating.REMAINDER_STUDENT_INDEX = seating.REGISTERED_STUDENTS_COUNT_INDEX+2
	seating.ROOMS_ALLOT_COUNT_INDEX = seating.REGISTERED_STUDENTS_COUNT_INDEX+3

	seating.STUDENT = StuPath["text"]
	seating.STUDENT_ID_INDEX = int(StuIDIndex.get())
	seating.COURSE_ID_INDEX = int(CourseIDIndex.get())
	seating.ROOM_ALLOT_INDEX = seating.COURSE_ID_INDEX+1

	uploadStatus.config(text="UPLOADED")

def GENERATE_CSV():
	seating.masterFunction()
	generateStatus.config(text="GENERATED")

def UPLOAD_CSV():
	seating.SEATING_CSV = csvPath['text']
	print(exam_type.get())
	seating.TEST_TYPE = exam_type.get()
	uploadCSVStatus.config(text="UPLOADED")

def CONVERT_CSV():
	seating.convert()
	convertStatus.config(text="CONVERTED")


n = ttk.Notebook(root)
generate = ttk.Frame(n)
convert = ttk.Frame(n)
n.add(generate, text="Generator")
n.add(convert, text = "Converter")


HeadFrame = ttk.Frame(generate, height=30 , width=600, borderwidth=2)
HeadFrame.grid(row=0, sticky="n")
generate.rowconfigure(0,weight=1)
ttk.Label(HeadFrame, text="SEATING ARRANGEMENT").grid(row=0, sticky="e")
ttk.Frame(generate, height=5, width=400).grid(row=1)

exam_type = StringVar()
choice = ttk.Labelframe(convert,text="TEST TYPE", height=30, width =600)
choice.grid(row=0, sticky="we")
r1 = ttk.Radiobutton(choice,text="Compre",variable=exam_type,value="Compre")
r1.grid(row=0)
ttk.Frame(choice, height=20, width=250).grid(row=0,column=1)
r2 = ttk.Radiobutton(choice,text="Midsem",variable=exam_type,value="Midsem")
r2.grid(row=0,column=2,sticky="e")

RoomForm=ttk.Labelframe(generate,text="ROOM DATA",width=800)
RoomForm.grid(row=3,sticky="nswe")
ttk.Label(RoomForm,text="File Path").grid(row=1,column=0,padx=12)
RoomPath = ttk.Label(RoomForm)
RoomPathBrowseButton = ttk.Button(RoomForm, text="Browse",command=RoomPathBrowseFunction).grid(row=1,column=1)
RoomPath.grid(row=1,column=2)
ttk.Label(RoomForm,text="Room Number Index").grid(row=2,column=0,padx=12)
ttk.Label(RoomForm,text="Exam Capacity Index").grid(row=3,column=0,padx=12)
RoomNumberIndex = ttk.Entry(RoomForm)
RoomNumberIndex.grid(row=2,column=1)
RoomCapacityIndex = ttk.Entry(RoomForm)
RoomCapacityIndex.grid(row=3,column=1)
for child in RoomForm.winfo_children(): child.grid_configure(padx=7, pady=5)


StuForm=ttk.Labelframe(generate,text="STUDENT DATA",width=800)
StuForm.grid(row=4,sticky="nswe")
ttk.Label(StuForm,text="File Path").grid(row=1,column=0,padx=15)
StuPathBrowseButton = ttk.Button(StuForm, text="Browse",command=StuPathBrowseFunction).grid(row=1,column=1)
StuPath = ttk.Label(StuForm)
StuPath.grid(row=1,column=2)
ttk.Label(StuForm,text="Student ID Index").grid(row=2,column=0,padx=10)
ttk.Label(StuForm,text="Course ID Index").grid(row=3,column=0,padx=10)
StuIDIndex = ttk.Entry(StuForm)
StuIDIndex.grid(row=2,column=1)
CourseIDIndex = ttk.Entry(StuForm)
CourseIDIndex.grid(row=3,column=1)
for child in StuForm.winfo_children(): child.grid_configure(padx=16, pady=5)


ExamForm=ttk.Labelframe(generate,text="EXAM DATA",width=800)
ExamForm.grid(row=5,sticky="nswe")
ttk.Label(ExamForm,text="File Path").grid(row=1,column=0,padx=10)
ExamPathBrowseButton = ttk.Button(ExamForm, text="Browse",command=ExamPathBrowseFunction).grid(row=1,column=1)
ExamPath = ttk.Label(ExamForm)
ExamPath.grid(row=1,column=2)
ttk.Label(ExamForm,text="Course ID Index").grid(row=2,column=0,padx=10)
ttk.Label(ExamForm,text="Course Name Index").grid(row=3,column=0,padx=10)
ttk.Label(ExamForm,text="Date Index").grid(row=4,column=0,padx=10)
ttk.Label(ExamForm,text="Session Index").grid(row=5,column=0,padx=10)
ttk.Label(ExamForm,text="Alloted Rooms Index").grid(row=6,column=0,padx=10)
ttk.Label(ExamForm,text="Student Strength Index").grid(row=7,column=0,padx=10)
CourseId_2_Index = ttk.Entry(ExamForm)
CourseId_2_Index.grid(row=2,column=1)
CourseNameIndex = ttk.Entry(ExamForm)
CourseNameIndex.grid(row=3,column=1)
DateIndex = ttk.Entry(ExamForm)
DateIndex.grid(row=4,column=1)
SessionIndex = ttk.Entry(ExamForm)
SessionIndex.grid(row=5,column=1)
AllotmentIndex = ttk.Entry(ExamForm)
AllotmentIndex.grid(row=6,column=1)
StrengthIndex = ttk.Entry(ExamForm)
StrengthIndex.grid(row=7,column=1)
for child in ExamForm.winfo_children(): child.grid_configure(padx=5, pady=5)


footerFrame = ttk.Frame(generate)
footerFrame.grid(row =6 ,sticky="nswe")
ttk.Button(footerFrame,text="UPLOAD",command=UPLOAD).grid(row=0,sticky="we",padx=30)
uploadStatus = ttk.Label(footerFrame)
uploadStatus.grid(row=0,column=1,sticky="we")
ttk.Button(footerFrame,text="RUN",command=GENERATE_CSV).grid(row=1,sticky="we",padx=30)
generateStatus = ttk.Label(footerFrame)
generateStatus.grid(row=1,column=1,sticky="we")

for child in generate.winfo_children(): child.grid_configure(padx=5, pady=5)


converter = ttk.Labelframe(convert,text="CONVERTER",width=800)
converter.grid(row=1,sticky="nswe")
ttk.Label(converter,text="Upload seating csv file").grid(row=0,column=0)
csvPathBrowseButton = ttk.Button(converter, text="Browse",command=csvPathBrowseFunction).grid(row=0,column=1)
csvPath = ttk.Label(converter)
csvPath.grid(row=0,column=2)
ttk.Button(converter, text="UPLOAD",command=UPLOAD_CSV).grid(row=1,sticky="we",padx=30,pady=10)
uploadCSVStatus = ttk.Label(convert)
uploadCSVStatus.grid(row=1,column=1,sticky="we")
ttk.Button(converter, text="CONVERT",command=CONVERT_CSV).grid(row=2,sticky="we",padx=30,pady=10)
convertStatus = ttk.Label(convert)
convertStatus.grid(row=2,column=1,sticky="we")

for child in convert.winfo_children(): child.grid_configure(padx=5, pady=5)


for child in root.winfo_children(): child.grid_configure(padx=5, pady=5)
root.mainloop()