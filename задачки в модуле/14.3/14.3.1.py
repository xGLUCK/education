#Создайте функцию-генератор, возвращающую бесконечную последовательность натуральных чисел. 
#По умолчанию, она начинается с единицы и шагом 1, но пользователь может указать любой шаг и 
#любое число в качестве аргумента функции, с которого будет начинаться последовательность.

def nat_gen(start=1,step=1):
    n = start
    while True:
        yield n
        n+=step

start = input("стартовое число: ")
step = input("шаг: ")

if start and step:
    count = nat_gen(int(start), int(step))
elif start:
    count = nat_gen(int(start))
elif step:
    count = nat_gen(step = int(step))
else:
    count = nat_gen()
   
while True:    
    print(next(count))
    input()