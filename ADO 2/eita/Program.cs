using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace eita {
	class Program {
		static void Main(string[] args) {
            
            System.Threading.Thread.CurrentThread.CurrentCulture = System.Globalization.CultureInfo.GetCultureInfo("en-UK");
            var data = iniciarDataSet();
			data.Embaralhar();
			Console.WriteLine("{0} entradas!",data.entries.Count);
			Console.WriteLine("atributos ({0}):",data.atributos.Length);
			foreach (var atributo in data.atributos) {
				Console.WriteLine("- {0}",atributo);
			}
			Console.WriteLine("resultados ({0}):",data.resultados.Length);
			foreach (var resultado in data.resultados) {
				Console.WriteLine("- {0}",resultado);
			}
			var rede = new RedeNeural(data.atributos.Length,data.resultados.Length,3);
			BackPropagation(rede,data);
			Console.ReadLine();
		}

		static void BackPropagation(RedeNeural rede,DataSet data) {
			double erroAnterior = 1;
			int i = 0;
			while (true) {
				var erroNeuronio = new double[rede.saída.Length];
				foreach (var entry in data.entries) {
					rede.SetarEntrada(entry.atributos);
					rede.PassoForward();
					rede.ObterErroQuadrático(entry.resultados,erroNeuronio);
				}
				double erroTotal = 0;
				for (int a = 0; a < erroNeuronio.Length; a++) {
					erroNeuronio[a] /= erroNeuronio.Length;
					erroTotal += erroNeuronio[a];
				}
				var razão = erroTotal/erroAnterior;
				if (i > 0 && razão < rede.limiar) break;
				Console.WriteLine("iteração #{0}: erro de {1} ({2}/{3})",i,razão,erroTotal,erroAnterior);
				rede.PassoBackward(erroNeuronio);
				erroAnterior = erroTotal;
				i++;
				Console.ReadLine();
			}
			Console.WriteLine("backpropagation terminado após {0} iterações!",i);
		}

        static DataSet iniciarDataSet()
        {
            string caminho = "winequality-white-NORMALIZED/Wine Quality - White - NORMALIZED Table.csv";
            string classe = "quality";

            Console.WriteLine("Selecione um DataSet:");
            Console.WriteLine("1 - Iris");
            Console.WriteLine("2 - Adult");
            Console.WriteLine("3 - Wine");
            Console.WriteLine("4 - Breast Cancer");
            Console.WriteLine("5 - Wine Quality (Red)");
            Console.WriteLine("6 - Wine Quality (White)");
            Console.WriteLine("7 - Abalone");
            int x = Int32.Parse(Console.ReadLine());

            switch (x)
            {
                case 1:
                    return new DataSet("iris-NORMALIZED/Iris - NORMALIZED Table.csv", " Class", true, "iris-NORMALIZED/Iris - Class Label.csv");
                case 2:
                    return null;
                case 3:
                    return new DataSet("wine-NORMALIZED/Wine - NORMALIZED Table.csv", "Alcohol", false);
                case 4:
                    return new DataSet("breast-cancer-NORMALIZED/Breast Cancer Wisconsin - NORMALIZED Table.csv", "Class", false);
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