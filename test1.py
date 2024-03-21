
from lupin import Lupin
import kaxe

def main():
    
    # Defineres to konstanter, $a$ og $b$
    a = 2
    b = 3

    # Der defineres en funktion $f$
    def f(x):
        return a*x+b
    
    # Derefter kan $f(2)$ nu regnes
    yield f(2)

    yield (f(2/4)**2) / (10+f(1))

    plt = kaxe.Plot()

    plt.add(kaxe.Function(f))

    # Tegner grafen til $f(x)$
    yield plt


def single():
    plt = kaxe.Plot()
    yield 0


lp = Lupin()
lp.add(main)
lp.save('test1.pdf')
