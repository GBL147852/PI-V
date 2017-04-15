using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace eita {
	/// <summary>
	/// estrutura da camada de conexões da rede neural.
	/// </summary>
	class Conexoes {
		public double this[int a,int b] {
			get => pesos[a,b];
			set => pesos[a,b] = value;
		}

		/// <summary>número de linhas (neurônios na camada atual + bias) na matriz de conexões</summary>
		public int tamanhoI { get; private set; }
		/// <summary>número de colunas (neurônios na próxima camada) na matriz de conexões</summary>
		public int tamanhoJ { get; private set; }

		/// <summary>matriz de pesos</summary>
		double[,] pesos;

		/// <summary>inicializa a camada de conexões.</summary>
		/// <param name="camada0">número de neurônios na camada atual (sem o bias)</param>
		/// <param name="camada1">número de neurônios na próxima camada (sem o bias)</param>
		/// <param name="random">se verdadeiro, seta valores aleatórios de -1 a 1 para os pesos</param>
		public Conexoes(int camada0,int camada1,bool random) {
			tamanhoI = camada0+1;
			tamanhoJ = camada1;
			pesos = new double[tamanhoI,tamanhoJ];
			if (random) {
				var r = new Random((int)DateTime.UtcNow.Ticks);
				for (int a = 0; a < tamanhoI; a++) {
					for (int b = 0; b < tamanhoJ; b++) {
						pesos[a,b] = r.NextDouble()*2-1;
					}
				}
			}
		}
	}
}