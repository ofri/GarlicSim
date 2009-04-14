#import ptdraft.nib
#from nib import Nib
import nib
import random
from .core import Simulation


class Life(Simulation):
    """
    """

    def step(self,sourcenib,*args,**kwargs):
        oldboard=sourcenib.board
        newboard=Board(oldboard.width,oldboard.height)
        for x in range(oldboard.width):
            for y in range(oldboard.height):
                newboard.set(x,y,oldboard.will_become(x,y))
        newnib=nib.Nib()
        newnib.board=newboard
        newnib.clock=sourcenib.clock+1
        return newnib

    def make_plain_nib(self,width=50,height=50):
        mynib=nib.Nib()
        mynib.board=Board(width,height,make_random=False)
        mynib.clock=0
        return mynib

    def make_random_nib(self,width=50,height=50):
        mynib=nib.Nib()
        mynib.board=Board(width,height,make_random=True)
        mynib.clock=0
        return mynib

    def show(self,nib):
        pass



class Board(object):
    def __init__(self,width,height,make_random=False):
        (self.width,self.height)=(width,height)
        self.__list=[]
        for i in range(self.width*self.height):
            self.__list.append(False if make_random==False else random.choice([True,False]))
    def get(self,x,y):
        return self.__list[(x%self.width)*self.height+(y%self.height)]
    def set(self,x,y,value):
        self.__list[(x%self.width)*self.height+(y%self.height)]=value
    def get_neighbour_count(self,x,y):
        result=0
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if i==j==0:
                    continue
                if self.get(x+i,y+j)==True:
                    result+=1
        return result
    def will_become(self,x,y):
        n=self.get_neighbour_count(x,y)
        if self.get(x, y)==True:
            if 2<=n<=3:
                return True
            else:
                return False
        else: # self.get(x, y)==False
            if n==3:
                return True
            else:
                return False
    def __repr__(self):
        return "\n".join(["".join([("#" if self.get(x,y)==True else " ") for y in range(self.height)]) for x in range(self.width)])

