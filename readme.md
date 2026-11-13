# 🎵 Miniplayer

Reprodutor de áudio MP3 desenvovido em Python com a finalidade de melhorar a experiência para quem ouve músicas em segundo plano. Possui uma interface gráfica compacta e permite ao usuário selecionar uma pasta para organizar e acessar suas músicas.

## Visão geral

O **Miniplayer** é projetado para permitir a reprodução de músicas em segundo plano sem ocupar muito espaço na tela.

Na primeira execução, o programa solicita ao usuário a seleção de um diretório com seus arquivos de áudio. Essa pasta fica salva nas configurações e pode ser alterada posteriormente por meio do atalho Ctrl + O.

Com uma interface gráfica discreta e funcionalidades essenciais, o Miniplayer busca oferecer uma experiência de reprodução simples e prática permitindo que o usuário ouça suas músicas enquanto realiza outras atividades no computador.

### 📸 Capturas de tela

<img src="assets/image 1.png" width="350">
<img src="assets/image 2.png" width="350">
<img src="assets/image 3.png" width="300">

## ⚙️ Funcionalidades

- **Seleção de diretório:** escolha de uma pasta para armazenar e acessar os arquivos de áudio.
- **Persistência de configurações:** salva automaticamente o diretório selecionado, restaurando-o nas próximas execuções.
- **Atalho de acesso:** permite selecionar ou alterar a pasta de áudios utilizando Ctrl + O.
- **Lista de reprodução:** identifica e exibe os arquivos MP3 encontrados no diretório configurado.
- **Reprodução de áudio:** permite selecionar e reproduzir músicas diretamente pela lista.
- **Controles de reprodução:** funcionalidades de pausar, retomar e avançar ou retroceder em 10 segundos.
- **Controle de progresso:** exibe o tempo atual e a duração total do áudio, com uma barra de progresso que permite navegar pela música.
- **Arrastar e soltar:** permite adicionar arquivos MP3 à pasta configurada diretamente pela interface, com indicação visual de sucesso ou rejeição do formato.
- **Interface gráfica reduzida:** janela de dimensões fixas, organizada para facilitar o acesso aos controles sem ocupar muito espaço na tela.

## 🏛️ Arquitetura

O Miniplayer foi desenvolvido em Python e possui sua estrutura dividida em blocos funcionais e funções responsáveis por diferentes tarefas da aplicação.

Sua organização contempla a inicialização e configuração da interface gráfica, o gerenciamento de arquivos e configurações, a reprodução de áudio e a atualização das informações de execução.

Principais componentes e responsabilidades:

- **Interface gráfica:** construída com Tkinter e TkinterDnD2, responsável pela apresentação dos elementos visuais e pela interação com o usuário.
- **Gerenciamento de configurações:** utiliza JSON para armazenar e recuperar o diretório de músicas selecionado, preservando as preferências entre diferentes execuções.
- **Manipulação de arquivos:** utiliza recursos nativos do Python para localizar, listar e copiar arquivos MP3 para o diretório configurado.
- **Reprodução de áudio:** utiliza Pygame para carregar e controlar a reprodução dos arquivos, incluindo pausa, retomada e navegação pela música.
- **Leitura de metadados:** utiliza Mutagen para obter informações sobre a duração dos arquivos MP3.
- **Atualização da reprodução:** monitora o progresso do áudio e atualiza periodicamente o relógio e a barra de progresso da interface.

> **Nota do desenvolvedor:** O Miniplayer é um projeto que eu desenvolvo desde que eu comecei a aprender programação e Python, então a forma como organizei a arquitetura não é a mais ideal, mas como este é um projeto de estudo eu me permiti dar mais foco para outras partes. De qualquer maneira, sinta-se livre para alterar a organização do código da forma que mais te agradar.

## 🛠️ Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| **Python** | Linguagem principal de desenvolvimento |
| **Tkinter** | Criação e gerenciamento da interface gráfica |
| **TkinterDnD2** | Implementação da funcionalidade de arrastar e soltar arquivos |
| **Pygame** | Reprodução e controle dos arquivos de áudio |
| **Mutagen** | Leitura de metadados dos arquivos MP3, como a duração |
| **JSON** | Armazenamento e recuperação das configurações do usuário |
| **PyInstaller** | Empacotamento da aplicação em executável para Windows |

O projeto utiliza funções para organizar as responsabilidades do código, além de bibliotecas nativas do Python para manipulação de arquivos, gerenciamento de caminhos e interação com o sistema operacional.

## **⬇️ Instalação e Execução**

1. Acesse a seção [Releases](https://github.com/GrecoSales/Miniplayer/releases) do repositório.
2. Baixe a versão mais recente do arquivo `Miniplayer.zip`.
3. Extraia o conteúdo do arquivo ZIP em uma pasta de sua preferência.
4. Execute o arquivo `Miniplayer.exe`.

**Primeira execução:**

Ao iniciar o Miniplayer pela primeira vez, será solicitada a seleção de uma pasta contendo arquivos MP3. Após selecionar o diretório, o programa carregará as músicas disponíveis e salvará o caminho nas configurações para utilizá-lo nas próximas execuções.

Para selecionar outra pasta posteriormente, utilize o atalho `Ctrl + O`.

**Requisitos:**
- Sistema operacional Windows.
- Não é necessário instalar Python ou as dependências do projeto para executar a versão empacotada.

Para executar e empacotar o projeto a partir do código-fonte, são necessários:

- Python 3.
- pip, para instalação das dependências.
- PyInstaller, para geração do executável.

## 📋 Funcionalidades planejadas

- [...] Suporte a novos formatos de áudio
- [...] Modo de reprodução aleatória
- [...] Modo de repetição
- [...] Informações adicionais da música
- [...] Controle de volume
- [...] Melhorias na interface
- [...] Reprodução simultânea opcional

## 📑 Licença

Este projeto está disponibilizado sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais informações.