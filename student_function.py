#student_function.py
from database_connect import student_collection  as collection

def insert_student(data):
    return collection.insert_one(data).inserted_id

def delete_student_by_id(student_id):
    return collection.delete_one({"student_id": student_id}).deleted_count

def find_by_id(student_id):
    return collection.find_one({"student_id": student_id})

def find_by_roll(roll_no):
    return list(collection.find({"roll_no": roll_no}))

def find_by_roll_no(roll_no):
    return collection.find_one({"roll_no": roll_no})

def find_by_name(name):
    return list(collection.find({"name": {"$regex": name, "$options": "i"}}))

def find_by_semester(sem):
    return list(collection.find({"current_semester": sem}))

def get_branch_count(year, branch):
    prefix = f"{year}-{branch}-"
    return collection.count_documents({"roll_no": {"$regex": f"^{prefix}"}}) + 1

def find_birthdays(month):
    pipeline = [
        {"$addFields": {"month": {"$month": "$dob"}}}, 
        {"$match": {"month": month}}
    ]
    return list(collection.aggregate(pipeline))

def update_marks_semester(student_id, semester, marks_dict):
    return collection.update_one(
        {"student_id": student_id},
        {"$set": {f"marks.{semester}": marks_dict}}
    )

def update_semester(student_id, new_semester):
    return collection.update_one(
        {"student_id": student_id},
        {"$set": {"current_semester": new_semester}}
    )

def add_fee_record(student_id, semester, fee_paid):
    return collection.update_one(
        {"student_id": student_id},
        {"$set": {f"semester_fee_history.{semester}": fee_paid}}
    )

def update_total_dues(student_id, new_dues):
    return collection.update_one(
        {"student_id": student_id},
        {"$set": {"total_dues": new_dues}}
    )

def reset_semester_fee(student_id):
    return collection.update_one(
        {"student_id": student_id},
        {"$set": {"semester_fees_paid": 0}}
    )