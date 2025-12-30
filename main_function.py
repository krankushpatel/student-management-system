# main_function.py

from utils import input_non_empty, input_phone_10_digits, validate_date, input_int, input_non_empty_name
from database_connect import user_collection as userc
from authentication import register_user
import student_function as stf
from class_Define import Student
from datetime import datetime


def print_student_info(s: dict):
    print("\n----------------")
    print(f"Name      : {s['name']}")
    print(f"Student ID: {s['student_id']}")
    print(f"Roll No   : {s['roll_no']}")
    print(f"Email     : {s['college_email']}")
    print(f"Branch    : {s['branch']}")
    print(f"Semester  : {s['current_semester']}")
    print(f"Phone     : {s['phone']}")
    print(f"DOB       : {s['dob'].strftime('%d-%m-%Y')}")
    print(f"Admission : {s['admission_date']}")
    print(f"Total Dues: {s.get('total_dues', 0)}")
    print("----------------\n")


def fee_details_stu(current_semester):
    ADMISSION = 1000
    SEM_FEE = 1500

    admission_paid = input_int("Enter admission fee paid: ", 0, ADMISSION)
    semester_paid = input_int("Enter semester fee paid: ", 0, SEM_FEE)

    dues = (ADMISSION + SEM_FEE) - (admission_paid + semester_paid)
    dues = max(0, dues)

    return admission_paid, semester_paid, dues


def add_student():
    name = input_non_empty_name("Enter Name: ")
    email = input_non_empty("Enter email: ").strip()
    address = input_non_empty("Enter address: ")
    branch = input_non_empty_name("Enter Branch(ME, CSE, ECE): ").upper()
    blood = input("Enter Blood group: ").strip()
    phone = input_phone_10_digits("Enter Phone no: ").strip()

    # Date of Birth Validation
    while True:
        dob_str = input("Enter DOB (DD-MM-YYYY): ").strip()
        try:
            dob_date = datetime.strptime(dob_str, "%d-%m-%Y")
            if dob_date > datetime.today():
                print("DOB cannot be a future date...")
                continue
            break
        except ValueError:
            print("Invalid date format. Please use DD-MM-YYYY")

    current_semester = input_int("Enter current semester(1-6): ", 1, 6)

    admission_date = datetime.now()
    admission_year = admission_date.year
    count = stf.get_branch_count(admission_year, branch)

    roll_no = f"{admission_year}-{branch}-{count:03d}"
    college_email = f"{roll_no.replace('-', '').lower()}@kle.ac.in"
    student_id = f"STU{admission_year}{branch}{count:03d}"

    print("\n--------Student Information---------")
    print(f"Student ID     : {student_id}")
    print(f"Roll No        : {roll_no}")
    print(f"College Email  : {college_email}")
    print(f"Admission Date : {admission_date.date()}")

    marks = {}
    print("\n------------------Fee Details-------------")

    admission_fee, semester_fee, total_dues = fee_details_stu(current_semester)

    student = Student(
        name=name,
        roll_no=roll_no,
        email=email,
        address=address,
        blood_group=blood,
        phone=phone,
        dob=dob_date,
        student_id=student_id,
        branch=branch,
        college_email=college_email,
        current_semester=current_semester,
        marks=marks,
        admission_fee_paid=admission_fee,
        semester_fees_paid=semester_fee,
        admission_date=admission_date,
        total_dues=total_dues
    )

    stf.insert_student(student.to_obj())
    print("\nStudent Inserted Successfully")

    # Auto-create login
    message = register_user(
        username=college_email,
        password=dob_str,
        role="student",
        student_id=student_id
    )
    print("Student login:", message)
    print("username :", college_email)
    print("password :", dob_str)
    print("student_id :", student_id)


def delete_student():
    stu_id = input("Enter Student ID: ").strip()
    stu = stf.find_by_id(stu_id)

    if not stu:
        print("Student not found.")
        return

    print_student_info(stu)

    if input("Delete student? (y/n): ").strip().lower() == "y":
        stf.delete_student_by_id(stu_id)
        userc.delete_one({"student_id": stu_id})
        print("Student deleted.")
    else:
        print("Cancelled.")


