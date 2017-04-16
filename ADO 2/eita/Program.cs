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
			BackPropagation(rede,data);
			Console.ReadLine();
		}

		static void BackPropagation(RedeNeural rede,DataSet data) {
			double e = 0;
			foreach (var entry in data.entries) {
				rede.SetarEntrada(entry.atributos);
				rede.PassoForward();
				e += rede.ObterErroQuadrático(entry.resultados);
			}
			e /= data.entries.Count;
			Console.WriteLine("erro: {0}",e);
		}
	}
}