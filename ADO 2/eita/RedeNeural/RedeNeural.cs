using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace eita {
	/// <summary>
	/// estrutura da rede neural.
	/// </summary>
	class RedeNeural {
		/// <summary>camada de entrada</summary>
		public Neuronios entrada;
		/// <summary>camada de saída</summary>
		public Neuronios saida;
		
		/// <summary>lista de todas as camadas</summary>
		Neuronios[] neuronios;
		/// <summary>lista de conexões por camada</summary>
		Conexoes[] conexoes;

		/// <summary>inicializa a rede neural.</summary>
		/// <param name="entradas">número de neurônios na entrada</param>
		/// <param name="saidas">número de neurônios na saída</param>
		/// <param name="camadasOcultas">número de camadas ocultas</param>
		/// <param name="neuroniosOcultos">número de neurônios por camada oculta</param>
		public RedeNeural(int entradas,int saidas,int camadasOcultas,int neuroniosOcultos) {
			neuronios = new Neuronios[camadasOcultas+2];
			conexoes = new Conexoes[camadasOcultas+1];
			entrada = neuronios[0] = new Neuronios(entradas);
			saida = neuronios[camadasOcultas+1] = new Neuronios(entradas);
			for (int a = 1; a < camadasOcultas+1; a++) {
				neuronios[a] = new Neuronios(neuroniosOcultos);
			}
			for (int a = 0; a < camadasOcultas+1; a++) {
				conexoes[a] = new Conexoes(neuronios[a].tamanho,neuronios[a+1].tamanho,true);
			}
		}

		/// <summary>inicializa a rede neural.</summary>
		/// <param name="entradas">número de neurônios na entrada</param>
		/// <param name="saidas">número de neurônios na saída</param>
		/// <param name="camadasOcultas">número de camadas ocultas</param>
		public RedeNeural(int entradas,int saidas,int camadasOcultas):
			this(entradas,saidas,camadasOcultas,((entradas > saidas) ? entradas : saidas)*2) {
		}
	}
}