try:
    AgeError = Exception
    num_tickets = int(input('Какое количество билетов вы хотите приобрести?: '))
    
    sum = 0
    for i in range(num_tickets):
        age = int(input("Сколько лет %d посетителю?: " %(i+1)))
            
        if 0<=age<18:
           pass
        elif 18<=age<25:
            sum += 990
        elif age>=25:
            sum += 1390
        elif age<0:
            raise AgeError("Неправильный возраст")

except ValueError:
    print("Ошибка ввода. Вероятно вы ввели не число или оставили поле пустым")
    exit(0)
    input()
except AgeError:
    print("Неправильный возраст")
    exit(0)
    input()


discount = int(sum *0.1) if num_tickets > 3 else 0
end_sum = sum-discount
print("Итоговая сумма %d. Скидка %d" %(end_sum, discount))
