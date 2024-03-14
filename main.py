
from lupin import Lupin


def main():
    
    # Der defineres en funktion $f$
    def f(x): 
        return 2*x


    def k(x):

        def a(x):
            return 2*x**2

        return a(1)

    # Hejsa
    yield f(2)


lp = Lupin()
lp.add(main)
lp.save('out.pdf')
