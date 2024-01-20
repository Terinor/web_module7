from sqlalchemy import create_engine, text, func
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Teacher, Subject, Grade

# Налаштування бази даних
username = 'postgres'
password = '12345'
host = 'localhost'
dbname = 'postgres'
database_url = f"postgresql+psycopg2://{username}:{password}@{host}/{dbname}"
engine = create_engine(database_url)
SessionLocal = sessionmaker(bind=engine)


# Функція select_1: Знайти 5 студентів із найбільшим середнім балом з усіх предметів
def select_1():
    with SessionLocal() as session:
        subquery = session.query(
            Grade.student_id,
            func.avg(Grade.grade).label('average_grade')
        ).group_by(Grade.student_id).subquery()

        top_students = session.query(
            Student.name,
            subquery.c.average_grade
        ).join(
            subquery, Student.id == subquery.c.student_id
        ).order_by(
            subquery.c.average_grade.desc()
        ).limit(5).all()

        return top_students


# Функція select_2: Знайти студента із найвищим середнім балом з певного предмета
def select_2(subject_id):
    with SessionLocal() as session:
        subquery = session.query(
            Grade.student_id,
            func.avg(Grade.grade).label('average_grade')
        ).filter(Grade.subject_id == subject_id
        ).group_by(Grade.student_id).subquery()

        top_student = session.query(
            Student.name,
            subquery.c.average_grade
        ).join(
            subquery, Student.id == subquery.c.student_id
        ).order_by(
            subquery.c.average_grade.desc()
        ).first()

        return top_student


# Функція select_3: Знайти середній бал у групах з певного предмета
def select_3(subject_id):
    with SessionLocal() as session:
        result = session.query(
            Group.name,
            func.avg(Grade.grade).label('average_grade')
        ).join(Student, Student.group_id == Group.id
        ).join(Grade, Grade.student_id == Student.id
        ).filter(Grade.subject_id == subject_id
        ).group_by(Group.id
        ).all()

        return result


# Функція select_4: Знайти середній бал на потоці
def select_4():
    with SessionLocal() as session:
        average_grade = session.query(
            func.avg(Grade.grade).label('average_grade')
        ).scalar()

        return average_grade


# Функція select_5: Знайти які курси читає певний викладач
def select_5(teacher_id):
    with SessionLocal() as session:
        courses = session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()
        return [course.name for course in courses]


# Функція select_6: Знайти список студентів у певній групі
def select_6(group_id):
    with SessionLocal() as session:
        students = session.query(Student.name).filter(Student.group_id == group_id).all()
        return [student.name for student in students]


# Функція select_7: Знайти оцінки студентів у окремій групі з певного предмета
def select_7(group_id, subject_id):
    with SessionLocal() as session:
        grades = session.query(
            Student.name,
            Grade.grade
        ).join(Grade, Student.id == Grade.student_id
        ).filter(
            Student.group_id == group_id,
            Grade.subject_id == subject_id
        ).all()

        return grades


# Функція select_8: Знайти середній бал, який ставить певний викладач
def select_8(teacher_id):
    with SessionLocal() as session:
        average_grade = session.query(
            func.avg(Grade.grade).label('average_grade')
        ).join(Subject, Subject.id == Grade.subject_id
        ).filter(Subject.teacher_id == teacher_id
        ).scalar()

        return average_grade


# Функція select_9: Знайти список курсів, які відвідує певний студент
def select_9(student_id):
    with SessionLocal() as session:
        courses = session.query(
            Subject.name
        ).join(Grade, Grade.subject_id == Subject.id
        ).filter(Grade.student_id == student_id
        ).distinct().all()

        return [course.name for course in courses]


# Функція select_10: Список курсів, які певному студенту читає певний викладач
def select_10(student_id, teacher_id):
    with SessionLocal() as session:
        courses = session.query(
            Subject.name
        ).join(Grade, Grade.subject_id == Subject.id
        ).filter(Grade.student_id == student_id
        ).filter(Subject.teacher_id == teacher_id
        ).distinct().all()

        return [course.name for course in courses]


# Тестування функцій
if __name__ == "__main__":
    print("Тестування функцій:")

    print("5 студентів із найбільшим середнім балом:")
    for student in select_1():
        print(student)

    subject_id_example = 1  # Замініть на існуючий ID предмета у вашій БД
    print(f"Студент із найвищим середнім балом з предмета (ID: {subject_id_example}):")
    print(select_2(subject_id_example))

    subject_id_example = 1  # Замініть на існуючий ID предмета у вашій БД
    print(f"Середній бал у групах з предмета (ID: {subject_id_example}):")
    for group in select_3(subject_id_example):
        print(group)

    print(f"Середній бал на потоці: {select_4()}")

    teacher_id_example = 1  # Замініть на існуючий ID викладача у вашій БД
    print(f"Курси, які читає викладач (ID: {teacher_id_example}):")
    for course in select_5(teacher_id_example):
        print(course)

    group_id_example = 1  # Замініть на існуючий ID групи у вашій БД
    print(f"Список студентів у групі (ID: {group_id_example}):")
    for student in select_6(group_id_example):
        print(student)

    group_id_example = 1  # Замініть на існуючий ID групи у вашій БД
    subject_id_example = 1  # Замініть на існуючий ID предмета у вашій БД
    print(f"Оцінки студентів у групі (ID: {group_id_example}) з предмета (ID: {subject_id_example}):")
    for student, grade in select_7(group_id_example, subject_id_example):
        print(f"Студент: {student}, Оцінка: {grade}")

    teacher_id_example = 1  # Замініть на існуючий ID викладача у вашій БД
    print(f"Середній бал, який ставить викладач (ID: {teacher_id_example}): {select_8(teacher_id_example)}")

    student_id_example = 1  # Замініть на існуючий ID студента у вашій БД
    print(f"Список курсів, які відвідує студент (ID: {student_id_example}):")
    for course in select_9(student_id_example):
        print(course)

    student_id_example = 1  # Замініть на існуючий ID студента у вашій БД
    teacher_id_example = 1  # Замініть на існуючий ID викладача у вашій БД
    print(f"Список курсів, які студенту (ID: {student_id_example}) читає викладач (ID: {teacher_id_example}):")
    for course in select_10(student_id_example, teacher_id_example):
        print(course)
