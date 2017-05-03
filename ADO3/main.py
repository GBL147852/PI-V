import math

#Constantes#

#Desvio Padrao
DPADRAO = 2
#Tau 1 dado no enunciado
T1 = 3321.92
#eta 0, ou seja, taxa de aprendizado
N0 = 0.1
#Tau 2 dado no enunciado
T2 = 1000
#Raio de vizinhanca do neuronio vencedor
R = 3

#Retorna a distancia euclidiana 
def distanciaEuclidiana(x, y, dimensions):
    distancia = 0
    for i in range(dimensions):
		distancia += pow((x[i] - y[i]), 2)
    return math.sqrt(distancia)

def main():
	A = [2,2]
	B = [3,2]
	print distanciaEuclidiana(A,B,2)
	
main()