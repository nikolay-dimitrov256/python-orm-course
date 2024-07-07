import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Student


# Run and print your queries
def add_students():
    # first way
    Student.objects.create(
        student_id='FC5204',
        first_name='John',
        last_name='Doe',
        birth_date='1995-05-15',
        email='john.doe@university.com'
    )

    # second way
    student = Student(
        student_id='FE0054',
        first_name='Jane',
        last_name='Smith',
        email='jane.smith@university.com'
    )
    student.save()

    # third way
    students = []
    student = Student(
        student_id='FH2014',
        first_name='Alice',
        last_name='Johnson',
        birth_date='1998-02-10',
        email='alice.johnson@university.com'
    )
    students.append(student)
    student = Student(
        student_id='FH2015',
        first_name='Bob',
        last_name='Wilson',
        birth_date='1996-11-25',
        email='bob.wilson@university.com'
    )
    students.append(student)

    Student.objects.bulk_create(students)


def get_students_info():
    students = Student.objects.all()
    result = [f'Student №{s.student_id}: {s.first_name} {s.last_name}; Email: {s.email}' for s in students]

    return '\n'.join(result)


def update_students_emails():
    # first way
    """
    for student in Student.objects.all():
        student.email = student.email.replace('university.com', 'uni-students.com')
        student.save()
    """

    # second way - optimal
    students = Student.objects.all()
    for student in students:
        student.email = student.email.replace('university.com', 'uni-students.com')

    Student.objects.bulk_update(students, ['email'])


def truncate_students():
    Student.objects.all().delete()

# add_students()
# print(Student.objects.all())

# print(get_students_info())

# update_students_emails()
# for student in Student.objects.all():
#     print(student.email)


truncate_students()
print(Student.objects.all())
print(f"Number of students: {Student.objects.count()}")
