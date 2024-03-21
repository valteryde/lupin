from lupin import Lupin


def main():
    #! Spændingskoncentrationer
    #!!! Valter Yde Daugberg

    import math
    import kaxe

    def moment(rd):
        #Givet at Dd = 36/30, så gælder
        A = 0.99590
        b = -0.23829
        return A*math.pow(rd, b)

    def torsion(rd):
        #Givet at Dd = 36/30, så gælder
        A = 0.90182
        b = -0.22334
        return A*math.pow(rd, b)

    #Finder spændingskoncentration $\sigma$ under moment
    yield moment(1/30)
    
    #Finder spændingskoncentration $\sigma$ under torision
    yield torsion(1/30)
    
    plt = kaxe.Plot([0, 0.3, 1, 3])

    plt.title('$\\frac{r}{d}$', '$K_{t}$')

    mf = kaxe.Function(moment).legend('Moment')
    Tf = kaxe.Function(torsion).legend('Torision')

    plt.add(mf)
    plt.add(Tf)

    yield plt


lp = Lupin()
lp.add(main)
lp.save('test2.pdf')
