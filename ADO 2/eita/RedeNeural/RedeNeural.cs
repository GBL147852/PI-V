﻿using System;
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
		/// <summary>alpha que dita a velocidade de aprendizado</summary>
		public double momentum = 0;
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
		/// seta valores nos neurônios de entrada.
		/// </summary>
		/// <param name="valores">valores de entrada</param>
		public void SetarEntrada(double[] valores) {
			for (int a = 0; a < entrada.Length && a < valores.Length; a++) {
				entrada[a] = valores[a];
			}
		}

		/// <summary>
		/// obtém o erro quadrático a partir dos neurônios de saída.
		/// </summary>
		/// <param name="valores">valores esperados de saída</param>
		/// <returns>erro quadrático</returns>
		public double ObterErroQuadrático(double[] valores) {
			double eq = 0;
			for (int a = 0; a < saída.Length && a < valores.Length; a++) {
				double e = valores[a]-saída[a];
				eq += e*e;
			}
			return eq/2;
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
		/// realiza o passo backward, utilizando resultados do passo foward e atualizando os pesos até a primeira.
		/// </summary>
		public void PassoBackward(double[] Erros)
        {
            // --- ETAPA BACKWARD CONSIDERANDO A ÚLTIMA CAMADA DE NEURÔNIOS OCULTA  ---
            // --- E A CAMADA DE SAÍDA, ONDE UTILIZAMOS OS ERROS DA CAMADA DE SAÍDA --- 
            //para o primeiro par de camadas adjacentes...
            int con = conexões.Length;
            var neuAtual = neurônios[con];
            var neuAnt = neurônios[con - 1];
            var conexão = conexões[con - 1];
            //e para cada neurônio da camada anterior à de saída ser atualizada...
            for (int ant = 0; ant < neuAnt.Length; ant++)
            {
                //conectado a cada neurônio da camada de saída em si...
                for (int atual = 0; atual < neuAtual.Length; atual++)
                {
                    //pegamos as conexões e atualizamos os pesos...
                    Console.WriteLine("Antes [{0},{0}]: {0}", ant, atual, conexão.pesos[ant, atual]);
                    conexão.pesos[ant, atual] = taxaAprendizado * Erros[atual] * neuAtual[atual] * neuAnt[ant];
                    Console.WriteLine("Depois [{0},{0}]: {0}", ant, atual, conexão.pesos[ant,atual]);
                    
                }
            }

            // --- ETAPA BACKWARD CONSIDERANDO AS OUTRAS CAMADAS DE NEURÔNIOS      ---
            // --- ATÉ CHEGAR À CAMADA DE ENTRADA, UTILIZANDO A MATRIZ DE CONEXÕES ---

            //diminuimos esta dimensão, pois precisamos das demais conexões para chegar ao input layer
            for (; con >= 0; con--)
            {
                neuAtual = neurônios[con];
                neuAnt = neurônios[con - 1];
                conexão = conexões[con - 1];
                //e para cada neurônio da camada anterior à de saída ser atualizada...
                for (int ant = 0; ant < neuAnt.Length; ant++)
                {
                    //conectado a cada neurônio da camada de saída em si...
                    for (int atual = 0; atual < neuAtual.Length; atual++)
                    {
                        //pegamos as conexões e atualizamos os pesos...
                        Console.WriteLine("Antes [{0},{0},{0}]: {0}", ant, atual, conexão.pesos[ant, atual]);
                        conexão.pesos[ant, atual] = conexão.pesos[ant,atual] * neuAtual[atual] * neuAnt[ant];
                        Console.WriteLine("Depois [{0},{0},{0}]: {0}", ant, atual, conexão.pesos[ant, atual]);

                    }
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