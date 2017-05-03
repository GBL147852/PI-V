import math

#Constantes#

#Desvio Padrao, ou sigma zero
SIGMA0 = 2
#Tau 1 dado no enunciado
T1 = 3321.92
#eta 0, ou seja, taxa de aprendizado
N0 = 0.1
#Tau 2 dado no enunciado
T2 = 1000
#Raio de vizinhanca do neuronio vencedor
R = 3

#eta n, ou seja, taxa de aprendizado no momento n
def eta(n):
	return N0 * (math.pow( math.e , -n/T2 ))
	
#sigma n, ou seja, desvio padrao no momento n
def sigma(n):
	return SIGMA0 * (math.pow( math.e , n/T1 ))
	
#Retorna a distancia euclidiana 
def distanciaEuclidiana(x, y, dimensions):
    distancia = 0
    for i in range(dimensions):
		distancia += pow((x[i] - y[i]), 2)
    return math.sqrt(distancia)

#Retorna o 	
def h(nx,ny,n):
	expoente = (-((distanciaEuclidiana(nx,ny,2))**2)) / (2 * (sigma(n)**2) )
	return math.pow( math.e , expoente )

#Funcao principal	
def main():
	i = 10000
	A = [2,2]
	B = [90,30]
	print h(A,B,i)
	print eta(0)
	print sigma(0)
	
main()