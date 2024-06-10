### Task 1
def task_1():
    if input("Желаете изучить хиты продаж?\n").lower() == "да":
        if input("Интересующая катеогрия:\n").lower() == "продукты":
            print("Молоко 1л, Печенье с изюмом, Персики")
        else:
            print("Стиральный порошок, Щётка для обуви")
    else:
        "Дайте знать, если передумаете!"

# task_1()
# раскомментировать 11 строку, чтобы запустить первую функцию (убрать решетку)

### Task 2
def task_2():
    goods = []
    goods.append(input("Цена первого товара:\n"))
    goods.append(input("Цена второго товара:\n"))
    goods.append(input("Цена трертьего товара:\n"))
    sum_to_pay = max(goods)
    print(f"Акция! К оплате за три товара: {sum_to_pay}")


### Task 3
def task_3():
    goods = []
    goods.append(input("Цена первого товара:\n"))
    goods.append(input("Цена второго товара:\n"))
    goods.append(input("Цена трертьего товара:\n"))
    sum_to_pay = sum(goods)
    time_of_visit = int(input("Время покупки:\n"))
    if time_of_visit >= 20 and time_of_visit <= 22:
        print(f"Акция! Покупка совершена в счатливые часы! Итого к оплате: {sum_to_pay / 2}")
    elif time_of_visit >= 8 and time_of_visit <= 19:
        print(f"Итого к оплате: {sum_to_pay}")
    else:
        print("Магазин не работает!")
