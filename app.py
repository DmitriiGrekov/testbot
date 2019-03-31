class Persons:
    lang1=""
    lang2=""
    
    def __init__(self,func):
        self.func=func
        print(self.func)
    def set_lang1(self,l1):
        self.lang1=l1
    def set_lang2(self,l2):
        self.lang2=l2

pit=Persons("Переводчик")
dig=Persons("калькулятор")

