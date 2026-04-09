def compute_final_grade(student):

    return (student['midterm'] + student['final']) / 2

def print_class_report(students):
    
    if not students:
        print("No students registered.")
        return

    # Build a list of (id, name, final_grade)
    records = []
    for sid, data in students.items():
        final = compute_final_grade(data)
        records.append((sid, data['name'], final))

    # Sort by final grade descending for top/bottom
    records.sort(key=lambda x: x[2], reverse=True)

    class_size = len(records)
    total = sum(r[2] for r in records)
    average = total / class_size

    top_id, top_name, top_grade = records[0]
    bottom_id, bottom_name, bottom_grade = records[-1]

    # Extra statistic: standard deviation (population)
    variance = sum((r[2] - average) ** 2 for r in records) / class_size
    std_dev = variance ** 0.5

    print("\n--- CLASS REPORT ---")
    print(f"Class size: {class_size}")
    print(f"Average final grade: {average:.2f}")
    print(f"Top student: {top_id} ({top_name}) -> {top_grade:.2f}")
    print(f"Bottom student: {bottom_id} ({bottom_name}) -> {bottom_grade:.2f}")
    print(f"Standard deviation: {std_dev:.2f}")