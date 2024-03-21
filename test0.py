
from lupin import Lupin
import kaxe

def main():
    
    # Der defineres en funktion $f$
    def f(x): 
        return 2*x
    
    # lad $a>0$ og $b<0$ så gælder at $a>0$
    def k(x):

        def a(x):
            return 2*x**2

        return a(1)

    # Derefter kan $f(2)$ nu regnes
    yield f(2)

    a = 2
    b = 3

    if a>b:
        print('hejsa')

    # hejsa
    yield k(1)

    plt = kaxe.Plot()

    plt.add(kaxe.Function(f))

    yield plt

lp = Lupin()
lp.add(main)
lp.save('out.pdf')
