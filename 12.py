# students = [1, 2, 3]
#
# def function_one():
#     global students
#     print(students)
#     students = ['Коля', 'Настя']
#     print(students)
#
# def function_two():
#     students = 2
#     print(students)
#
# function_one()
# function_two()
# print(students)


# правило LEGB
# L (Local) — внутри функции или класса, где была объявлена переменная.
# E (Enclosing) — внутри внешних функций, от ближайшего к дальнему.
# G (Global) — на уровне модуля или скрипта.
# B (Built-in) — встроенные функции и исключения Python.

x = "global"

# def outer():
#     x = "enclosing"
#
#     def inner():
#         x = "local"
#         print(x)
#
#     inner()
#     print(x)
#
# outer()
# print(x)

# students = [1, 2, 3]
#
# def function_one():
#     students = ['Коля', 'Настя']
#     print(43, students)
#
#     def function_two():
#         students = ['Коля', 'Настя', 'Никита']
#         print(47, students)
#
#         def function_three():
#             nonlocal students
#
#             students = 2
#             print(53, students)
#
#         function_three()
#         print(56, students)
#
#     function_two()
#     print(59, students)
#
# function_one()
# print(students)


for i in range(5):
    x = i * 10
    print(x)

print("Последнее значение x:", x)