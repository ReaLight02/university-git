#  (con map ma non funzia)

# -*- coding: utf-8 -*-
'''Nel gioco "chi la spara più grossa" si sfidano due concorrenti A e
B che generano delle sequenze di valori di lunghezza variabile,
rappresentati da un singolo carattere. Le sequenze possono essere di
lunghezza diversa poiché i valori possono essere separati da uno (o
più) spazi bianchi e tab ('\t'). Il numero di caratteri non spazio è,
comunque, uguale per ogni sequenza.

Ogni elemento della sequenza di A viene confrontato con l'elemento
corrispondente della sequenza di B e viene assegnato un punto
- al concorrente che ha generato il valore più alto (per esempio A),
  se la differenza fra il valore di A e il valore di B è inferiore o
  uguale ad un parametro k deciso all'inizio della sfida
- al concorrente che ha generato il valore più basso (per esempio B),
  se la differenza fra il valore di A e il valore di B è superiore
  a k (cioè A ha sballato)
- a nessuno, in caso di pareggio.
Al termine dell'assegnazione, vince chi ha ottenuto più punti. In caso
di pareggio, vince il giocatore che ha generato la sequenza con somma
totale dei valori inferiore. In caso di ulteriore pareggio, il punto
è assegnato al giocatore con la prima sequenza in ordine
lessicografico. Non può capitare che due giocatori generino
esattamente la stessa sequenza di valori.

Si deve realizzare una funzione che prende in input il parametro k e
una lista di stringhe corrispondenti a un torneo di "chi la spara più
grossa" e restituisce la classifica finale del torneo. La stringa in
posizione i corrisponde alla sequenza dei valori generati dal
giocatore i.

Nel torneo, ogni giocatore sfida tutti gli altri con la propria
sequenza: ovvero, se ci sono n giocatori, ogni giocatore farà n-1
sfide. Il numero di sfide vinte determina la posizione in
classifica. In caso di parità di sfide vinte, i giocatori sono
ordinati in modo crescente in base alla posizione.

Esempio di partite a chi la spara più grossa fra tre giocatori.
    Se k=2 e la lista è ["aac","ccc","caa"]
        La sfida 0, 1 è vinta da 1 per 2 punti a 0, poiché la
            differenza fra "c" e "a" è inferiore o uguale a 2
        La sfida 0, 2 è un pareggio 1 a 1, le due sequenze hanno somma
            uguale, ma vince 0 perché la sequenza "aac" < "caa".
        La sfida 1, 2 è vinta da 1 per 2 punti a 0, poiché la
            differenza fra "c" e "a" è inferiore o uguale a 2.
        Alla fine 0 ha 1 sfida, 1 ha 2 sfide e 2 ha 0 sfide, per cui
            la classifica finale sarà [1, 0, 2].

    Se k=1 e la lista è ["aac","ccc","caa"]
        La sfida 0, 1 è vinta da 0 per 2 punti a 0, poiché la
            differenza fra "c" e "a" è maggiore di 1.
        La sfida 0, 2 è un pareggio 1 a 1, le due sequenze hanno somma
            uguale, ma vince 0 perché la sequenza "aac" < "caa".
        La sfida 1, 2 è vinta da 2 per 2 punti a 0, poiché la
            differenza fra "c" e "a" è maggiore di 1.
        Alla fine 0 ha 2 sfide, 1 ha 0 sfide e 2 ha 1 sfida, per cui
            la classifica finale sarà [0, 2, 1].

    Se k=10 e la lista è  [ "abc",  "dba" , "eZo"]
        La sfida 0, 1 è un pareggio, ma vince 0 perché la sua sequenza
            ha somma inferiore.
        La sfida 0, 2 è vinta da 0 per 2 punti a 1, perché 2 sballa
            con la lettera 'o' contro 'c'.
        La sfida 1, 2 è vinta da 1 per 2 punti a 1, perché 2 sballa
            con la lettera 'o' contro 'a'
        Alla fine 0 ha 2 sfide, 1 ha 1 sfida e 2 ha 0 sfide, per cui
            la classifica finale sarà [0, 1, 2].

    Se k=50 e la lista è  [ "A ƐÈÜ",  "BEAR" , "c Ʈ  ´  ."]
        La sfida 0, 1 è vinta da 1 per 4 punti a 0.
        La sfida 0, 2 è vinta da 2 per 3 punti a 1.
        La sfida 1, 2 è vinta da 1 per 3 punti a 1.
        Alla fine 0 ha 0 sfide, 1 ha 2 sfida e 2 ha 1 sfide, per cui
        la classifica finale sarà [1, 2, 0].

Il timeout per l'esecuzione di ciascun test è di 6 secondi (*2 sualla VM)

'''

def ex(matches, k):
    matches = list(map(lambda x: x.replace(' ', '').replace('\t', ''),matches))
    ord_values = set("".join(matches))
    ord_values = {i:ord(i) for i in ord_values}
    mapping = [(matches[i],matches[j]) for i in range(len(matches)) for j in range(i+1,len(matches))]
    results = dict.fromkeys(range(len(matches)),0)
    def get_char_win(a,b):
        # print("==>",a,b)
        if abs(ord_values[a] - ord_values[b]) <= k:
            if ord_values[a] > ord_values[b]:
                return 0
            else:
                return 1
        else:
            if ord_values[a] > ord_values[b]:
                return 1
            else:
                return 0
    def check_lower(tupla):
        if tupla[0] < tupla[1]:
            return 0
        else:
            return 1
    def check_lower_sum(tupla):
        if sum([ord_values[i] for i in tupla[0]]) < sum([ord_values[i] for i in tupla[1]]):
                return 0
        else:
            return 1
    def check_equal(tupla):
        if sum([ord_values[i] for i in tupla[0]]) == sum([ord_values[i] for i in tupla[1]]):
            return check_lower(tupla)
        else:
            return check_lower_sum(tupla)
    def get_string_win(tupla):
        results = [get_char_win(a,b) for a,b in zip(tupla[0],tupla[1]) if a != b]
        if results.count(0) == results.count(1):
            return check_equal(tupla)
        else:
            if results.count(0) > results.count(1):
                return 0
            else:
                return 1
    def get_results(mapping):
        lista = list(map(get_string_win,mapping))
        return lista
    temp_results = get_results(mapping)
    # [('aac', 'ccc'), ('aac', 'caa'), ('ccc', 'caa')]
    # [1,0,0]
    for i in range(len(temp_results)):
        match = mapping[i]
        results[matches.index(match[temp_results[i]])] += 1
    return list(sorted(results,key=results.get,reverse=True))

if __name__ == "__main__":
    # Inserisci qui i tuoi test
    pass
