using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace eita {
	class Program {
		static void Main(string[] args) {
			var data = new DataSet(
				"wdbc-NORMALIZED/WDBC - NORMALIZED Table.csv",
				"diagnosis",true,
				"wdbc-NORMALIZED/WDBC - Class Label.csv"
			);
			data.Embaralhar();
			Console.WriteLine("{0} entradas!",data.entries.Count);
			Console.WriteLine("atributos ({0}):",data.atributos.Length);
			foreach (var atributo in data.atributos) {
				Console.WriteLine("- {0}",atributo);
			}
			if (data.usandoClasses) {
				Console.WriteLine("classes ({0}):",data.classes.Count);
				foreach (var classe in data.classes) {
					Console.WriteLine("- {0} ({1})",classe.Key,classe.Value);
				}
			}
			var rede = new RedeNeural(data.atributos.Length,data.usandoClasses ? data.classes.Count : 1,3);
			int i = 0;
			int padding;
			if (data.usandoClasses) {
				padding = data.classes.Values.Aggregate("",(x,y) => (x.Length > y.Length) ? x : y).Length;
			} else {
				padding = 0;
			}
			while (true) {
				Console.ReadLine();
				if (i >= data.entries.Count) continue;
				for (int a = 0; a < rede.entrada.Length; a++) {
					rede.entrada[a] = data.entries[i].atributos[a];
				}
				rede.PassoForward();
				if (data.usandoClasses) {
					int b = 0;
					foreach (var classe in data.classes) {
						Console.WriteLine("{0} / D: {1} / Y: {2}",
							classe.Value.PadRight(padding),
							(classe.Key == data.entries[i].classeEsperada) ? 1 : 0,
							rede.saída[b++]
						);
					}
				} else {
					Console.Write("D: {0} / Y: {1}",data.entries[i].decimalEsperado,rede.saída[0]);
				}
				i++;
			}
		}
	}
}