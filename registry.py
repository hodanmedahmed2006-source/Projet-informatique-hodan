from src.validation import (
    validate_id,
    validate_name,
    validate_phone,
    validate_grade,
)

# ----------------------------------------------------------------------
# 1. Add a new student
# ----------------------------------------------------------------------
def add_student(students):

    print("\n--- ADD STUDENT ---")

    # ID
    while True:
        id_str = input("ID (unique integer, or empty to cancel): ").strip()
        if id_str == "":
            print("Operation cancelled.")
            return
        try:
            student_id = validate_id(students, id_str, is_new=True)
            break
        except ValueError as e:
            print(f"Error: {e}")

    # Name
    while True:
        name_input = input("Name (non-empty, or empty to cancel): ").strip()
        if name_input == "":
            print("Operation cancelled.")
            return
        try:
            name = validate_name(name_input)
            break
        except ValueError as e:
            print(f"Error: {e}")

    # Phone
    while True:
        phone_input = input("Phone (digits only, or empty to cancel): ").strip()
        if phone_input == "":
            print("Operation cancelled.")
            return
        try:
            phone = validate_phone(phone_input)
            break
        except ValueError as e:
            print(f"Error: {e}")

    # Midterm grade
    while True:
        mid_str = input("Midterm grade (0-100, or empty to cancel): ").strip()
        if mid_str == "":
            print("Operation cancelled.")
            return
        try:
            midterm = validate_grade(mid_str, "midterm")
            break
        except ValueError as e:
            print(f"Error: {e}")

    # Final grade
    while True:
        final_str = input("Final grade (0-100, or empty to cancel): ").strip()
        if final_str == "":
            print("Operation cancelled.")
            return
        try:
            final = validate_grade(final_str, "final")
            break
        except ValueError as e:
            print(f"Error: {e}")

    # Store student
    students[student_id] = {
        "name": name,
        "phone": phone,
        "midterm": midterm,
        "final": final
    }
    print(f"Student {student_id} ({name}) added successfully.")

# ----------------------------------------------------------------------
# 2. Update an existing student
# ----------------------------------------------------------------------
def update_student(students):

    if not students:
        print("No students registered.")
        return

    print("\n--- UPDATE STUDENT ---")
    # Get existing ID
    while True:
        id_str = input("Student ID to update (or empty to cancel): ").strip()
        if id_str == "":
            print("Operation cancelled.")
            return
        try:
            student_id = validate_id(students, id_str, is_new=False)
            break
        except ValueError as e:
            print(f"Error: {e}")

    current = students[student_id]
    print(f"Student found: {current['name']} (ID {student_id})")

    # Field selection menu
    fields = {
        "1": "name",
        "2": "phone",
        "3": "midterm",
        "4": "final"
    }
    print("\nWhat would you like to update?")
    print("1. Name")
    print("2. Phone")
    print("3. Midterm grade")
    print("4. Final grade")
    print("0. Cancel")
    choice = input("Choice: ").strip()

    if choice == "0" or choice not in fields:
        print("Update cancelled.")
        return

    field = fields[choice]

    # Get new value with validation
    while True:
        new_value = input(f"New {field} (or empty to cancel): ").strip()
        if new_value == "":
            print("Update cancelled.")
            return
        try:
            if field == "name":
                validated = validate_name(new_value)
            elif field == "phone":
                validated = validate_phone(new_value)
            elif field in ("midterm", "final"):
                validated = validate_grade(new_value, field)
            else:
                validated = new_value
            break
        except ValueError as e:
            print(f"Error: {e}")

    # Apply update
    current[field] = validated
    print(f"Student {student_id} updated: {field} -> {validated}")

# ----------------------------------------------------------------------
# 3. Delete a student
# ----------------------------------------------------------------------
def delete_student(students):

    if not students:
        print("No students registered.")
        return

    print("\n--- DELETE STUDENT ---")
    while True:
        id_str = input("Student ID to delete (or empty to cancel): ").strip()
        if id_str == "":
            print("Operation cancelled.")
            return
        try:
            student_id = validate_id(students, id_str, is_new=False)
            break
        except ValueError as e:
            print(f"Error: {e}")

    student = students[student_id]
    print(f"You are about to delete: {student['name']} (ID {student_id})")
    confirm = input("Confirm (y/N)? ").strip().lower()
    if confirm == "y":
        del students[student_id]
        print(f"Student {student_id} deleted.")
    else:
        print("Deletion cancelled.")

# ----------------------------------------------------------------------
# 4. Search by ID
# ----------------------------------------------------------------------
def search_by_id(students):
    
    if not students:
        print("No students registered.")
        return

    print("\n--- SEARCH BY ID ---")
    id_str = input("Student ID (or empty to cancel): ").strip()
    if id_str == "":
        return
    try:
        student_id = validate_id(students, id_str, is_new=False)
    except ValueError as e:
        print(f"Error: {e}")
        return

    student = students[student_id]
    print(f"\nID       : {student_id}")
    print(f"Name     : {student['name']}")
    print(f"Phone    : {student['phone']}")
    print(f"Midterm  : {student['midterm']}")
    print(f"Final    : {student['final']}")
    avg = (student['midterm'] + student['final']) / 2
    print(f"Average  : {avg:.2f}")

# ----------------------------------------------------------------------
# 5. Search by name (partial match)
# ----------------------------------------------------------------------
def search_by_name(students):
    
    if not students:
        print("No students registered.")
        return

    print("\n--- SEARCH BY NAME ---")
    pattern = input("Name to search (partial, empty to cancel): ").strip()
    if pattern == "":
        return

    pattern_lower = pattern.lower()
    results = []
    for sid, data in students.items():
        if pattern_lower in data["name"].lower():
            results.append((sid, data))

    if not results:
        print("No student found.")
        return

    print(f"\n{len(results)} student(s) found:")
    for sid, data in results:
        print(f"  {sid} : {data['name']} (phone: {data['phone']})")