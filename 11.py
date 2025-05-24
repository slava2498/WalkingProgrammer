# for i in range(10):
#     if i == 5:
#         break
#     print(i)


students = [{
    "name": "Николай",
    "assessments": [5, 5, 5, 5, 5]
}, {
    "name": "Иван",
    "assessments": [5, 5, 5, 5, 5]
}, {
    "name": "Наталья",
    "assessments": [5, 5, 5, 5, 5]
}, {
    "name": "Ольга",
    "assessments": [5, 5, 5, 5, 5]
}, {
    "name": "Никита",
    "assessments": [5, 5, 5, 5, 5]
}]

# break_flag = False
# for student in students:
#     for assessment in student['assessments']:
#         if assessment != 5:
#             break_flag = True
#             break
#
#     if break_flag:
#         break
#
# if not break_flag:
#     print("В классе все отличники.")
# else:
#     print("В классе не все отличники.")
#
# for student in students:
#     break_flag = False
#     if 2 in set(student['assessments']):
#         break
#
#
# for i in range(10):
#     if i % 2 == 0:
#         continue
#     print(i)


# excellent_students = []
# for student in students:
#     if {2, 3, 4} & set(student['assessments']):
#         continue
#
#     excellent_students.append(student['name'])
#
# print(excellent_students)

# for i in range(5):
#     print(i)
#     break
# else:
#     print("Цикл завершен без прерываний.")


break_flag = False
for student in students:
    for assessment in student['assessments']:
        if assessment != 5:
            break_flag = True
            break

    if break_flag:
        break
else:
    print("В классе все отличники.")

