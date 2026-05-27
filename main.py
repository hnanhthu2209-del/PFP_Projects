from models.user import Admin, Organizer, Student

admin = Admin("A001", "Alice", "admin123") # this is the object we use
organizer = Organizer("B001", "Bob", "org123")
student = Student("S001", "Charlie", "stu123")

print(admin)
print(organizer)
print(student)

#Print menus
print("\n--- Admin menu ---") # start the content after \n in a new line
for i, option in enumerate(admin.get_menu(), 1): # give the number and the item at the same time
    print(f"{i}. {option}")

print("\n--- Student menu ---") # start the content after \n in a new line
for i, option in enumerate(student.get_menu(), 1): # give the number and the item at the same time
    print(f"{i}. {option}")