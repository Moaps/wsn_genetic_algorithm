######################################################################
#
# Trabalho realizado para nota na matéria Inteligência Artificial 2
# Docente: Luis Fernando de Almeida
# Discentes:    Clariana Costa  -  RA: 10112363
#               Lara Marques    -  RA: 10102584
#
######################################################################
 
import os
import sys
import customtkinter
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from problema import Problema
from algoritmo_genetico import AlgoritmoGenetico
 
######################################################################
 
'''
 
    Parâmetros do algoritmo genético
 
'''
tamanho_populacao = 10
taxa_cruzamento = 0.3
taxa_mutacao = 0
num_geracoes = 20
 
'''
 
    Configurando o Tema e Modo de Aparência
 
'''
customtkinter.set_default_color_theme("green")
customtkinter.set_appearance_mode("system")
 
'''
 
    A Classe 'App' é responsável por inicializar o programa e prover a GUI ao usuário
 
'''
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Network AG")
 
        # Define o caminho correto para as imagens
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS # Caminho para aplicações empacotadas
        else:
            base_path = os.path.dirname(os.path.abspath(__file__)) # Caminho do diretório atual
 
        image_path = os.path.join(base_path, "images") # Diretório das imagens
 
        # Verifica se o arquivo de ícone existe
        icon_path = os.path.join(image_path, "app_logo.ico")
        if not os.path.exists(icon_path):
            messagebox.showerror("Erro", f"Ícone não encontrado: {icon_path}")
            sys.exit(1)
 
        self.wm_iconbitmap(icon_path) # Define o ícone da janela
        self.iconapp = ImageTk.PhotoImage(file=os.path.join(image_path, "app_logo_2.png"))
        self.iconphoto(False, self.iconapp) # Define a imagem do aplicativo
 
        # Centralizar a janela na tela
        self.update_idletasks()
        self.wm_attributes('-fullscreen', True)
        self.state('normal')
        #width = 1000
        #height = 1100
        #x = (self.winfo_screenwidth() // 2) - (width // 2)
        #y = (self.winfo_screenheight() // 2) - (height // 2)
        #self.geometry(f"{width}x{height}+{x}+{y}") # Define o tamanho e a posição da janela
 
        # Carregar a imagem com suporte para modos claro e escuro
        self.logo_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "robologo_light.png")),
            dark_image=Image.open(os.path.join(image_path, "robologo_dark.png")), size=(100, 100))
 
        # Criação do frame principal
        self.main_page = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_page.grid(row=0, column=0, sticky="nsew")
 
        # Configuração das linhas e colunas do grid no frame principal
        self.main_page.grid_rowconfigure([0, 1, 2, 3, 4], weight=1)  # The row for the label should not expand
        self.main_page.grid_columnconfigure(0, weight=1)  # The row for the label should not expand
        self.columnconfigure(0, weight=1)
 
        # Título do App
        self.nf_title = customtkinter.CTkLabel(self.main_page, text="Inteligência Artificial II",
                                               font=customtkinter.CTkFont(size=32, weight="bold"))
        self.nf_title.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="n")
 
        # Subtítulo do App
        self.nf_subtitle = customtkinter.CTkLabel(self.main_page, text="8º Semestre de Engenharia de Computação\nUNITAU",
                                                  font=customtkinter.CTkFont(size=14, weight="normal"))
        self.nf_subtitle.grid(row=1, column=0, padx=20, pady=(5, 15), sticky="n")
 
        # Imagem do logo
        self.nf_image_label = customtkinter.CTkLabel(self.main_page, text="", image=self.logo_image)
        self.nf_image_label.grid(row=2, column=0, padx=20, pady=0, sticky="n")
 
        # Informações dos docentes e discentes
        self.nf_subtitle = customtkinter.CTkLabel(self.main_page, text="Docente: Luis Fernando de Almeida\nDiscentes: Clariana (RA 10112363) e Lara (RA 10102584)",
                                                  font=customtkinter.CTkFont(size=14, weight="normal"))
        self.nf_subtitle.grid(row=3, column=0, padx=20, pady=(20, 0), sticky="n")
 
        # Criando e configurando o textbox com a problemática
        #self.ms_hc_init_sol_textbox = customtkinter.CTkTextbox(self.main_page, wrap="word", height=95, border_spacing=20)
        #self.ms_hc_init_sol_textbox.tag_config("center", justify="center")
        #self.ms_hc_init_sol_textbox.insert("0.0", "O presente programa pretende solucionar a problemática da otimização do roteamento em Redes de Sensores Sem Fio (WSNs) "
        #                                                     "a partir de Algoritmos Genéticos, priorizando o método do Caixeiro Viajante. O objetivo é reduzir o consumo de energia "
        #                                                     "e maximizar a vida útil da rede, garantindo que todos os pontos de demanda sejam atendidos de forma eficiente.", "center")
        #self.ms_hc_init_sol_textbox.grid(row=4, column=0, padx=50, pady=(20, 0), sticky="nsew")
        #self.ms_hc_init_sol_textbox.configure(state="disabled")  # Permitir edição temporária para ajuste de altura
 
        # Criando um Frame para os Inputs e Resultado
        self.input_frame = customtkinter.CTkFrame(self.main_page, fg_color="transparent", border_width=1, border_color="gray")
        self.input_frame.grid(row=5, column=0, padx=50, pady=(20, 20), sticky="nsew")
        self.input_frame.grid_rowconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], weight=1)
        self.input_frame.grid_columnconfigure([0, 1], weight=1)
 
        # Criando o título "Parâmetros"
        self.input_frame_param_title = customtkinter.CTkLabel(self.input_frame, text="Parâmetros do AG", fg_color="transparent",
                                                             font=customtkinter.CTkFont(size=14, weight="bold"))
        self.input_frame_param_title.grid(row=0, column=0, columnspan=2, padx=20, pady=(10, 0), sticky="nsew")
 
        # Criando os Inputs do Tamanho de População
        self.input_frame_tampop_title = customtkinter.CTkLabel(self.input_frame, text="Tamanho da População", fg_color="transparent",
                                               font=customtkinter.CTkFont(size=14))
        self.input_frame_tampop_title.grid(row=1, column=0, padx=20, pady=(0, 5), sticky="nsew")
 
        self.input_frame_tampop_entry = customtkinter.CTkEntry(self.input_frame, placeholder_text="Digite o Tamanho da População...",
                                                    font=customtkinter.CTkFont(size=12, weight="normal"))
        self.input_frame_tampop_entry.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.input_frame_tampop_entry.insert(0, tamanho_populacao)
 
        # Criando os Inputs de Taxa de Cruzamento
        self.input_frame_taxc_title = customtkinter.CTkLabel(self.input_frame, text="Taxa de Cruzamento", fg_color="transparent",
                                                             font=customtkinter.CTkFont(size=14))
        self.input_frame_taxc_title.grid(row=1, column=1, padx=20, pady=(0, 5), sticky="nsew")
 
        self.input_frame_taxc_entry = customtkinter.CTkEntry(self.input_frame, placeholder_text="Digite a Taxa de Cruzamento...",
                                                    font=customtkinter.CTkFont(size=12, weight="normal"))
        self.input_frame_taxc_entry.grid(row=2, column=1, padx=20, pady=(0, 20), sticky="nsew")
        self.input_frame_taxc_entry.insert(0, taxa_cruzamento)
       
        # Criando os Inputs de Taxa de Mutação
        self.input_frame_taxm_title = customtkinter.CTkLabel(self.input_frame, text="Taxa de Mutação", fg_color="transparent",
                                                             font=customtkinter.CTkFont(size=14))
        self.input_frame_taxm_title.grid(row=3, column=0, padx=20, pady=(0, 5), sticky="nsew")
 
        self.input_frame_taxm_entry = customtkinter.CTkEntry(self.input_frame, placeholder_text="Digite a Taxa de Mutação...",
                                                    font=customtkinter.CTkFont(size=12, weight="normal"))
        self.input_frame_taxm_entry.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.input_frame_taxm_entry.insert(0, taxa_mutacao)
       
        # Criando os Inputs de Número de Gerações
        self.input_frame_numg_title = customtkinter.CTkLabel(self.input_frame, text="Número de Gerações", fg_color="transparent",
                                                             font=customtkinter.CTkFont(size=14))
        self.input_frame_numg_title.grid(row=3, column=1, padx=20, pady=(0, 5), sticky="nsew")
 
        self.input_frame_numg_entry = customtkinter.CTkEntry(self.input_frame, placeholder_text="Digite o número de Gerações...",
                                                    font=customtkinter.CTkFont(size=12, weight="normal"))
        self.input_frame_numg_entry.grid(row=4, column=1, padx=20, pady=(0, 20), sticky="nsew")
        self.input_frame_numg_entry.insert(0, num_geracoes)
       
        # Criando o título "Inputs"
        self.input_frame_mind_title = customtkinter.CTkLabel(self.input_frame, text="Inputs", fg_color="transparent",
                                                             font=customtkinter.CTkFont(size=14, weight="bold"))
        self.input_frame_mind_title.grid(row=5, column=0, columnspan=2, padx=20, pady=(10, 0), sticky="nsew")
 
        # Criando os Inputs de MinD e MaxD
        self.input_frame_mind_title = customtkinter.CTkLabel(self.input_frame, text="Distância Mínima", fg_color="transparent",
                                               font=customtkinter.CTkFont(size=14))
        self.input_frame_mind_title.grid(row=6, column=0, padx=20, pady=(0, 5), sticky="nsew")
 
        self.input_frame_mind_entry = customtkinter.CTkEntry(self.input_frame, placeholder_text="Digite o valor mínimo da Distância...",
                                                    font=customtkinter.CTkFont(size=12, weight="normal"))
        self.input_frame_mind_entry.grid(row=7, column=0, padx=20, pady=(0, 20), sticky="nsew")
 
        self.input_frame_maxd_title = customtkinter.CTkLabel(self.input_frame, text="Distância Máxima", fg_color="transparent",
                                                             font=customtkinter.CTkFont(size=14))
        self.input_frame_maxd_title.grid(row=6, column=1, padx=20, pady=(0, 5), sticky="nsew")
 
        self.input_frame_maxd_entry = customtkinter.CTkEntry(self.input_frame, placeholder_text="Digite o valor máximo da Distância...",
                                                    font=customtkinter.CTkFont(size=12, weight="normal"))
        self.input_frame_maxd_entry.grid(row=7, column=1, padx=20, pady=(0, 20), sticky="nsew")
 
        # Criando os Inputs de MinE e MaxE
        self.input_frame_mine_title = customtkinter.CTkLabel(self.input_frame, text="Energia Mínima", fg_color="transparent",
                                                             font=customtkinter.CTkFont(size=14))
        self.input_frame_mine_title.grid(row=8, column=0, padx=20, pady=(0, 5), sticky="nsew")
 
        self.input_frame_mine_entry = customtkinter.CTkEntry(self.input_frame,
                                                             placeholder_text="Digite o valor mínimo da Energia...",
                                                             font=customtkinter.CTkFont(size=12, weight="normal"))
        self.input_frame_mine_entry.grid(row=9, column=0, padx=20, pady=(0, 20), sticky="nsew")
 
        self.input_frame_maxe_title = customtkinter.CTkLabel(self.input_frame, text="Energia Máxima", fg_color="transparent",
                                                             font=customtkinter.CTkFont(size=14))
        self.input_frame_maxe_title.grid(row=8, column=1, padx=20, pady=(0, 5), sticky="nsew")
 
        self.input_frame_maxe_entry = customtkinter.CTkEntry(self.input_frame,
                                                             placeholder_text="Digite o valor máximo da Energia...",
                                                             font=customtkinter.CTkFont(size=12, weight="normal"))
        self.input_frame_maxe_entry.grid(row=9, column=1, padx=20, pady=(0, 20), sticky="nsew")
 
        # Criando os Inputs de MinC e MaxC
        self.input_frame_minc_title = customtkinter.CTkLabel(self.input_frame, text="Custo de Comunicação Mínimo", fg_color="transparent",
                                                             font=customtkinter.CTkFont(size=14))
        self.input_frame_minc_title.grid(row=10, column=0, padx=20, pady=(0, 5), sticky="nsew")
 
        self.input_frame_minc_entry = customtkinter.CTkEntry(self.input_frame,
                                                             placeholder_text="Digite o valor mínimo do Custo de Comunicação...",
                                                             font=customtkinter.CTkFont(size=12, weight="normal"))
        self.input_frame_minc_entry.grid(row=11, column=0, padx=20, pady=(0, 20), sticky="nsew")
 
        self.input_frame_maxc_title = customtkinter.CTkLabel(self.input_frame, text="Custo de Comunicação Máximo", fg_color="transparent",
                                                             font=customtkinter.CTkFont(size=14))
        self.input_frame_maxc_title.grid(row=10, column=1, padx=20, pady=(0, 5), sticky="nsew")
 
        self.input_frame_maxc_entry = customtkinter.CTkEntry(self.input_frame,
                                                             placeholder_text="Digite o valor máximo do Custo de Comunicação...",
                                                             font=customtkinter.CTkFont(size=12, weight="normal"))
        self.input_frame_maxc_entry.grid(row=11, column=1, padx=20, pady=(0, 20), sticky="nsew")
 
        # Criando os Inputs de QtdCidades
        self.input_frame_nos_title = customtkinter.CTkLabel(self.input_frame, text="Quantidade de Nós", fg_color="transparent",
                                                             font=customtkinter.CTkFont(size=14))
        self.input_frame_nos_title.grid(row=12, column=0, columnspan=2, padx=20, pady=(0, 5), sticky="nsew")
 
        self.input_frame_nos_entry = customtkinter.CTkEntry(self.input_frame,
                                                             placeholder_text="Digite a quantidade de nós...",
                                                             font=customtkinter.CTkFont(size=12, weight="normal"))
        self.input_frame_nos_entry.grid(row=13, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="nsew")
 
        # Criando o título de Resultados
        self.input_frame_title_result = customtkinter.CTkLabel(self.input_frame, text="Resultados", fg_color="transparent",
                                                             font=customtkinter.CTkFont(size=14, weight="bold"))
        self.input_frame_title_result.grid(row=14, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="nsew")
 
        # Criando e configurando o textbox com o Resultado
        self.input_frame_result_textbox = customtkinter.CTkTextbox(self.input_frame, wrap="word", border_spacing=20)
        self.input_frame_result_textbox.tag_config("center", justify="center")
        self.input_frame_result_textbox.insert("0.0", "", "center")
        self.input_frame_result_textbox.grid(row=15, column=0, columnspan=2, padx=15, pady=(0, 20), sticky="nsew")
        self.input_frame_result_textbox.configure(state="disabled")  # Permitir edição temporária para ajuste de altura
 
        # Criando o botão Rodar
        self.input_frame_result_run = customtkinter.CTkButton(self.input_frame, text="Rodar", command=self.executar_validacao)
        self.input_frame_result_run.grid(row=16, column=0, padx=15, pady=(0, 20), sticky="nsew")
 
        # Criando o botão Limpar
        self.input_frame_result_run = customtkinter.CTkButton(self.input_frame, text="Limpar", command=self.limpar)
        self.input_frame_result_run.grid(row=16, column=1, padx=15, pady=(0, 20), sticky="nsew")
 
    def validar_numero(self, valor):
        """Valida se o valor fornecido é um número."""
        try:
            float(valor)
            return True
        except ValueError:
            return False
 
    def validar_min_e(self, min_e):
        """Valida se o valor de min_e é 1, 2 ou 4."""
        return min_e in ['1', '2', '4']
 
    def validar_n_nos(self, n_nos):
        """Valida se n_nos é um inteiro positivo e maior que 1."""
        try:
            n_nos = int(n_nos)
            return n_nos > 1
        except ValueError:
            return False
 
    def validar_distancia(self, min_d, max_d):
        """Valida min_d e max_d para serem não negativos e min_d < max_d."""
        try:
            min_d = float(min_d)
            max_d = float(max_d)
            return min_d >= 0 and max_d >= 0 and min_d < max_d
        except ValueError:
            return False
 
    def validar_energia(self, min_e, max_e):
        """Valida min_e e max_e para serem não negativos e min_e < max_e."""
        try:
            min_e = float(min_e)
            max_e = float(max_e)
            return min_e >= 0 and max_e >= 0 and min_e < max_e
        except ValueError:
            return False
 
    def validar_custo(self, min_c, max_c):
        """Valida min_c e max_c para serem não negativos e min_c < max_c."""
        try:
            min_c = float(min_c)
            max_c = float(max_c)
            return min_c >= 0 and max_c >= 0 and min_c < max_c
        except ValueError:
            return False
 
    def validar_entradas(self, tam_p, tax_c, tax_m, num_g, min_d, max_d, min_e, max_e, min_c, max_c, qtd_nos):
        """Valida as entradas e exibe mensagens de erro no Tkinter se houver problemas."""
        if not (self.validar_numero(tam_p) and self.validar_numero(tax_c) and
                self.validar_numero(tax_m) and self.validar_numero(num_g) and
                self.validar_numero(min_d) and self.validar_numero(max_d) and
                self.validar_numero(min_e) and self.validar_numero(max_e) and
                self.validar_numero(min_c) and self.validar_numero(max_c) and
                self.validar_numero(qtd_nos)):
            messagebox.showwarning("Erro",
                                   "Todas as entradas de distância, energia, custo e quantidade de nós devem ser números.")
            return False
 
        if not self.validar_n_nos(qtd_nos):
            messagebox.showwarning("Erro", "A quantidade de nós (n_nos) deve ser um inteiro positivo maior que 1.")
            return False
 
        if not self.validar_distancia(min_d, max_d):
            messagebox.showwarning("Erro", "min_d deve ser menor que max_d e ambos devem ser não negativos.")
            return False
 
        if not self.validar_energia(min_e, max_e):
            messagebox.showwarning("Erro", "min_e deve ser menor que max_e e ambos devem ser não negativos.")
            return False
 
        if not self.validar_custo(min_c, max_c):
            messagebox.showwarning("Erro", "min_c deve ser menor que max_c e ambos devem ser não negativos.")
            return False
 
        if not self.validar_min_e(min_e):
            messagebox.showwarning("Erro", "O valor de Energia Mínima (min_e) deve ser 1, 2 ou 4.")
            return False
 
        return True
 
    # Execute a validação das entradas
    def executar_validacao(self):
        tam_p = self.input_frame_tampop_entry.get()
        tax_c = self.input_frame_taxc_entry.get()
        tax_m = self.input_frame_taxm_entry.get()
        num_g = self.input_frame_numg_entry.get()
        min_d = self.input_frame_mind_entry.get()
        max_d = self.input_frame_maxd_entry.get()
        min_e = self.input_frame_mine_entry.get()  # Supondo que min_e sempre será inteiro
        max_e = self.input_frame_maxe_entry.get()
        min_c = self.input_frame_minc_entry.get()
        max_c = self.input_frame_maxc_entry.get()
        qtd_nos = self.input_frame_nos_entry.get()
 
        if self.validar_entradas(tam_p, tax_c, tax_m, num_g, min_d, max_d, min_e, max_e, min_c, max_c, qtd_nos):
            messagebox.showinfo("Validação", "Validações bem sucedidas.")
            self.rodar_algoritmo()
        else:
            messagebox.showerror("Erro na validação", "Erro na validação dos dados de entrada.")
 
    # Função que executa o algoritmo genético
    def rodar_algoritmo(self):
        # Inicializa o problema e o algoritmo genético
        problema = Problema(int(self.input_frame_nos_entry.get()),
                            int(self.input_frame_mind_entry.get()),
                            int(self.input_frame_maxd_entry.get()),
                            int(self.input_frame_mine_entry.get()),
                            int(self.input_frame_maxe_entry.get()),
                            int(self.input_frame_minc_entry.get()),
                            int(self.input_frame_maxc_entry.get()))
        algoritmo_genetico = AlgoritmoGenetico(problema, int(self.input_frame_tampop_entry.get()), float(self.input_frame_taxc_entry.get()),
                                               float(self.input_frame_taxm_entry.get()), int(self.input_frame_numg_entry.get()))
 
        # Executa o algoritmo
        solucao_inicial = algoritmo_genetico.executar_1_geracao()
        melhor_solucao = algoritmo_genetico.executar()
       
        custo_inicial = str(problema.calcular_custo_total(solucao_inicial, problema.matriz_energia))
        custo_total = str(problema.calcular_custo_total(melhor_solucao, problema.matriz_energia))
       
        custo_inicial_num = int(problema.calcular_custo_total(solucao_inicial, problema.matriz_energia))
        custo_total_num = int(problema.calcular_custo_total(melhor_solucao, problema.matriz_energia))
       
        percentual_ganho = round(100 * (custo_inicial_num - custo_total_num) / custo_total_num)
 
        self.input_frame_result_textbox.configure(state="normal")
        self.input_frame_result_textbox.delete("1.0", tk.END)
        self.input_frame_result_textbox.insert(tk.END, str(melhor_solucao) + "\nCusto inicial: " + custo_inicial + "\nCusto final: " + custo_total + "\nGanho: " + str(percentual_ganho) + "%")
        self.input_frame_result_textbox.configure(state="disabled")
 
        self.salvar_resultados(melhor_solucao, solucao_inicial, custo_total, percentual_ganho)
 
    # Função que limpa os campos de entrada e saída
    def limpar(self):
        # Limpar o Textbox
        self.input_frame_result_textbox.configure(state="normal")
        self.input_frame_result_textbox.delete("1.0", tk.END)
        self.input_frame_result_textbox.configure(state="disabled")
 
        # Limpar os campos de entrada
        self.input_frame_nos_entry.delete(0, tk.END)
        self.input_frame_mind_entry.delete(0, tk.END)
        self.input_frame_maxd_entry.delete(0, tk.END)
        self.input_frame_mine_entry.delete(0, tk.END)
        self.input_frame_maxe_entry.delete(0, tk.END)
        self.input_frame_minc_entry.delete(0, tk.END)
        self.input_frame_maxc_entry.delete(0, tk.END)
 
        # Desfocar todos os campos de entrada
        self.input_frame_result_textbox.focus_set()  # Mover o foco para um widget neutro
 
    # Funcção para salvar os resultados em um txt
    def salvar_resultados(self, solucao_inicial, melhor_solucao, custo_total, percentual_ganho):
        # Caminho do arquivo
        arquivo_resultados = "resultados.txt"
 
        # Coletar os parâmetros
        min_d = self.input_frame_mind_entry.get()
        max_d = self.input_frame_maxd_entry.get()
        min_e = self.input_frame_mine_entry.get()
        max_e = self.input_frame_maxe_entry.get()
        min_c = self.input_frame_minc_entry.get()
        max_c = self.input_frame_maxc_entry.get()
        qtd_nos = self.input_frame_nos_entry.get()
 
        # Preparar o conteúdo a ser salvo
        conteudo = (
            "Inputs WSNs:\n"
            f"Distancia Minima: {min_d}\n"
            f"Distancia Maxima: {max_d}\n"
            f"Energia Minima: {min_e}\n"
            f"Energia Maxima: {max_e}\n"
            f"Custo de Comunicacao Manimo: {min_c}\n"
            f"Custo de Comunicacao Maximo: {max_c}\n"
            f"Quantidade de Nos: {qtd_nos}\n\n"
            "Resultados:\n"
            f"Primeiro Caminho: {solucao_inicial}\n"
            f"Melhor Caminho Encontrado: {melhor_solucao}\n"
            f"Custo Total do Caminho: {custo_total}\n"
            f"Ganho do algoritmo: {percentual_ganho}\n"
        )
 
        # Salvar no arquivo
        with open(arquivo_resultados, "w") as file:
            file.write(conteudo)
 
        messagebox.showinfo("Salvar Resultados", f"Resultados salvos em '{arquivo_resultados}'.")
 
if __name__ == "__main__":
    app = App()
    app.mainloop()