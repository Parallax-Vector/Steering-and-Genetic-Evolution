'''
Credit to Daniel Shiffman for original seek function and
inspiration to create my own version of this program: 
https://github.com/shiffman/NOC-S17-2-Intelligence-Learning/tree/master/week2-evolution/01_evolve_steering
'''
from vehicle import Vehicle
debug = True
food = []
poison = []
vehicles = []
nutrition = [0.1,-0.2] #food, poison nutrition values

def setup():
    size(640,360)
    vehicles.append(Vehicle(width / 2, height / 2, [100, 300, 1, -2]))
    for i in range(25):
        food.append(PVector(random(width),random(height)))
        poison.append(PVector(random(width),random(height)))
    return

def draw():
    background(51)
    #add food and poison
    if random(1) < 0.05: #5% chance of adding food
        food.append(PVector(random(width),random(height)))
    if random(1) < 0.02: #2% chance of adding poison
        poison.append(PVector(random(width),random(height)))
    #draw food and poison
    for f in food:
        fill(0,255,0)
        noStroke();
        ellipse(f.x-5, f.y-5, 10, 10)
    for p in poison:
        fill(255,0,0)
        noStroke()
        ellipse(p.x-5, p.y-5, 10, 10)
        
    #draw and update vehicles
    for vehicle in vehicles:
        #vehicle.applyForce(vehicle.seek(target))
        vehicle.boundaries()
        vehicle.eat(food, nutrition[0], 0)
        vehicle.eat(poison, nutrition[1], 1)
        vehicle.update()
        if not vehicle.dead:
            vehicle.show()
        else:
            vehicles.remove(vehicle)
    return