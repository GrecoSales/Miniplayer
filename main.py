import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pygame
from mutagen.mp3 import MP3
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import shutil
import json

janela = TkinterDnD.Tk()

ícone = tk.PhotoImage(file="layers/icone_player.png")
janela.iconphoto(False, ícone)

janela.title("Miniplayer") # Muda o título exibido na barra superior
janela.geometry("800x400") # Redimensiona o tamanho da janela
janela.config(padx = 5, pady = 5, bg = "gray15") # Acrescenta margens e uma cor para o fundo da janela
janela.resizable(False, False) # O usuário não pode arrastar as bordas da janela para alterar largura ou altura

pygame.mixer.init()

Pasta = tk.PhotoImage(file = "layers/pasta.png")

Retornar = tk.PhotoImage(file = "layers/Retornar.png")
Pausar = tk.PhotoImage(file = "layers/Pausar.png")
Avançar = tk.PhotoImage(file = "layers/Avançar.png")
Drag_and_Drop = tk.PhotoImage(file = "layers/adicionar_arquivo.png")

# -------------------------------------------------------------------------------------------------------------
        # TIPOS DE ESTILOS PERSONALIZADOS DO MINIPLAYER

# Altera o estilo dos dois frames de uma vez, apenas mencionando o depois
estilo_frames = {
    "bg" : "gray15",
    "highlightbackground" : "#164FD2",
    "highlightcolor" : "#164FD2",
    "highlightthickness" : 3
}

estilo_títulos = {
    "bg" : "gray15",
    "fg" : "white",
    "font" : ("Arial", 18, "bold")
}

estilo_textos = {
    "bg" : "gray15",
    "fg" : "white",
    "font" : ("Arial", 20)
}

# Altera o estilo da barra de rolagem
estilo_scrollbar = ttk.Style()
estilo_scrollbar.theme_use("clam")

estilo_scrollbar.configure(
    "Vertical.TScrollbar",
    gripcount = 0,
    background = "gray25",
    troughcolor = "gray15",
    bordercolor = "gray15",
    darkcolor = "gray15",
    lightcolor = "gray15",
    arrowcolor = "white"
)

# Altera o estilo da barra de progresso
estilo_barra_progresso = ttk.Style()

estilo_barra_progresso.configure(
    "Horizontal.TProgressbar",
    background = "#427AF5",
    troughcolor = "gray25",
    bordercolor = "gray8",
    lightcolor = "#427AF5",
    darkcolor = "#427AF5",
    thickness = 10
)

# -------------------------------------------------------------------------------------------------------------
        # SEPARAÇÂO ENTRE AS JANELAS COM E SEM PASTA CONFIGURADA

janela_inicial = tk.Frame(janela, bg = "gray15")
janela_player = tk.Frame(janela)

def exibir_início(): # Mostra a janela de seleção de pasta
    janela_player.pack_forget()
    janela_inicial.pack(fill = "both", expand = True)

def exibir_player(): # Mostra a janela principal do Miniplayer
    janela_inicial.pack_forget()
    janela_player.pack(fill = "both", expand = True)

frame_de_introdução = tk.Label(janela_inicial, image = Pasta, text = "Clique para inserir uma pasta com áudios", compound = "top", **estilo_textos, cursor = "hand2")

frame_de_introdução.pack(expand = True)

# -------------------------------------------------------------------------------------------------------------
        # INSTÂNCIA DOS FRAMES ESQUERDO E DIREITO

frame_esquerdo = tk.Frame(janela_player, width = 300, **estilo_frames)
frame_direito = tk.Frame(janela_player, width = 500, **estilo_frames)

# Impede que o frame encolha para o tamanho do conteúdo
frame_esquerdo.pack_propagate(False)
frame_direito.pack_propagate(False)

# fill = "y" ajusta o tamanho do frame para preencher a tela até chegar ao extremo de baixo
frame_esquerdo.pack(side = "left", fill = "y")
frame_direito.pack(side = "left", fill = "y")

# -------------------------------------------------------------------------------------------------------------
        # INSTÂNCIA DOS ELEMENTOS DO FRAME ESQUERDO

caixa_cima = tk.Frame(frame_esquerdo, bg = "gray15")
separador1 = tk.Frame(frame_esquerdo, bg = "#164FD2", height=3)
caixa_baixo = tk.Frame(frame_esquerdo, bg = "gray15")

# Configura e insere o título "Áudios:"
título_esquerda = tk.Label(caixa_cima, text = "Lista de Áudios:", **estilo_títulos)
título_esquerda.pack()

