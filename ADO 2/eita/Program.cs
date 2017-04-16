using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace eita {
	class Program {
		static void Main(string[] args) {
			System.Threading.Thread.CurrentThread.CurrentCulture = System.Globalization.CultureInfo.GetCultureInfo("en-UK");
			var data = new DataSet(
				"winequality-white-NORMALIZED/Wine Quality - White - NORMALIZED Table.csv",
				"quality",false
			);
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
			int i = 0;
			int padding = data.resultados.Aggregate("",(x,y) => (x.Length > y.Length) ? x : y).Length;
			while (true) {
				Console.ReadLine();
				if (i >= data.entries.Count) continue;
				var entry = data.entries[i++];
				for (int a = 0; a < rede.entrada.Length; a++) {
					rede.entrada[a] = entry.atributos[a];
				}
				rede.PassoForward();
				for (int a = 0; a < data.resultados.Length; a++) {
					Console.WriteLine("{0} / D: {1} / Y: {2}",
						data.resultados[a].PadRight(padding),
						entry.resultados[a],
						rede.saída[a]
					);
				}
			}
		}

		static void BackPropagation() {
			//
		}
	}
}