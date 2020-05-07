import random
class Myextension(object):
    def __init__(self,list1):
        self.__key = 'init'
        self.list1 =list1
    def Shuffle(self,list1):
        n=len(list1)
        print(n)
        while n>1:
            n=n-1
            k=random.randint(0,n+1)
            value=list1[k]
            list1[k]=list1[n]
            list1[n]=value

'''
list1=['10','20','30','40']
a = Myextension(list1)
a.Shuffle(list1)
print(list1)
'''



