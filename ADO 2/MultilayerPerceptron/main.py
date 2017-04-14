import math
import random
import operator
import csv

BIAS = 1


# Carrega os dados a partir de um arquivo csv
def carregardados(nomebase):
    with open("../datasets/"+nomebase+" - NORMALIZED Table.csv", 'r') as csvfile:

        # Puxa todos os dados
        lines = csv.reader(csvfile)
        dataset = list(lines)[1:]
        for x in range(len(dataset)):
            for y in range(len(dataset[x])):
                dataset[x][y] = float(dataset[x][y])

    return dataset


def main():
    dataset = carregardados("abalone-NORMALIZED/Abalone")
    print(dataset)
    print("Oi")


main()