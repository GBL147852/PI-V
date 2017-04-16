using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace eita {
	class DataSet {
		/// <summary>nomes dos atributos do dataset</summary>
		public string[] atributos { get; private set; }
		/// <summary>nomes dos resultados do dataset</summary>
		public string[] resultados { get; private set; }
		/// <summary>entries do dataset</summary>
		public List<DataSetEntry> entries { get; private set; }

		/// <summary>caminho padrão para os datasets</summary>
		const string caminhoBase = "../../../datasets/";
		/// <summary>separador do .csv</summary>
		static char[] sep = new char[] {','};

		#region construtor

		/// <summary>
		/// inicializa o dataset, lendo os dados de arquivos .csv especificados.
		/// </summary>
		/// <param name="caminho">caminho para o dataset</param>
		/// <param name="atributoResultado">atributo a ser utilizado como resultado</param>
		/// <param name="usandoClasses">se verdadeiro, o resultado esperado é uma classe. caso contrário, é decimal</param>
		/// <param name="caminhoLabel">caminho para as labels das classes, se houver</param>
		public DataSet(string caminho,string atributoResultado,bool usandoClasses,string caminhoLabel = "") {
			atributos = resultados = new string[0];
			entries = new List<DataSetEntry>();
			var classes = new Dictionary<string,string>();
			var vazio = new double[0];
			var listaClasses = new List<string>();
			if (usandoClasses) {
				if (caminhoLabel.Length > 0) {
					try {
						using (var file = new StreamReader(new FileStream(caminhoBase+caminhoLabel,FileMode.Open,FileAccess.Read))) {
							string line;
							while ((line = file.ReadLine()) != null) {
								var l = line.Split(sep);
								if (l.Length >= 2 && !string.IsNullOrWhiteSpace(l[0]) && !string.IsNullOrWhiteSpace(l[1])) {
									classes[l[1].Trim()] = l[0].Trim();
								}
							}
						}
					} catch (Exception e) {
						Console.WriteLine("AVISO: não foi possível ler as labels!");
						Console.WriteLine(e);
					}
				}
			} else {
				resultados = new string[] { atributoResultado };
			}
			try {
				var classesEncontradas = new HashSet<string>();
				using (var file = new StreamReader(new FileStream(caminhoBase+caminho,FileMode.Open,FileAccess.Read))) {
					var l = file.ReadLine().Split(sep);
					int n = l.Length;
					if (n < 2) throw new Exception("o .csv deve ter no mínimo 2 colunas");
					atributos = new string[n-1];
					int atributoIndex = -1;
					atributoResultado = atributoResultado.Trim();
					int i = 0;
					for (int a = 0; a < n; a++) {
						var atr = l[a].Trim();
						if (atributoIndex < 0 && string.Compare(atributoResultado,atr,StringComparison.InvariantCultureIgnoreCase) == 0) {
							atributoIndex = a;
							continue;
						}
						if (i < n-1) atributos[i++] = atr;
					}
					if (atributoIndex < 0) throw new Exception("atributo de resultado não encontrado");
					string line;
					while ((line = file.ReadLine()) != null) {
						l = line.Split(sep);
						if (l.Length < n) continue;
						var atributos = new double[n-1];
						var resultados = vazio;
						bool entryVálida = true;
						i = 0;
						for (int a = 0; a < n; a++) {
							if (a == atributoIndex) {
								if (usandoClasses) {
									var s = l[a].Trim();
									listaClasses.Add(s);
									classesEncontradas.Add(s);
								} else if (double.TryParse(l[a],out double v)) {
									resultados = new double[] { v };
								} else {
									entryVálida = false;
									break;
								}
							} else if (double.TryParse(l[a],out double v)) {
								atributos[i++] = v;
							} else {
								entryVálida = false;
								break;
							}
						}
						if (!entryVálida) continue;
						entries.Add(new DataSetEntry {
							atributos = atributos,
							resultados = resultados,
						});
					}
				}
				if (usandoClasses) {
					foreach (var classe in classesEncontradas) {
						if (!classes.ContainsKey(classe)) {
							classes[classe] = classe;
						}
					}
				}
			} catch (Exception e) {
				atributos = resultados = new string[0];
				entries.Clear();
				Console.WriteLine("ERRO: não foi possível ler o dataset!");
				Console.WriteLine(e);
				return;
			}
			if (usandoClasses) {
				var classesIndex = new Dictionary<string,int>();
				int i = 0;
				foreach (var classe in classes) {
					classesIndex[classe.Key] = i++;
				}
				resultados = classes.Values.ToArray();
				for (int a = 0; a < entries.Count; a++) {
					var res = new double[classes.Count];
					int index = classesIndex[listaClasses[a]];
					for (int b = 0; b < classes.Count; b++) {
						res[b] = (b == index) ? 1 : 0;
					}
					entries[a] = new DataSetEntry {
						atributos = entries[a].atributos,
						resultados = res,
					};
				}
			}
		}

		#endregion

		/// <summary>
		/// embaralha todas as entries do dataset.
		/// </summary>
		public void Embaralhar() {
			var random = new Random((int)DateTime.UtcNow.Ticks);
			entries.Sort((x,y) => (random.NextDouble() > .5) ? 1 : -1);
		}
	}

	/// <summary>
	/// estrutura de entradas disponíveis no dataset.
	/// </summary>
	struct DataSetEntry {
		/// <summary>atributos de input</summary>
		public double[] atributos;
		/// <summary>resultados esperados de output</summary>
		public double[] resultados;
	}
}