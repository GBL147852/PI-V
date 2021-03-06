﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace eita {
	class Program {
		static void Main(string[] args) {

            System.Threading.Thread.CurrentThread.CurrentCulture = System.Globalization.CultureInfo.GetCultureInfo("en-UK");
			while (true) {
				Console.Clear();
				var data = iniciarDataSet();
				data.Embaralhar();
				RodarDataSet(data);
				Console.WriteLine("pressione enter para recomeçar...");
				Console.ReadLine();
			}
		}

		static int[] topologias = {
			2,	3,
			2,	5,
			3,	10,
		};
		const int partições = 10;

		static void RodarDataSet(DataSet data) {
			var entries = new List<DataSetEntry>[partições*2];
			for (int p = 0; p < partições; p++) {
				int start = (int)((double)data.entries.Count*p/partições);
				int end = (int)((double)data.entries.Count*(p+1)/partições);
				entries[p*2] = new List<DataSetEntry>(); //90%
				entries[p*2+1] = new List<DataSetEntry>(); //10%
				for (int a = 0; a < data.entries.Count; a++) {
					if (a >= start && a < end) {
						entries[p*2+1].Add(data.entries[a]);
					} else {
						entries[p*2].Add(data.entries[a]);
					}
				}
			}
			int melhorTopologia = 0;
			double melhorClassificação = 0;
			int[,] melhorMatriz = null;
			for (int t = 0; t < topologias.Length; t += 2) {
				int camadasOcultas = topologias[t];
				int neuroniosOcultos = topologias[t+1];
				double classificaçõesCorretasMédias = 0;
				double erroAbsolutoMédio = 0;
				double erroQuadráticoMédio = 0;
				var matrizDeConfusão = new int[data.resultados.Length,data.resultados.Length];
				for (int p = 0; p < partições; p++) {
					var rede = new RedeNeural(data.atributos.Length,data.resultados.Length,camadasOcultas,neuroniosOcultos);
					PassoTreinamento(rede,entries[t*2]);
					double classificaçõesCorretas = 0;
					double erroAbsoluto = 0;
					double erroQuadrático = 0;
					foreach (var entry in entries[t*2+1]) {
						var teste = rede.Testar(entry.atributos);
						var esperado = entry.resultados;
						int atingido = 0;
						int correto = 0;
						double atingidoMax = 0;
						for (int b = 0; b < teste.Length; b++) {
							if (atingidoMax < teste[b]) {
								atingidoMax = teste[b];
								atingido = b;
							}
							if (esperado[b] > .5) {
								correto = b;
							}
						}
						if (correto == atingido) {
							classificaçõesCorretas++;
						}
						matrizDeConfusão[atingido,correto]++;
						erroAbsoluto += rede.ObterErroAbsoluto(esperado).Sum();
						erroQuadrático += rede.ObterErroQuadrático(esperado).Sum();
					}
					int testes = entries[t*2+1].Count;
					classificaçõesCorretasMédias += classificaçõesCorretas/testes;
					erroAbsolutoMédio += erroAbsoluto/testes;
					erroQuadráticoMédio += Math.Sqrt(erroQuadrático/testes);
				}
				erroAbsolutoMédio /= partições;
				erroQuadráticoMédio /= partições;
				classificaçõesCorretasMédias /= partições;
				Console.WriteLine();
				Console.WriteLine("TOPOLOGIA {2}: {0} camadas ocultas, com {1} neurônios em cada",camadasOcultas,neuroniosOcultos,t/2);
				Console.WriteLine("classificações corretas: {0:F6}%",classificaçõesCorretasMédias*100);
				Console.WriteLine("erro absoluto médio: {0:F6}",erroAbsolutoMédio*100);
				Console.WriteLine("erro quadrático médio: {0:F6}",erroQuadráticoMédio);
				Console.WriteLine();
				if (melhorClassificação <= classificaçõesCorretasMédias) {
					melhorClassificação = classificaçõesCorretasMédias;
					melhorTopologia = t;
					melhorMatriz = matrizDeConfusão;
				}
			}
			Console.WriteLine();
			Console.WriteLine("MATRIZ DE CONFUSÃO para a topologia {0}:",melhorTopologia/2);
			Console.WriteLine("(linhas: atingido; colunas: esperado)");
			for (int i = 0; i < data.resultados.Length; i++) {
				for (int j = 0; j < data.resultados.Length; j++) {
					if (j > 0) Console.Write(" / ");
					Console.Write("{0,-2:F0}",melhorMatriz[i,j]);
				}
				Console.WriteLine();
			}
			Console.WriteLine();
			Console.WriteLine("fim!!");
		}

		static void PassoTreinamento(RedeNeural rede,IEnumerable<DataSetEntry> entries) {
			int i = 0;
			double erroAnterior = 0;
			while (true) {
				var erroNeuronio = new double[rede.saída.Length];
				int entryCount = 0;
				foreach (var entry in entries) {
					entryCount++;
					rede.SetarEntrada(entry.atributos);
					rede.PassoForward();
					rede.ObterErroQuadrático(entry.resultados,erroNeuronio);
				}
				double erroTotal = 0;
				for (int a = 0; a < erroNeuronio.Length; a++) {
					erroNeuronio[a] /= entryCount;
					erroTotal += erroNeuronio[a];
				}
				erroTotal /= rede.saída.Length;
				if (i > 0 && Math.Abs(erroAnterior-erroTotal) < rede.limiar) break;
				erroAnterior = erroTotal;
				rede.PassoBackward(erroNeuronio);
				i++;
			}
		}

        static DataSet iniciarDataSet()
        {
            Console.WriteLine("Selecione um DataSet:");
            Console.WriteLine("1 - Iris");
            Console.WriteLine("2 - Adult");
            Console.WriteLine("3 - Wine");
            Console.WriteLine("4 - Breast Cancer");
            Console.WriteLine("5 - Wine Quality (Red)");
            Console.WriteLine("6 - Wine Quality (White)");
            Console.WriteLine("7 - Abalone");
			int x;
			while (!int.TryParse(Console.ReadLine(),out x));
            switch (x)
            {
                case 1:
                    return new DataSet("iris-NORMALIZED/Iris - NORMALIZED Table.csv", " Class", true, "iris-NORMALIZED/Iris - Class Label.csv");
                case 2:
                    return new DataSet("adult-NORMALIZED/Adult - NORMALIZED Table.csv", "Class", false);
                case 3:
                    return new DataSet("wine-NORMALIZED/Wine - NORMALIZED Table.csv", "Alcohol", false);
                case 4:
                    return new DataSet("breast-cancer-NORMALIZED/Breast Cancer Winsconsin - NORMALIZED Table.csv", "Class", false);
                case 5:
                    return new DataSet("winequality-red-NORMALIZED/Wine Quality - Red - NORMALIZED Table.csv", "Alcohol", false);
                case 6:
                    return new DataSet("winequality-white-NORMALIZED/Wine Quality - White - NORMALIZED Table.csv", "Alcohol", false);
                case 7:
                    return new DataSet("abalone-NORMALIZED/Abalone - NORMALIZED Table.csv", "Sex", true, "abalone-NORMALIZED/Abalone - Class Label.csv");
                default:
                    return null;
            }

        }
	}
}