caixa_cima.pack(anchor = "nw") # anchor = "nw", ancora o conteúdo ao canto superior esquerdo
separador1.pack(fill = "x") # fill = "x" preenche até chegar na extrema direita
caixa_baixo.pack(fill = "both", expand = True) # expand = True e fill = "both" determinam que o conteúdo deve se expandir até o limite

# -------------------------------------------------------------------------------------------------------------
        # CONFIGURAÇÕES E SELEÇÃO DE PASTA

CONFIG_FILE = "config.json"

def ler_config():
    if os.path.exists(CONFIG_FILE):
        with open (CONFIG_FILE, "r", encoding = "UTF-8") as arquivo:
            return json.load(arquivo)

    return {"music_folder" : None}

config = ler_config()

def editar_config(config):
    with open(CONFIG_FILE, "w", encoding = "UTF-8") as arquivo:
        json.dump(config, arquivo, indent = 4)

def selecionar_pasta(evento = None):
    pasta = filedialog.askdirectory(title = "Escolha a sua pasta de áudios")
    
    if pasta:
        config["music_folder"] = pasta # o valor dentro do "music_folder" no json, será igual ao valor da variável pasta
        editar_config(config)
        carregar_audios(pasta)
        exibir_player()

frame_de_introdução.bind("<Button-1>", selecionar_pasta) # Na janela inicial é capaz de clicar para selecionar a pasta

janela.bind("<Control-o>", selecionar_pasta)

# -------------------------------------------------------------------------------------------------------------
        # LISTA DE ÁUDIOS E REPRODUÇÃO

FORMATOS_SUPORTADOS = (".mp3")

lista = tk.Listbox(caixa_baixo, bd = 0, highlightthickness = 0, selectbackground="gray6", **estilo_textos)

def carregar_audios(pasta):
    lista.delete(0, tk.END)

    for arquivo in os.listdir(pasta):
        if arquivo.lower().endswith(FORMATOS_SUPORTADOS):
            lista.insert(tk.END, arquivo)

tocando = False # Permite que .play, .pause e .unpause trabalhem adequadamente

tempo_total = 0 # Variável para ver e ajustar o tempo total dos arquivos

tempo_iniciada = 0 # conta o tempo da música

def selecionado(evento):
    global tocando
    global tempo_total
    global tempo_iniciada

    atual = lista.curselection()

    if atual:
        arquivo = lista.get(atual)
        caminho = os.path.join(config["music_folder"], arquivo)
        pygame.mixer.music.load(caminho)
        tempo_iniciada = 1
        pygame.mixer.music.play()
        tocando = True

        audio = MP3(caminho)
        tempo_total = int(audio.info.length)

lista.bind("<<ListboxSelect>>", selecionado)

scrollbar = ttk.Scrollbar(caixa_baixo, orient="vertical", command = lista.yview)
lista.config(yscrollcommand = scrollbar.set)

scrollbar.pack(side = "right", fill = "y")
lista.pack(padx = 7, pady = 5, fill = "both", expand = True)

# -------------------------------------------------------------------------------------------------------------
        # ARRASTAR E SOLTAR ARQUIVOS PARA A PASTA SELECIONADA

adicionar_arquivo = tk.Label(lista, bg = "steel blue", bd = 0, highlightthickness = 0, image = Drag_and_Drop, text = "Adicionar arquivo", fg = "black", font = ("Arial", 13, "bold"), padx = 1, compound = "top")

transferência_aceita = tk.Label(text = "✓Arquivo adicionado para pasta", bg = "#2E8B57", fg = "white", font = ("Arial", 18), highlightbackground = "#0C3329", highlightthickness = 3)
transferência_negada = tk.Label(text = "✗Tipo de arquivo não suportado", bg = "#B22222", fg = "white", font = ("Arial", 18), highlightbackground = "#400E0E", highlightthickness = 3)

lista.drop_target_register(DND_FILES)

def icone_liga(evento):
    adicionar_arquivo.place(relx = 0.5, rely = 0.5, anchor = "center")

def icone_desliga(evento):
    adicionar_arquivo.place_forget()

def arrastar_e_soltar(evento):
    caminho = evento.data.strip("{}")
    arquivo = os.path.basename(caminho)

    adicionar_arquivo.place_forget()

    if caminho.lower().endswith(FORMATOS_SUPORTADOS):
        shutil.copy2(caminho, config["music_folder"])
        lista.insert(tk.END, arquivo)
        mostrar_mensagem(transferência_aceita)
    
    else:
        mostrar_mensagem(transferência_negada)

def mostrar_mensagem(label):
    y = 1.05

    def entrada():
        nonlocal y

        if y > 0.95:
            y -= 0.02
            label.place(relx = 0.22, rely = y, anchor = "s")
            janela.after(15, entrada)
        else:
            janela.after(2000, saída)
    
    def saída():
        nonlocal y

        if y < 1.05:
            y += 0.02
            label.place(relx = 0.22, rely = y, anchor = "s")
            janela.after(15, saída)
        else:
            label.place_forget()

    entrada()

