'''
Credit to Daniel Shiffman for original seek function and
inspiration to create my own version of this program: 
https://github.com/shiffman/NOC-S17-2-Intelligence-Learning/tree/master/week2-evolution/01_evolve_steering
'''
class Vehicle():
    import math
    def __init__(self, x, y, dna = [random(256),random(256), random(4), random(4)]):
        self.pos = PVector(x,y)
        self.vel = PVector(0,0)
        self.acc = PVector(0,0)
        self.health = 1
        self.maxspeed = 2
        self.dna = dna #foodReach, poisonReach, foodAttraction, poisonAttraction
        self.r = 5
        self.maxforce = 0.4
        return
    
    def seek(self, target):
        desired = PVector.sub(target, self.pos)
        desired.setMag(self.maxspeed)
        steer = PVector.sub(desired, self.vel)
        steer.limit(self.maxforce)
        return steer
    
    def eat(self, targets, nutrition, type):
        #find closest food within range of sight
        closestD = width*height;
        closest = None
        for target in targets:
            d = self.pos.dist(target)
            if d < self.dna[type]: #type 0 = food, 1 = poison. Index modifier to point to dna vals based on target
                if d < closestD:
                    closestD = d
                    closest = target
        if closestD <= self.maxspeed*2: #close enough to eat the food
            #remove the food
            targets.remove(closest)
            #give nutrition
            self.health += nutrition #food nutrition value index
        elif closest: #seek the closest food
            self.applyForce(self.seek(closest)*self.dna[2+type]) #type 0 = food, 1 = poison. Index modifier... ^^^^
        #if no food within range of sight, do nothing
        return
    
    def boundaries(self):
        if self.pos.x < 0 or self.pos.x > width or self.pos.y < 0 or self.pos.y > height:
            self.applyForce(self.seek(PVector(width / 2, height / 2)))
            
    
    def applyForce(self, force):
        self.acc.add(force)
        return
    
    def update(self):
        #Update velocity
        self.vel.add(self.acc)
        #Limit and apply velocity
        self.vel.limit(self.maxspeed)
        self.pos.add(self.vel)
        #Reset acc
        self.acc.mult(0)
        #Degrade health slightly
        self.health -= 0.002
        return
    
    def show(self):
        if debug:
            #draw reaches for food and poison sight
            ellipseMode(CENTER)
            noFill()
            stroke(0,255,0)
            ellipse(self.pos.x, self.pos.y, self.dna[0] * 2, self.dna[0] * 2)
            stroke(255,0,0)
            ellipse(self.pos.x, self.pos.y, self.dna[1] * 2, self.dna[1] * 2)
        col = lerpColor(color(255,0,0),color(0,255,0), self.health)
        fill(col)
        noStroke()
        
        pushMatrix()
        translate(self.pos.x,self.pos.y)
        rotate(self.vel.heading() + PI / 2)
        beginShape()
        vertex(0, -self.r * 2)
        vertex(-self.r, self.r * 2)
        vertex(self.r, self.r *2)
        endShape(CLOSE)
        popMatrix()
        return
    
    @property
    def dead(self):
        return (self.health <= 0)
        