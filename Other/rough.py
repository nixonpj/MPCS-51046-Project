from datetime import datetime

time1 = datetime.utcnow()
time2 = datetime(2018, 10, 10)

print(time1)
print(time2)
print((time1 - time2).days / 30)


class A:
    a = 12
    b = 'strq'

    def func(self):
        pass


class B(A):
    c = A.a


x = A()
y = B()
print(B.c)

b = [4,5]
for i in range(len(b)):
    print(i)
