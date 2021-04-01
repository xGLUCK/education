#Создайте генератор цикла, то есть в функцию на входе будет 
#передаваться массив, например, [1, 2, 3], генератор будет 
#вечно работать возвращая 1 2 3 1 2 3… и так далее.

#array = input("Введите массив, разделяя элементы пробелом: \n").split()
array = [1,2,3]

def generator(array):
    i=0
    while True:        
        result = array[i]
        a = len(array)
        if i<len(array):
            i+=1
        if i >= 3:
            i=0
        yield result

next_gen = iter(generator(array))
while True:
    print(next(next_gen))
    #input()
