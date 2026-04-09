def validate_id(students, id_str, is_new=True):
    
    try:
        student_id = int(id_str)
    except ValueError:
        raise ValueError("ID must be an integer.")

    if student_id <= 0:
        raise ValueError("ID must be a positive integer.")

    if is_new:
        if student_id in students:
            raise ValueError(f"ID {student_id} already exists.")
    else:
        if student_id not in students:
            raise ValueError(f"No student with ID {student_id} found.")

    return student_id

def validate_name(name_str):
    """
    Validate a student name.
    - name_str: input string
    Returns the name formatted with title().
    Raises ValueError if name is empty or contains only whitespace.
    """
    cleaned = name_str.strip()
    if not cleaned:
        raise ValueError("Name cannot be empty.")
    return cleaned.title()

def validate_phone(phone_str):
    
    # Keep only digits
    digits = ''.join(ch for ch in phone_str if ch.isdigit())
    if not digits:
        raise ValueError("Phone number must contain at least one digit.")
    # Optional: you could add length checks here (e.g., 8 digits)
    return digits

def validate_grade(grade_str, field_name="grade"):
    
    try:
        grade = float(grade_str)
    except ValueError:
        raise ValueError(f"{field_name} must be a number.")

    if grade < 0 or grade > 100:
        raise ValueError(f"{field_name} must be between 0 and 100.")

   
    return grade