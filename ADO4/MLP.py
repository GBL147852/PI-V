import random
import math
import random
import csv
import os


class Conexoes():
    def __init__(self, camadax, camaday, aleatorizar = True):
        self.qtdAtual = camadax + 1
        self.qtdProx = camaday
        self.pesos = [[random.uniform(0,1) for y in range(self.qtdProx)] for x in range(self.qtdAtual)]


class RedeNeural():
    sigmoideA = 1
    limiar = 0.01
    momentum = 0
    taxaAprendizado = 0.01
    count = 1
    erroQuadMedio = 0
    erroQuadMedioAnt = 0

    def __init__(self, entradas, saidas, camadasOcultas, hiddenNeurons):
        self.neuronios = [[0]for x in range(camadasOcultas+2)]
        self.conexoes = [0] * (camadasOcultas+1)
        self.neuronios[0] = [0] * entradas
        self.entrada = self.neuronios[0]
        self.neuronios[camadasOcultas+1] = [0] * saidas
        self.saida = self.neuronios[camadasOcultas+1]
        for i in range (1,camadasOcultas+1):
            self.neuronios[i] = [0] * hiddenNeurons;
        for i in range (0,camadasOcultas+1):
            self.conexoes[i] = Conexoes(camadax=len(self.neuronios[i]), camaday=len(self.neuronios[i+1]), aleatorizar=True)

    def Sigmoide(self, x):
        return 1 / (1 + math.exp(-x * self.sigmoideA))

    def SigmoideDeriv(self, x):
        return (math.exp(-x) / math.pow((1+math.exp(-x*self.sigmoideA)), 2))


    def Debug(self):
        print "--"
        for a in range (0,len(self.conexoes)):
            print "[conexoes camadas ", a, " -> ", (a+1)
            for prox in range (0,self.conexoes[a].qtdProx):
                print "neuronio ", prox, ":"
                for atual in range (0, self.conexoes[a].qtdAtual):
                    print self.conexoes[a].pesos[atual][prox]
        print "--"


    def SetarEntrada(self, valores = []):
        a = 0
        while True:
            if a < len(self.entrada) and a < len(valores):
                self.entrada[a] = valores[a]
            else:
                break
            a += 1


    def ObterErroQuadratico(self, valores = []):
        a = 0
        output = 0
        while True:
            if a < len(valores) and a < len(self.saida):
                e = valores[a] - self.saida[a]
                output += e*e/2
            else:
                break
            a += 1
        return output

    def ObterErroAbsoluto(self, valores = []):
        a = 0
        output = [0] * len(valores)
        while True:
            if a < len(valores) and a < len(self.saida):
                e = valores[a] - self.saida[a]
                output[a] = e
            else:
                break
            a += 1
        return output

    def ErroQuadraticoMedio(self, erroQuadratico):
        self.erroQuadMedio *= self.count
        self.erroQuadMedio += erroQuadratico
        self.count += 1
        self.erroQuadMedio /= self.count
        return self.erroQuadMedio

    def PassoForward(self):
        for con in range(0,len(self.conexoes)):
            neuAtual = self.neuronios[con]
            neuProx = self.neuronios[con+1]
            conexao = self.conexoes[con]
            for prox in range(0, len(neuProx)):
                v = 0
                for atual in range(0, len(neuAtual)):
                    v += conexao.pesos[atual][prox]*neuAtual[atual]
                v += conexao.pesos[len(neuAtual)][prox]
                neuProx[prox] = self.Sigmoide(v)
        
    def Teste(self, inputs = [], valores = []):
        self.SetarEntrada(inputs)
        self.PassoForward()
        classeObtida = self.saida.index(max(self.saida))
        classeEsperada = valores.index(max(valores))
        if classeObtida == classeEsperada:
            return 1
        else:
            return 0

    def PassoBackward(self, Erro = []):
        con = len(self.conexoes)
        neuAtual = self.neuronios[con]
        neuAnt = self.neuronios[con-1]
        conexao = self.conexoes[con-1]
        deltaAnt = 0
        deltaAtual = 0
        
        
        for ant in range (0, len(neuAnt)):
            for atual in range (0, len(neuAtual)):
                deltaAnt += Erro[atual] * self.SigmoideDeriv(x = neuAtual[atual]) * conexao.pesos[ant][atual]
                conexao.pesos[ant][atual] += self.taxaAprendizado * (Erro[atual] * self.SigmoideDeriv(x = neuAtual[atual])) * neuAnt[ant]


        for x in range (con-1,0,-1):
            neuAtual = self.neuronios[x]
            neuAnt = self.neuronios[x-1]
            conexao = self.conexoes[x-1]
            for ant in range (0, len(neuAnt)):
                for atual in range (0, len(neuAtual)):
                    deltaAtual += self.SigmoideDeriv(x = neuAtual[atual]) * deltaAnt * conexao.pesos[ant][atual]
                    conexao.pesos[ant][atual] += self.taxaAprendizado * (self.SigmoideDeriv(x = neuAtual[atual]) * deltaAnt) * neuAnt[ant]
            deltaAnt = deltaAtual
            deltaAtual = 0


        


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

data = LoadDataSet("wine")
treinamento = data[:(len(data)*9/10)]
teste = data[(len(data)*9/10):]

classes = 3
inputs = len(data[0])-1
print len(data), "entradas"
rede = RedeNeural(entradas=inputs, saidas=classes, camadasOcultas=classes, hiddenNeurons=classes)

#Treinamento
while(True):
    for entrada in treinamento:
        esperado = [0] * classes
        esperado[(int(entrada[0]))-1] = 1
        rede.SetarEntrada(valores = entrada[1:])
        rede.PassoForward()
        rede.PassoBackward(rede.ObterErroAbsoluto(valores = esperado))
    rede.count += 1
    rede.erroQuadMedioAnt = rede.erroQuadMedio
    rede.erroQuadMedio = rede.ErroQuadraticoMedio(rede.ObterErroQuadratico(valores = esperado))
    print "|", rede.erroQuadMedio, " - ", rede.erroQuadMedioAnt, "| = ", abs(rede.erroQuadMedioAnt - rede.erroQuadMedio)
    if(abs(rede.erroQuadMedioAnt - rede.erroQuadMedio) < rede.limiar):
        break

quantAcertos = 0
#Teste
for entrada in teste:
    esperado = [0] * classes
    esperado[(int(entrada[0]))-1] = 1    
    quantAcertos += rede.Teste(inputs = entrada, valores = esperado)
print (float(quantAcertos) / float(len(teste)))*100.0 , "% belezinha"


raw_input()