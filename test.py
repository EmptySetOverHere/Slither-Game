class x:
        def __foo1(self):
                print("foo1")
        def foo2(self):
                self.__foo1()

y = x()

y.__foo1()