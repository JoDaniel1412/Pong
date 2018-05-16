class Robot:
    def __init__(self, nombre, color, peso):
        self.name = nombre
        self.color = color
        self.weight = peso
    def introduce_self(self):
        print("My name is " + self.name)
r1 = Robot("Tom", "red", 30)
r2 = Robot("Jerry", "Blue", 40)
class Person:
    def __init__(self,n,p,i,r):
        self.name = n
        self.personality = p
        self.is_sitting = i
        self.robot_own = r
    def sit_down(self):
        self.is_sitting = True
    def stand_up(self):
        self.is_sitting = False
persona1 = Person("Alice", "agreesive", False)
persona1.robot_owned = r2
p2 = Person("Becky", "talkative", True)
p2.robot_owned = r1

