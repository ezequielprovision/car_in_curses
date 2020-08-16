'''
- Crear clase "Persona" para ejercicio 1 de clase 1 con los atributos nombre, edad, temperatura y crear los siguientes metodos:
  - fiebre() Devuelve True o False si la temperatura supera los 37 grados
  - es_mayor_de_edad() Devuelve True o False si la persona es mayor de 18 años

- Crear clase "Auto" que va a tener propiedades X e Y, y va a tener un metodo avanzar, 
otro metodo retroceder, otro metodo girar que puede ser para la derecha o la izquierda. 
Cuando llamamos a avanzar, incrementa en Y, cuando llamamos a retroceder, resta en Y, cuando giramos a la derecha y avanzamos luego, 
suma en X... cuando giramos a la izquierda nuevamente va a sumar en Y, y si giramos a la izquierda una vez mas, resta en X

     |
     |
<---------->
     |
     |

Tambien meter un metodo "empezar", donde empieza a recibir los comandos para manejar e ir imprimiendo la posicion actual. 
En lo posible usar curses con la flechita 
'''
import curses
import time

class Person():
    def __init__(self, name, age, temperature):
        self.name = name
        self.age = age
        self.temperature = temperature

    def get_person_data(self):
        self.name = screen.getstr('Insert name')
        self.age = int(screen.getstr('Insert age'))
        self.temperature = float(screen.getstr('Insert temperature'))
    
    def show_person_data(self):
        return 'Name : {}, Age : {}, Temperature : {}'.format(self.name, self.age, self.temperature)
    
    def has_fever(self):
        return self.temperature >= 37.5         
    
    def is_major(self):
        return self.age >= 18


class Car():
    directions = ('up', 'right', 'down', 'left')
    image = ('^', '>', 'v', '<')
    def __init__(self):
        self.coor_x = None
        self.coor_y = None
        self.car_direction = self.directions[0]
        self.has_started = False
    
    
    def start_driving(self):
        self.has_started = True
        self.coor_x = WIDHT//2
        self.coor_y = HEIGHT//2

    def set_position(self, x, y):
        self.coor_x = x
        self.coor_y = y

    def move_foward(self):
        if self.car_direction == 'up':
            self.coor_y -= 1
        elif self.car_direction == 'down':
            self.coor_y += 1
        elif self.car_direction == 'right':
            self.coor_x += 1
        elif self.car_direction == 'left':
            self.coor_x -= 1
    
    def move_back(self):
        if self.car_direction == 'up':
            self.coor_y += 1
        elif self.car_direction == 'down':
            self.coor_y -= 1
        elif self.car_direction == 'right':
            self.coor_x -= 1
        elif self.car_direction == 'left':
            self.coor_x += 1

    def turn_direction(self, key):
        if key == curses.KEY_RIGHT:
            if self.car_direction == self.directions[-1]:
                self.car_direction = self.directions[0]
            else:
                self.car_direction = self.directions[self.directions.index(self.car_direction) + 1] # con itertools seguro se hace mejor
        
        elif key == curses.KEY_LEFT:
            if self.car_direction == self.directions[0]:
                self.car_direction = self.directions[-1]
            else:
                self.car_direction = self.directions[self.directions.index(self.car_direction) - 1]
        
    
    def get_car_image(self):
        return self.image[self.directions.index(self.car_direction)]



class Racetrack():
    matrix = []
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.create_racetrack()

    def create_racetrack(self):
        for x in range(self.height):
            vector = []
            for y in range(self.width):
                if (x == 0) or (x == self.height - 1) or (y == 0) or (y == self.width - 1):
                    vector.append(2)
                else:
                    vector.append(0)
            self.matrix.append(vector)

    def show_cursor(self, x, y):
        if self.matrix[y][x] == 0:
            return ' '
        elif self.matrix[y][x] == 2:
            return 'x'
        else:
            return 'car'
    
    def can_pass(self, x, y):
        return self.matrix[y][x] != 2




###########################################################################

""" 
donde empieza a recibir los comandos para manejar e ir imprimiendo la posicion actual

MEDIO QUE ESTO NO LO ENTENDI BIEN, O AL MENOS ME SALIO HACERLO DE OTRA FORMA
"""


WIDHT = 60
HEIGHT = 20

racetrack = Racetrack(WIDHT, HEIGHT)
driver = Person('Viru', 31, 36.7)
car = Car()

screen = curses.initscr()
curses.noecho()  
curses.cbreak()
curses.curs_set(False) # hace que no se vea el cursor
  
try:
    screen.keypad(True)
    while True:
        screen.clear() 
        for y in range(HEIGHT):
            for x in range(WIDHT):
                cursor = racetrack.show_cursor(x, y)
                if cursor == 'car':
                    cursor = car.get_car_image()
                elif cursor == 'x':
                    cursor = 'x'
                screen.addstr(y, x, "{}".format(cursor))
        
        screen.addstr(HEIGHT + 2, (WIDHT//2) - 12, "x :{} - y:{}".format(car.coor_x, car.coor_y))
        screen.refresh() 
        
        key = screen.getch() 

        if key == ord('q'):
            break

        if car.has_started:
            if key == curses.KEY_LEFT:
                car.turn_direction(key)
                
            elif key == curses.KEY_RIGHT:
                car.turn_direction(key)
            
            elif key == curses.KEY_UP:
                """ es la manera mas facil que encontre de chequear que pueda moverse el auto sin romper"""
                aux_x, aux_y = car.coor_x, car.coor_y
                car.move_foward()
                if racetrack.can_pass(car.coor_x, car.coor_y):
                    racetrack.matrix[aux_y][aux_x] = 0
                    racetrack.matrix[car.coor_y][car.coor_x] = 1
                else:
                    car.set_position(aux_x, aux_y)
                
            elif key == curses.KEY_DOWN:
                aux_x, aux_y = car.coor_x, car.coor_y
                car.move_back()
                if racetrack.can_pass(car.coor_x, car.coor_y):
                    racetrack.matrix[aux_y][aux_x] = 0
                    racetrack.matrix[car.coor_y][car.coor_x] = 1
                else:
                    car.set_position(aux_x, aux_y)
                
            elif key == ord('p'):
                screen.addstr(HEIGHT + 4, 0, driver.show_person_data())
                screen.refresh()
                time.sleep(1)
                screen.addstr(HEIGHT + 5, 0, "Fever {}".format(driver.has_fever()))
                screen.refresh()
                time.sleep(1)
                screen.addstr(HEIGHT + 6, 0, "Major {}".format(driver.is_major()))
                screen.refresh()
                time.sleep(1)


        elif key == ord('s'):
            car.start_driving()
            racetrack.matrix[car.coor_y][car.coor_x] = 1 # elegi dejarlo por fuera del metodo star driving asi no mezclo una clase con otra



finally:
    screen.keypad(False)
    curses.curs_set(True)
    curses.nocbreak()
    curses.echo()
    curses.endwin()
    