def show_fee_status():
    roll = input("Enter roll no: ").strip()
    student = stf.find_by_roll_no(roll)

    if not student:
        print("No student found.")
        return
    
    print("\n------ FEE STATUS ------")
    print_student_info(student)

    fee_history = student.get("semester_fee_history", {})

    print("Semester-wise Fee Paid:")
    for sem, fee in sorted(fee_history.items(), key=lambda x: int(x[0])):
        print(f"Semester {sem}: Paid → {fee}")

    print(f"\nTotal Dues: {student['total_dues']}")


def show_fee_status_semester_wise():
    sem = input_int("Enter the semester: ", 1, 6)
    students = stf.find_by_semester(sem)

    if not students:
        print("No students found.")
        return

    for s in students:
        paid = s.get("semester_fee_history", {}).get(str(sem), "No record")
        dues = s.get("total_dues", 0)
        print(f"{s['roll_no']}  {s['name']}  Paid: {paid}  Dues: {dues}")

def show_birthdays_all():
    month = int(input("Enter the month(1-12): "))
    students = stf.find_birthdays(month)

    if not students:
        print("No birthdays in this month.")
        return

    print(f"\n--- BIRTHDAYS IN MONTH {month} ---")
    for s in students:
        print("\n--------------------")
        print(f"Name      : {s['name']}")
        print(f"Roll No   : {s['roll_no']}")
        print(f"Student ID: {s['student_id']}")
        print(f"Semester  : {s['current_semester']}")
        print(f"DOB       : {s['dob'].strftime('%d-%m-%Y')}")
        print("--------------------")


def search_by_name_roll_sem():
    menu = {
        1: ("Enter name: ", stf.find_by_name),
        2: ("Enter roll no: ", stf.find_by_roll),
        3: ("Enter semester: ", stf.find_by_semester)
    }

    print("1. Search by Name\n2. Search by Roll No\n3. Search by Semester")
    choice = input_int("Enter choice: ", 1, 3)

    prompt, func = menu[choice]
    key = input(prompt)

    key = int(key) if choice == 3 else key
    students = func(key)

    if not students:
        print("No student found.")
        return

    for stu in students:
        print_student_info(stu)


def add_marks_by_roll():
    roll = input("Enter roll no: ").strip()
    student = stf.find_by_roll_no(roll)

    if not student:
        print("No student found.")
        return

    semester = input_int("Enter semester: ", 1, 6)

    if semester != student["current_semester"]:
        print(f"You can only add marks for current semester: {student['current_semester']}")
        return

    subjects = ["math", "english", "physics", "chemistry", "IT"]
    marks_dict = {sub: input_int(f"{sub}: ", 0, 100) for sub in subjects}

    stf.update_marks_semester(student["student_id"], semester, marks_dict)
    print("Marks updated successfully!")


def promote_student_semester():
    roll = input("Enter roll no: ").strip()
    student = stf.find_by_roll_no(roll)

    if not student:
        print("No student found.")
        return

    current = student["current_semester"]

    if current >= 6:
        print("Student already in highest semester.")
        return

    new_sem = current + 1
    SEM_FEE = 1500

    new_dues = student["total_dues"] + SEM_FEE

    stf.update_total_dues(student["student_id"], new_dues)
    stf.add_fee_record(student["student_id"], current, student.get("semester_fees_paid", 0))
    stf.update_semester(student["student_id"], new_sem)
    stf.reset_semester_fee(student["student_id"])
    stf.add_fee_record(student["student_id"], new_sem, 0)

    print(f"Promoted to Semester {new_sem}. Total Dues: {new_dues}")


def show_marks_for_student_record(student):
    marks = student.get("marks", {})

    if not marks:
        print("No marks available.")
        return

    print("\n--------- STUDENT MARKS ---------")
    for sem, subs in marks.items():
        print(f"\n--- Semester {sem} ---")
        for sub, score in subs.items():
            print(f"{sub}: {score}")


def show_marks_and_result():
    roll = input("Enter roll no: ").strip()
    student = stf.find_by_roll_no(roll)

    if not student:
        print("No student found.")
        return

    show_marks_for_student_record(student)

def search_student_by_id():
    sid = input("Enter Student ID: ").strip()
    s = stf.find_by_id(sid)
    if not s:
        print("Student not found.")
        return
    print_student_info(s)


def get_student_by_id(student_id):
    return stf.find_by_id(student_id)