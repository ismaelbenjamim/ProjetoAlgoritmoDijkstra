class Heap:
    def __init__(self):
        self.lista = []

    def append(self, item):
        self.lista.append(item)
        aux = len(self.lista) - 1
        pai = (aux + 1) // 2 - 1
        while self.lista[aux] < self.lista[pai] and pai != -1:
            self.lista[aux], self.lista[pai] = self.lista[pai], self.lista[aux]
            aux, pai = pai, ((pai + 1) // 2 - 1)

    def pop(self):
        if self.lista:
            self.lista[0], self.lista[len(self.lista)-1] = self.lista[len(self.lista)-1], self.lista[0]
            no = self.lista.pop()
            pai = 0
            menor = self.menor(pai)
            while menor != -1 and self.lista[menor] < self.lista[pai]:
                self.lista[menor], self.lista[pai] = self.lista[pai], self.lista[menor]
                pai, menor = menor, self.menor(menor)
            return no
        else:
            return None

    def peek(self):
        if self.lista:
            return self.lista[0]
        else:
            return None


    def menor(self, pai):
        i_obj = []
        for i in get_filho(pai):
            if i < len(self.lista):
                i_obj.append(i)

        menor = -1
        for i in i_obj:
            if menor == -1:
                menor = self.lista[i][0]
            if i < menor:
                menor = i

        return menor


def get_filho(num):
    esquerda = ((num + 1) * 2) - 1
    direita = esquerda + 1

    return esquerda, direita


def dijkstra(grafo, origem, fim):

    peso = {}
    for i in grafo:
        peso[i] = float('inf')

    melhores_pais = {}
    for i in grafo:
        melhores_pais[i] = None

    visitados = Heap()

    visitados.append((0, origem))
    peso[origem] = 0

    visited = set()

    while visitados:
        aux_peso, aux = visitados.pop()

        if aux == fim:
            break
        visited.add(aux)
        for pont, distancia in grafo[aux].items():
            novo = peso[aux] + grafo[aux][pont]
            if peso[pont] > novo:
                peso[pont] = novo
                melhores_pais[pont] = aux
                visitados.append((novo, pont))

    if fim in melhores_pais:
        aux = fim
        caminho = [aux]
        while aux in melhores_pais:
            aux = melhores_pais[aux]
            caminho.append(aux)
            if aux == origem:
                return list(reversed(caminho))
    else:
        return