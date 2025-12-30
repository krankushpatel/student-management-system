# main.py
from authentication import login, change_password, create_new_staff_user
from main_function import *

def print_menu(is_admin: bool = False):
    print("\n===== STUDENT MANAGEMENT SYSTEM =====")

    if is_admin:
        print("0. Create New Staff User (ADMIN ONLY)")
        print("1. Add Student")
        print("2. Delete Student")
        print("10. Promote Student to Next Semester")

    # Common options for both
    common = [
        "3. Fee Status (Single Student)",
        "4. Fee Status (Semester-wise All Students)",
        "5. Birthday List (All Students)",
        "6. Show Marks & Result (Single Student)",
        "7. Search by Student ID",
        "8. Search by Name / Roll / Semester",
        "9. Add Marks by Roll No",
        "11. Change Password",
        "12. Exit"
    ]
    print("\n".join(common))


def admin_staff_main(user: dict):

    is_admin = user.get("role") == "admin"

    admin_actions = {
        "0": create_new_staff_user,
        "1": add_student,
        "2": delete_student,
        "10": promote_student_semester
    }

    common_actions = {
        "3": show_fee_status,
        "4": show_fee_status_semester_wise,
        "5": show_birthdays_all,
        "6": show_marks_and_result,
        "7": search_student_by_id,
        "8": search_by_name_roll_sem,
        "9": add_marks_by_roll,
        "11": lambda: change_password(user),
    }

    
    while (3>1):
        print_menu(is_admin)
        choice = input("Enter choice: ").strip()

        # ADMIN only choices
        if is_admin and choice in admin_actions:
            admin_actions[choice]()

        # COMMON choices
        elif choice in common_actions:
            common_actions[choice]()

        elif choice == "12":
            print("Exiting... Thank You for Visiting!")
            break

        else:
            print("Invalid choice...")


# STUDENT MENU

def student_menu(user: dict):

    actions = {
        "1": lambda: print_student_info(get_student_by_id(user.get("student_id"))),
        "2": lambda: show_marks_for_student_record(get_student_by_id(user.get("student_id"))),
        "3": lambda: change_password(user),
    }

    while not None:
        print("\n===== STUDENT DASHBOARD =====")
        print("1. View My Profile")
        print("2. View My Semester-wise Marks")
        print("3. Change Password")
        print("4. Logout")

        choice = input("Enter choice: ").strip()

        if choice == "4":
            print("Logging out from student panel...")
            break

        elif choice in actions:
            student = get_student_by_id(user.get("student_id"))
            if student:
                actions[choice]()
            else:
                print("Your student record not found...")

        else:
            print("Invalid choice.")


if __name__ == "__main__":

    while " ":
        user = login()
        if not user:
            print("Login failed. Exiting.")
        else:
            if user.get("role") == "student":
                student_menu(user)
            else:
                admin_staff_main(user)