using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace eita {
	/// <summary>
	/// estrutura da camada de conexões da rede neural.
	/// </summary>
	class Conexões {
		/// <summary>número de linhas (neurônios na camada atual + bias) na matriz de pesos</summary>
		public int qtdAtual { get; private set; }
		/// <summary>número de colunas (neurônios na próxima camada) na matriz de pesos</summary>
		public int qtdProx { get; private set; }
		/// <summary>matriz de pesos</summary>
		public double[,] pesos { get; private set; }

		/// <summary>inicializa a camada de conexões.</summary>
		/// <param name="camada0">número de neurônios na camada atual (sem o bias)</param>
		/// <param name="camada1">número de neurônios na próxima camada (sem o bias)</param>
		/// <param name="aleatorizar">se verdadeiro, gera valores aleatórios de -1 a 1 para os pesos</param>
		public Conexões(int camada0,int camada1,bool aleatorizar = true) {
			qtdAtual = camada0+1;
			qtdProx = camada1;
			pesos = new double[qtdAtual,qtdProx];
			if (aleatorizar) GerarPesosAleatórios();
		}

		/// <summary>
		/// gera valores aleatórios de -1 a 1 para os pesos.
		/// </summary>
		public void GerarPesosAleatórios() {
			var geradorRandom = new Random((int)DateTime.UtcNow.Ticks);
			for (int atual = 0; atual < qtdAtual; atual++) {
				for (int prox = 0; prox < qtdProx; prox++) {
					pesos[atual,prox] = geradorRandom.NextDouble()*2-1;
				}
			}
		}
	}
}