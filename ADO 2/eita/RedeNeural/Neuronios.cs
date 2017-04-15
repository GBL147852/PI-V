using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace eita {
	/// <summary>
	/// estrutura da camada de neurônios da rede neural.
	/// </summary>
	class Neuronios {
		/// <summary>tamanho da camada, desconsiderando a dimensão extra do bias (último elemento)</summary>
		public int tamanho => valores.Length;

		public double this[int index] {
			get {
				if (index == tamanho) return 1;
				return valores[index];
			}
			set {
				if (index == tamanho) return;
				valores[index] = value;
			}
		}

		/// <summary>lista de valores</summary>
		double[] valores;

		public Neuronios(int n) {
			valores = new double[n];
		}
	}
}