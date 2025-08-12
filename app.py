from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["student_db"]
students_collection = db["students"]
counters_collection = db["counters"]

# Initialize counter if not exists
def initialize_counter():
    if counters_collection.count_documents({"_id": "student_id"}) == 0:
        counters_collection.insert_one({"_id": "student_id", "seq": 0})

# Get next sequential student ID
def get_next_student_id():
    counter = counters_collection.find_one_and_update(
        {"_id": "student_id"},
        {"$inc": {"seq": 1}},
        return_document=True
    )
    return counter["seq"]

# Add student
def add_student():
    name = input("Enter student name: ")
    age = int(input("Enter student age: "))
    grade = input("Enter student grade: ")
    address = input("Enter student address: ")
    phone_number = input("Enter student phone number: ")
    email = input("Enter student email: ")
    enrollment_date = input("Enter enrollment date (YYYY-MM-DD): ")

    student_id = get_next_student_id()

    student = {
        "student_id": student_id,
        "name": name,
        "age": age,
        "grade": grade,
        "address": address,
        "phone_number": phone_number,
        "email": email,
        "enrollment_date": enrollment_date
    }

    students_collection.insert_one(student)
    print(f"Student '{name}' added successfully with ID: {student_id}")

# List all students
def list_students():
    students = list(students_collection.find().sort("student_id", 1))
    if not students:
        print("No students found.")
    else:
        for s in students:
            print(f"ID: {s['student_id']}, Name: {s['name']}, Age: {s['age']}, Grade: {s['grade']}, "
                  f"Address: {s['address']}, Phone: {s['phone_number']}, Email: {s['email']}, "
                  f"Enrollment Date: {s['enrollment_date']}")

# Delete student by ID
def delete_student():
    student_id = int(input("Enter student ID to delete: "))
    result = students_collection.delete_one({"student_id": student_id})
    if result.deleted_count > 0:
        print(f"Student with ID {student_id} deleted successfully.")
    else:
        print("Student not found.")

# Update student by ID
def update_student():
    student_id = int(input("Enter student ID to update: "))
    student = students_collection.find_one({"student_id": student_id})
    if student:
        print("Leave field empty to keep current value.")
        name = input(f"Name [{student['name']}]: ") or student['name']
        age_input = input(f"Age [{student['age']}]: ")
        age = int(age_input) if age_input else student['age']
        grade = input(f"Grade [{student['grade']}]: ") or student['grade']
        address = input(f"Address [{student['address']}]: ") or student['address']
        phone_number = input(f"Phone Number [{student['phone_number']}]: ") or student['phone_number']
        email = input(f"Email [{student['email']}]: ") or student['email']
        enrollment_date = input(f"Enrollment Date [{student['enrollment_date']}]: ") or student['enrollment_date']

        updated_data = {
            "name": name,
            "age": age,
            "grade": grade,
            "address": address,
            "phone_number": phone_number,
            "email": email,
            "enrollment_date": enrollment_date
        }

        students_collection.update_one(
            {"student_id": student_id},
            {"$set": updated_data}
        )
        print(f"Student with ID {student_id} updated successfully.")
    else:
        print("Student not found.")

# Main menu loop
def menu():
    initialize_counter()
    while True:
        print("\nStudent Management System")
        print("1. Add Student")
        print("2. List Students")
        print("3. Delete Student")
        print("4. Update Student")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_student()
        elif choice == '2':
            list_students()
        elif choice == '3':
            delete_student()
        elif choice == '4':
            update_student()
        elif choice == '5':
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    menu()
