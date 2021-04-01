#Создайте класс любых геометрических фигур, где на выход мы получаем характеристики фигуры. 
#Каждый экземпляр должен иметь атрибуты, которые зависят от выбранной фигуры. Например, для прямоугольника это будут аргументы x, y, width и height.
#Кроме того вы должны иметь возможность передавать эти атрибуты при создании объекта класса.
#Создайте метод, который возвращает атрибуты вашей фигуры в виде строки. 

class RegularDodecahedron:        
    def __init__(self, edge):
        self.__edge = edge

    def edge(self):
        return self.__edge
    
    def square(self):
        e=self.__edge
        s=3*e**2*(5*(5+2*5**.5))**.5
        return s

figure = RegularDodecahedron(5)
print(figure.edge())
print(figure.square())