
#Напишите программу, которой на вход подается последовательность чисел через пробел, а также запрашивается у пользователя любое число.
#В качестве задания повышенного уровня сложности можете выполнить проверку соответствия указанному в условии ввода данных.
#Далее программа работает по следующему алгоритму:
#Преобразование введённой последовательности в список
#Сортировка списка по возрастанию элементов в нем (для реализации сортировки определите функцию)
#Устанавливается номер позиции элемента, который меньше введенного пользователем числа, а следующий за ним больше или равен этому числу.
#При установке позиции элемента воспользуйтесь алгоритмом двоичного поиска, который был рассмотрен в этом модуле. Реализуйте его также отдельной функцией.


try:
    numbers = list(map(int, input("Введите последовательность чисел через пробел \n").split())) #получаем список чисел сразу в int
    user_num = int(input("Введите произвольное число: "))
except ValueError:
    print('Ошибка ввода. порограмма будет закрыта')
    input()
    exit(0)

#--------Для отладки
#numbers = [1, 5, 10, 18, 7, 4, 8] 
#user_num = 6

def BubbleSort(list):
    n=len(list)-1
    for i in range(n):
        for j in range(n-i):
            if list[j] > list [j+1]:
                list[j], list[j+1] = list [j+1], list[j]
    return list

def BinSearch(list,num,left,right):
    mid = len(list) // 2
    left = 0
    right = len(list) - 1
         
    if left > right:
        return False
     
    while list[mid] != num and left <= right:
        if num >= list[mid]:
            left = mid + 1
        else:
            right = mid - 1
        mid = (left + right) // 2

    else:
        return mid

sorted_numbers = BubbleSort(numbers)
left = sorted_numbers[0]
right = sorted_numbers[len(sorted_numbers)-1]
sought = BinSearch(sorted_numbers,user_num,left,right)
print('Сортированный список: ', sorted_numbers)
if sought == -1:
    print('Введенное число (%d) находится в начале списка'  % user_num)
elif sought+1<len(sorted_numbers):
    print('Введенное число (%d) идет после числа на позиции %d (между числами %d и %d), отсчет позиции начинается с единицы' 
    % (user_num, sought+1, sorted_numbers[sought], sorted_numbers[sought+1]))
else:
    print('Введенное число (%d) находится в конце списка'  % user_num)