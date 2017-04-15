using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace eita {
	class Program {
		static void Main(string[] args) {
			var rede = new RedeNeural(3,5,3);
			rede.Debug();
			while (true) {
				Console.Write("[entrada] ");
				var asd = Console.ReadLine().Split(',');
				int i = 0;
				for (int a = 0; a < asd.Length && i < rede.entrada.Length; a++) {
					if (double.TryParse(asd[a].Trim(),out double n)) {
						rede.entrada[i++] = n;
					}
				}
				if (i < rede.entrada.Length) continue;
				rede.PassoForward();
				Console.WriteLine("[saída] {0}",string.Join(", ",rede.saida));
			}
		}
	}
}