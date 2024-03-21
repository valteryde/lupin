from lupin import Lupin
import kaxe


def frekvensGraf(data):
    chart = kaxe.chart.Bar()

    chart.style(
        barGap=10
    )

    s = sum([data[i] for i in data])

    for key in data:
        chart.add(key.upper(), (data[key]/s)*100)

    return chart



def main():
    #! Frekvensanalyse af cæsar kryptering

    import math

    # Et ordinært frekvenanalyse for alle de engelske ord ser således ud
    
    distribution = {
        'a': 8.1,
        'b': 1.8,
        'c': 2.3,
        'd': 4.1,
        'e': 12.8,
        'f': 2.3,
        'g': 2,
        'h': 6.1,
        'i': 7,
        'j': 0.2,
        'k': 0.9,
        'l': 4,
        'm': 2.1,
        'n': 6.9,
        'o': 7.5,
        'p': 2,
        'q': 0.18,
        'r': 6,
        's': 6.3,
        't': 9,
        'u': 2.8,
        'v': 1,
        'w': 2.1,
        'x': 0.2,
        'y': 2,
        'z': 0.18,
    }

    s = sum([distribution[i] for i in distribution])

    for key in distribution:
        distribution[key] = distribution[key]/s

    yield frekvensGraf(distribution)

    # Givet en linje
    linje = "hello this is a message to Ceasar, someome will propbaly try to kill you. Stay save. Love Brutus"

    # Frekvensen af denne er kan findes ved nedenstående funktion
    alfabet = "abcdefghijklmnopqrstuvwxyz"
    def frekvensanalyse(linje):

        res = {}
        for bogstav in alfabet:
            res[bogstav] = linje.count(bogstav)

        s = sum([res[i] for i in res])
        for key in res:
            res[key] = res[key]/s

        return res

    frekvenser = frekvensanalyse(linje)
    yield frekvenser
    
    
    # Dertil kan nedenstående frekvensgraf laves
    yield frekvensGraf(frekvenser)

    # Dette minder om den første frekvenanalyse.
    # En cæsar kryptering skubber eller "rotere" alle bogstaver en vist antal
    # Funktionen for cæsar kryptering er herunder
    def krypter(linje, n):
        
        s = ''
        for bogstav in linje:
            if bogstav not in alfabet: continue

            s += alfabet[(alfabet.index(bogstav.lower()) + n) % 26]

        return s

    # Der anvendes nu $n=6$

    # Dermed bliver voers linje fra før nu
    cipher = krypter(linje, 6)
    yield cipher

    #Frekvensanalysen af den krypteret sætning er således
    yield frekvensGraf(frekvensanalyse(cipher))

    # Vi vil nu prøve at finde $n$ ved at gætte og sammenligne med den "rigtige" distribution af bogstaver
    # Dette gøres ned nedenstående funktion
    def kneakKoden(cipher):
        
        scores = []
        for i in range(26):
            
            guess = krypter(cipher, i)
            guessfreq = frekvensanalyse(guess)

            score = 0
            for bogstav in frekvenser:
                
                score += abs(distribution[bogstav] - guessfreq[bogstav])

            scores.append(score)
        
        return scores


    resultat = kneakKoden(cipher)
    yield resultat

    chart = kaxe.chart.Bar()

    chart.style(barGap=10)

    for i, res in enumerate(resultat):
        chart.add(i, res)

    yield chart

    # Dette indikere at for at rotere cipheren tilbage skal der bruges $n=20$
    yield 26-20
    # Dermed er den orginale er $n=6$

    # Og dekrpyteringen kan fortages med
    yield krypter(cipher, 20)

    #NB:
    # I praksis lavede man ikke alle analyse, man gættede bare på forflyningen og så mønstre


lp = Lupin()
lp.add(main)
lp.save('test3.pdf')
