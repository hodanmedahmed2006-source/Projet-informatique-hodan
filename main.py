from src.registry import (
    add_student,
    update_student,
    delete_student,
    search_by_id,
    search_by_name,
)
from src.report_utils import print_class_report

def main():
   
    students = {}  # dictionary of student records

    while True:
        print("\n" + "=" * 40)
        print("Student Service Desk & Registry")
        print("=" * 40)
        print("1) Add student")
        print("2) Update student")
        print("3) Delete student")
        print("4) Find student by ID")
        print("5) Search by name")
        print("6) Print class report")
        print("0) Exit")
        print("-" * 40)

        choice = input("Choice: ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            update_student(students)
        elif choice == "3":
            delete_student(students)
        elif choice == "4":
            search_by_id(students)
        elif choice == "5":
            search_by_name(students)
        elif choice == "6":
            print_class_report(students)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 0 and 6.")

if __name__ == "__main__":
    main()