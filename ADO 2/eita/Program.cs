using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace eita {
	class Program {
		static void Main(string[] args) {
            
            System.Threading.Thread.CurrentThread.CurrentCulture = System.Globalization.CultureInfo.GetCultureInfo("en-UK");
            var data = iniciarDataSet() ;
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
            double e = 0;
			foreach (var entry in data.entries) {
				rede.SetarEntrada(entry.atributos);
				rede.PassoForward();
                rede.PassoBackward(rede.ObterErroQuadrático(entry.resultados));
                e += rede.ObterErroQuadráticoSomatória(entry.resultados);
			}
			e /= data.entries.Count;
			Console.WriteLine("erro: {0}",e);
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
                    break;
                case 2:
                    return new DataSet("adult-NORMALIZED/Adult - NORMALIZED Table.csv", "Class", false);
                    break;
                case 3:
                    return new DataSet("wine-NORMALIZED/Wine - NORMALIZED Table.csv", "Alcohol", false);
                    break;
                case 4:
                    return new DataSet("breast-cancer-NORMALIZED/Breast Cancer Wisconsin - NORMALIZED Table.csv", "Class", false);
                    break;
                case 5:
                    return new DataSet("winequality-red-NORMALIZED/Wine Quality - Red - NORMALIZED Table.csv", "Alcohol", false);
                    break;
                case 6:
                    return new DataSet("winequality-white-NORMALIZED/Wine Quality - White - NORMALIZED Table.csv", "Alcohol", false);
                    break;
                case 7:
                    return new DataSet("abalone-NORMALIZED/Abalone - NORMALIZED Table.csv", "Sex", true, "abalone-NORMALIZED/Abalone - Class Label.csv");
                    break;
                default:
                    return null;
                    break;
            }
            
        }
	}
}