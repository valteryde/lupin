from lupin import Lupin
import kaxe

l = [0,1,2,3]


def main():

    plt = kaxe.Plot([0, 0.3, 1, 3])



lp = Lupin()
lp.add(main, False)
lp.save('test4.pdf')

