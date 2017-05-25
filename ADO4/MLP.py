import random
import math
import random
import csv
import os


class Conexoes():
    def __init__(self, camadax, camaday, aleatorizar = True):
        self.qtdAtual = camadax + 1
        self.qtdProx = camaday
        self.pesos = [[random.uniform(0,1) for y in range(qtdProx)] for x in range(qtdAtual)]



class RedeNeural():
    sigmoideA = 1
    limiar = 0.01
    momentum = 0
    taxaAprendizado = 0.01


    def __init__(self, entradas, saidas, camadasOcultas, neuroniosOcultos):
        self.neuronios = [[]for x in range(camadasOcultas+2)]
        self.conexoes = [Conexoes()] * (camadasOcultas+1)
        self.neuronios[0] = [] * entradas
        self.entrada = self.neuronios[0]
        self.neuronios[camadasOcultas+1] = [] * saidas
        self.saida = self.neuronios[camadasOcultas+1]
        for i in range (1,camadasOcultas+1):
            self.neuronios[i] = [] * neuroniosOcultos;
        for i in range (1,camadasOcultas+1):
            self.conexoes[i] = Conexoes(self.neuronios[i].Length, self.neuronios[a+1].Length, True)

    def __init__(self, entradas, saidas, camadasOcultas):
        if entradas > saidas:
            a = entradas
        else:
            a = saidas
        this(entradas, saidas, camadasOcultas, a * 2)

    def Sigmoide(self, x):
        return 1 / (1 + math.exp(-x * self.sigmoideA))

    def SigmoideDeriv(self, x):
        return (math.exp(-x) / math.pow((1+math.exp(-x*sigmoideA)), 2))


    def Debug(self):
        print "--"
        for a in range (0,self.conexoes.Length):
            print "[conexoes camadas ", a, " -> ", (a+1)
            for prox in range (0,self.conexoes[a].qtdProx):
                print "neuronio ", prox, ":"
                for atual in range (0, self.conexoes[a].qtdAtual):
                    print self.conexoes[a].pesos[atual,prox]
        print "--"


    def SetarEntrada(self, valores = []):
        a = 0
        while True:
            if a < entrada.Length and a < valores.Length:
                entrada[a] = valores[a]
            else:
                break
            a += 1


    def ObterErroQuadratico(self, valores = [], output = []):
        while True:
            if a < output.Length and a < valores.Length and a < self.saida.Length:
                e = valores[a] - self.saida[a]
                output[a] += e*e/2
            else:
                break
            a += 1

    def ObterErroAbsoluto(self, valores = [], output = []):
        while True:
            if a < output.Length and a < valores.Length and a < self.saida.Length:
                output[a] += math.abs(valores[a] - self.saida[a])
            else:
                break
            a += 1

    def ObterErroQuadratico(self, valores = []):
        output = [] * valores.Length
        ObterErroQuadratico(valores, output)
        return output

    def ObterErroAbsoluto(self, valores = []):
        output = [] * valores.Length
        ObterErroAbsoluto(valores, output)
        return output


    def PassoForward(self):
        for con in range(0,self.conexoes.Length):
            neuAtual = self.neuronios[con]
            neuProx = self.neuronios[con+1]
            conexao = self.conexoes[con]
            for prox in range(0, neuProx.Length):
                v = 0
                for atual in range(0, neuAtual.Length):
                    v += conexao.pesos[atual,prox]*neuAtual[atual]
                v += conexao.pesos[neuAtual.Length,prox]
                neuProx[prox] = Sigmoide(v)

    def PassoBackward(self, Erros = []):
        con = self.conexoes.Length
        neuAtual = self.neuronios[con]
        neuAnt = self.neuronios[con-1]
        conexao = self.conexoes[con-1]
        
        for ant in range (0, neuAnt.Length):
            for atual in range (0, neuAtual.Length):
                self.conexoes.pesos[ant,atual] = self.taxaAprendizado * Erros[atual] * neuAtual[atual] * neuAnt[ant]

        for x in range (con,0,-1):
            neuAtual = self.neuronios[con]
            neuAnt = self.neuronios[con-1]
            conexao = self.conexoes[con-1]
            for ant in range (0, neuAnt.Length):
                for atual in range (0, neuAtual.Length):
                    self.conexao.pesos[ant, atual] = SigmoideDeriv(neuAtual[atual]) * conexao.pesos[ant,atual] * neuAtual[atual] * neuAnt[ant]

    def Testar(self, entrada = []):
        SetarEntrada(entrada)
        PassoForward()
        return self.saida;


def LoadDataSet(path):
    data = []
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'data/'+path+'.csv')
    
    with open(filename) as csvfile:
        r = csv.reader(csvfile)
        firstRow = True
        for row in r:
            if firstRow:
                firstRow = False
            else:
                data.append(list(map(float,row)))
                
    random.shuffle(data)
    return data