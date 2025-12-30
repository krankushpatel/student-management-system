from datetime import datetime

class Student:
    def __init__(self,name: str,roll_no: str,email: str,address: str,blood_group: str,phone: str,dob: datetime,student_id: str,branch: str,college_email: str,current_semester: int,marks: dict = None,admission_fee_paid: int = 0,semester_fees_paid: int = 0,admission_date: datetime = None,total_dues: int = 0):

        self.name = name
        self.roll_no = roll_no
        self.email = email
        self.address = address
        self.blood_group = blood_group
        self.phone = phone
        self.dob = dob
        self.student_id = student_id
        self.branch = branch
        self.college_email = college_email
        self.current_semester = int(current_semester)
        self.marks = marks or {} 

        self.admission_fee_paid = int(admission_fee_paid)
        self.semester_fees_paid = int(semester_fees_paid)

        self.admission_date = admission_date or datetime.now()
        self.total_dues = int(total_dues)

        self.semester_fee_history = {
            str(self.current_semester): self.semester_fees_paid
        }

    
    # Convert Object to Dictionary for MongoDB
    def to_obj(self):
        return {
            "name": self.name,
            "roll_no": self.roll_no,
            "email": self.email,
            "address": self.address,
            "blood_group": self.blood_group,
            "phone": self.phone,
            "dob": self.dob,
            "student_id": self.student_id,
            "branch": self.branch,
            "college_email": self.college_email,
            "current_semester": self.current_semester,
            "marks": self.marks,
            "admission_fee_paid": self.admission_fee_paid,
            "semester_fees_paid": self.semester_fees_paid,
            "admission_date": self.admission_date,
            "semester_fee_history": self.semester_fee_history,
            "total_dues": self.total_dues
        }
