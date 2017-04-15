using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace eita {
	class RedeNeural {
		public Camada entrada,saida;
		
		Camada[] camadas;
		Conexao[] conexoes;

		public RedeNeural(int entradas,int saidas,int camadasOcultas,int nos) {
			camadas = new Camada[camadasOcultas+2];
			conexoes = new Conexao[camadasOcultas+1];
			entrada = camadas[0] = new Camada(entradas);
			saida = camadas[camadasOcultas+1] = new Camada(entradas);
			for (int a = 1; a < camadasOcultas+1; a++) {
				camadas[a] = new Camada(nos);
			}
			for (int a = 0; a < camadasOcultas+1; a++) {
				conexoes[a] = new Conexao(camadas[a].tamanho,camadas[a+1].tamanho,true);
			}
		}
		
		public RedeNeural(int entradas,int saidas,int camadasOcultas):
			this(entradas,saidas,camadasOcultas,((entradas > saidas) ? entradas : saidas)*2) {
		}
	}
	
	class Camada {
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
		
		double[] valores;
		
		public Camada(int n) {
			valores = new double[n];
		}
	}
	
	class Conexao {
		public double this[int a,int b] {
			get => pesos[a,b];
			set => pesos[a,b] = value;
		}
		public int tamanhoI { get; private set; }
		public int tamanhoJ { get; private set; }
		
		double[,] pesos;
		
		public Conexao(int camada0,int camada1,bool random) {
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