lista.dnd_bind("<<DropEnter>>", icone_liga)
lista.dnd_bind("<<DropLeave>>", icone_desliga)
lista.dnd_bind('<<Drop>>', arrastar_e_soltar)

# -------------------------------------------------------------------------------------------------------------

direita_cima = tk.Frame(frame_direito, bg = "gray15")
separador2 = tk.Frame(frame_direito, bg = "#164FD2", height=3)
direita_meio = tk.Frame(frame_direito, bg = "gray11")
separador3 = tk.Frame(frame_direito, bg = "#164FD2", height=3)
direita_baixo = tk.Frame(frame_direito, bg = "gray15")

# -------------------------------------------------------------------------------------------------------------

caixa_botões = tk.Label(direita_meio, bg = "gray11")

título_direita = tk.Label(direita_cima, text = "Player:", **estilo_títulos)
título_direita.pack()

def retornar():

    global tocando
    global tempo_iniciada

    tempo_atual = tempo_iniciada + (pygame.mixer.music.get_pos() // 1000)

    tempo_iniciada = max(0, tempo_atual - 10)

    tocando = True
    pygame.mixer.music.play(start = tempo_iniciada)

def play():

    global tocando

    if tempo_iniciada > 0: # Impede que o play feche o programa pela falta de um arquivo
        if tocando:
            pygame.mixer.music.pause()
            tocando = False
        else:
            pygame.mixer.music.unpause()
            tocando = True

def avançar():

    global tocando
    global tempo_iniciada

    tempo_atual = tempo_iniciada + (pygame.mixer.music.get_pos() // 1000)

    tempo_iniciada = min(tempo_atual + 10, tempo_total)

    tocando = True
    pygame.mixer.music.play(start = tempo_iniciada)

botão_menos10 = tk.Button(caixa_botões, bg = "gray11", activebackground = "gray11", bd = 0, relief = "flat", image = Retornar, command = retornar)
botão_play = tk.Button(caixa_botões, bg = "gray11", activebackground = "gray11", bd = 0, relief = "flat", image = Pausar, command = play)
botão_mais10 = tk.Button(caixa_botões, bg = "gray11", activebackground = "gray11", bd = 0, relief = "flat", image = Avançar, command = avançar)

botão_menos10.pack(side = "left", padx = 5)
botão_play.pack(side = "left", padx = 5)
botão_mais10.pack(side = "left", padx = 5)

caixa_botões.pack(expand = True)

# -------------------------------------------------------------------------------------------------------------

def atualizar_tempo():

    posicao = pygame.mixer.music.get_pos()

    if posicao < 0:
        tempo = tempo_total
    else:
        tempo = tempo_iniciada + (posicao // 1000)

    if tempo_total > 0:
        min_atual = tempo // 60
        seg_atual = tempo % 60

        min_total = tempo_total // 60
        seg_total = tempo_total % 60

        relógio.config(text = f"{min_atual:02}:{seg_atual:02} / {min_total:02}:{seg_total:02}")
        progresso = min((tempo / tempo_total) * 100, 100)
        barra_progresso["value"] = progresso

    janela.after(500, atualizar_tempo)

barra_progresso = ttk.Progressbar(direita_baixo, orient = "horizontal", mode = "determinate", maximum = 100)
barra_progresso.pack(fill = "x", padx = 10, pady = 10)

def clicar_barra(evento):
    
    global tempo_iniciada

    porcentagem = evento.x / barra_progresso.winfo_width()

    tempo_iniciada = int(porcentagem * tempo_total)

    pygame.mixer.music.play(start = tempo_iniciada)

barra_progresso.bind("<Button-1>", clicar_barra)

relógio = tk.Label(direita_baixo, text = "00:00 / 00:00", **estilo_textos) # Mostra visualmente o tempo do áudio
relógio.pack()

# -------------------------------------------------------------------------------------------------------------

direita_cima.pack(anchor = "nw")
separador2.pack(fill = "x")
direita_meio.pack(fill = "both", expand = True)
separador3.pack(fill = "x")
direita_baixo.pack(side = "bottom", fill = "x", pady = 10)

# -------------------------------------------------------------------------------------------------------------
    # TRANSIÇÃO ENTRE AS JANELAS

if config["music_folder"] and os.path.isdir(config["music_folder"]):
    carregar_audios(config["music_folder"])
    exibir_player()

else:
    config["music_folder"] = None
    editar_config(config)
    exibir_início()

# -------------------------------------------------------------------------------------------------------------

atualizar_tempo()
janela.mainloop()