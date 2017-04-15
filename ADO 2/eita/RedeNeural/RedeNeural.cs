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
		public double[] entrada;
		/// <summary>camada de saída</summary>
		public double[] saída;

		/// <summary>lista de todas as camadas</summary>
		public double[][] neurônios;
		/// <summary>lista de conexões por camada</summary>
		public Conexões[] conexões;

		/// <summary>parâmetro do sigmoide</summary>
		public double sigmoideA = 1;
		/// <summary>limiar definindo o critério de parada</summary>
		public double limiar = .01;
		/// <summary>taxa de aprendizado para atualização dos pesos</summary>
		public double taxaAprendizado = .01;

		#region construtores

		/// <summary>
		/// inicializa a rede neural.
		/// </summary>
		/// <param name="entradas">número de neurônios na entrada</param>
		/// <param name="saidas">número de neurônios na saída</param>
		/// <param name="camadasOcultas">número de camadas ocultas</param>
		/// <param name="neuroniosOcultos">número de neurônios por camada oculta</param>
		public RedeNeural(int entradas,int saidas,int camadasOcultas,int neuroniosOcultos) {
			neurônios = new double[camadasOcultas+2][];
			conexões = new Conexões[camadasOcultas+1];
			entrada = neurônios[0] = new double[entradas];
			saída = neurônios[camadasOcultas+1] = new double[saidas];
			for (int a = 1; a < camadasOcultas+1; a++) {
				neurônios[a] = new double[neuroniosOcultos];
			}
			for (int a = 0; a < camadasOcultas+1; a++) {
				conexões[a] = new Conexões(neurônios[a].Length,neurônios[a+1].Length,true);
			}
		}

		/// <summary>
		/// inicializa a rede neural.
		/// </summary>
		/// <param name="entradas">número de neurônios na entrada</param>
		/// <param name="saidas">número de neurônios na saída</param>
		/// <param name="camadasOcultas">número de camadas ocultas</param>
		public RedeNeural(int entradas,int saidas,int camadasOcultas):
			this(entradas,saidas,camadasOcultas,((entradas > saidas) ? entradas : saidas)*2) {
		}

		#endregion

		/// <summary>
		/// printa informações sobre o peso de cada conexão.
		/// </summary>
		public void Debug() {
			Console.WriteLine("--");
			for (int a = 0; a < conexões.Length; a++) {
				Console.WriteLine("[conexões camadas #{0} -> #{1}]",a,a+1);
				for (int prox = 0; prox < conexões[a].qtdProx; prox++) {
					Console.WriteLine("neurônio {0}:");
					for (int atual = 0; atual < conexões[a].qtdAtual; atual++) {
						Console.WriteLine("    {0}",conexões[a].pesos[atual,prox]);
					}
				}
			}
			Console.WriteLine("--");
		}

		/// <summary>
		/// realiza o passo forward, utilizando valores da primeira camada e atualizando até a última.
		/// </summary>
		public void PassoForward() {
			//para cada par de camadas adjacentes...
			for (int con = 0; con < conexões.Length; con++) {
				var neuAtual = neurônios[con];
				var neuProx = neurônios[con+1];
				var conexão = conexões[con];
				//e para cada neurônio da camada a ser atualizada...
				for (int prox = 0; prox < neuProx.Length; prox++) {
					double v = 0;
					//soma os neurônios atuais multiplicados pelo peso na matriz de conexão
					for (int atual = 0; atual < neuAtual.Length; atual++) {
						v += conexão.pesos[atual,prox]*neuAtual[atual];
					}
					//soma o peso do bias
					v += conexão.pesos[neuAtual.Length,prox];
					//atribui o valor novo ao próximo neurônio
					neuProx[prox] = Sigmoide(v);
				}
			}
		}

		/// <summary>
		/// função sigmoide.
		/// </summary>
		/// <param name="x">valor x</param>
		/// <returns>resultado da sigmoide</returns>
		public double Sigmoide(double x) {
			return 1/(1+Math.Exp(-x*sigmoideA));
		}
	}
}