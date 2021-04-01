# Напишите функцию, которая печатает «обратную лесенку» следующего типа:

def print_ladder(n):
    for i in range(n,0,-1):
        print("*"*i)
 
n = int(input("Введите количество ступеней: "))
print_ladder(n)