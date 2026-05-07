<div align="center">

# Organizador de Arquivos — File Organizer

Aplicação desenvolvida em **Python** para organizar arquivos automaticamente por categoria, com **interface gráfica**, **seleção de pasta**, **filtros por categoria**, **relatório detalhado** e recurso para **desfazer a última organização**.

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![GitHub](https://img.shields.io/badge/GitHub-phmbezerra-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/phmbezerra)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Paulo%20Henrique-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/paulo-henrique-melo-bezerra-8b1b28372/)

</div>

---

## Sobre o projeto

O **Organizador de Arquivos** é uma aplicação em Python criada para automatizar a organização de arquivos em uma pasta, separando-os em subpastas com base em suas extensões.

O projeto começou como uma solução em terminal para categorizar arquivos e gerar um relatório simples, e foi evoluído para uma versão mais completa e mais forte para portfólio, com foco em:

- automação prática;
- usabilidade;
- interface gráfica;
- controle maior sobre a organização;
- possibilidade de desfazer alterações.

Nesta versão atualizada, o projeto oferece uma experiência mais amigável ao usuário e recursos que aumentam sua utilidade em um cenário real.

---

## Visão geral

A aplicação permite:

- escolher a pasta por meio de uma interface gráfica;
- selecionar quais categorias poderão ser organizadas;
- mover arquivos automaticamente para subpastas;
- gerar um relatório detalhado da execução;
- salvar um histórico da organização;
- desfazer a última organização realizada.

Isso torna o projeto muito mais completo do que um simples script de automação.

---

## Tecnologias utilizadas

<div align="left">

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-0f172a?style=flat-square)
![Pathlib](https://img.shields.io/badge/Pathlib-Manipula%C3%A7%C3%A3o%20de%20arquivos-1e293b?style=flat-square)
![JSON](https://img.shields.io/badge/JSON-Hist%C3%B3rico-334155?style=flat-square)

</div>

---

## Objetivo do projeto

Este projeto foi desenvolvido com o objetivo de praticar e demonstrar conceitos importantes de automação com Python, incluindo:

- manipulação de arquivos e diretórios;
- organização automática por extensão;
- criação de subpastas dinamicamente;
- geração de relatórios;
- estruturação de lógica de negócio;
- construção de interface gráfica com Tkinter;
- persistência de histórico em JSON;
- tratamento de erros;
- desenvolvimento de soluções úteis para produtividade.

---

## Funcionalidades

- organização automática de arquivos por categoria;
- categorização com base em extensões;
- criação automática de subpastas;
- tratamento de nomes duplicados;
- escolha da pasta via explorador de arquivos;
- interface gráfica com Tkinter;
- filtros por categoria;
- log visual da execução dentro da aplicação;
- geração de relatório detalhado em `.txt`;
- salvamento de histórico em `.json`;
- desfazer a última organização realizada;
- mensagens de erro e sucesso mais amigáveis.

---

## Categorias suportadas

A aplicação reconhece e organiza arquivos nas seguintes categorias:

- **Imagens**
- **Documentos**
- **Planilhas**
- **Compactados**
- **Códigos**
- **Áudios**
- **Vídeos**
- **Outros**

Cada categoria é definida por um conjunto de extensões conhecidas.

---

## Melhorias implementadas nesta versão

Esta nova versão foi desenvolvida para tornar o projeto mais profissional, mais utilizável e mais valioso para portfólio.

### Principais melhorias
- migração de um script simples para uma aplicação com interface gráfica;
- botão para escolher pasta sem precisar digitar caminho manualmente;
- filtros por categoria antes da organização;
- relatório mais detalhado;
- histórico de execuções em arquivo JSON;
- opção para desfazer a última organização;
- tratamento mais robusto de erros;
- melhor organização do código;
- estrutura mais próxima de uma ferramenta real de produtividade.

---

## Diferenciais do projeto

O grande diferencial desta versão é que o projeto deixa de ser apenas um script básico e passa a funcionar como uma ferramenta mais completa.

Entre os diferenciais, estão:

- interface amigável;
- recurso de desfazer;
- histórico persistente;
- filtros de organização;
- relatórios detalhados;
- melhor experiência para o usuário final.

Esses pontos tornam o projeto muito mais interessante para demonstrar domínio prático de Python.

---

## Estrutura do projeto

```text
organizador-de-arquivos/
├── organizador_arquivos.py
└── README.md
```

## Destaques técnicos

### Python

- uso de pathlib para manipulação moderna de caminhos;
- uso de shutil.move para movimentação de arquivos;
- uso de datetime para registrar execuções;
- uso de json para salvar histórico de organização.


### Interface gráfica

- construída com tkinter;
- seleção de pasta via janela;
- filtros de categoria;
- área de log com acompanhamento da execução;
- botões para organizar e desfazer.


### Lógica de organização

- identificação de categoria por extensão;
- criação automática de diretórios;
- prevenção de conflito de nomes;
- geração de nomes alternativos quando necessário.

### Desfazer organização

- registro das movimentações em histórico;
- restauração dos arquivos para a origem;
- remoção de pastas vazias quando aplicável;
- tratamento de erros durante o processo de restauração.


## Relatórios e histórico

A aplicação gera automaticamente:

- relatorio_organizacao.txt

Arquivo com:

- data da execução;
- pasta analisada;
- categorias selecionadas;
- resumo por categoria;
- detalhamento de cada arquivo movido;
- total de arquivos organizados.

## .historico_organizacao.json

Arquivo usado para:

- registrar execuções anteriores;
- armazenar origem e destino de cada arquivo;
- permitir desfazer a última organização.

## Como executar o projeto

1. Clone este repositório:
```
git clone https://github.com/phmbezerra/organizador-de-arquivos.git
```

2. Acesse a pasta do projeto:
```
cd organizador-de-arquivos
```

3. Execute o arquivo Python:
python organizador_arquivos.py

Em alguns sistemas, pode ser necessário usar python3 no lugar de python.

## Como usar

1. Abra a aplicação.
2. Clique em Escolher pasta.
3. Selecione a pasta que deseja organizar.
4. Marque ou desmarque as categorias que deseja permitir.
5. Clique em Organizar arquivos.
6. Consulte o relatório gerado e o log exibido na tela.
7. Caso queira, use o botão Desfazer última organização para restaurar os arquivos.

## Aprendizados

Durante o desenvolvimento e evolução deste projeto, foram reforçados conceitos como:

- automação com Python;
- manipulação de arquivos e diretórios;
- estruturação de lógica de negócio;
- construção de interfaces gráficas;
- geração de relatórios;
- persistência de dados em JSON;
- tratamento de erros;
- criação de ferramentas úteis para produtividade.

## Melhorias futuras

Mesmo após esta atualização, o projeto ainda pode evoluir com recursos como:

- tema visual personalizado;
- arrastar e soltar pasta para organização;
- relatórios em formato CSV ou PDF;
- seleção manual de extensões personalizadas;
- múltiplos níveis de desfazer;
- empacotamento como executável.

## Autor

- Paulo Henrique de Melo Bezerra
- Estudante de Ciência da Computação — CEUB
- Brasília - DF

## Contato

- Email: paulohenriquemelobezerra1@gmail.com
- GitHub: github.com/phmbezerra
- LinkedIn: linkedin.com/in/paulo-henrique-melo-bezerra-8b1b28372

## Observação

Este projeto faz parte da construção do meu portfólio em tecnologia e representa minha evolução prática em Python, automação, organização de arquivos e criação de aplicações com interface gráfica.

<div align="center">
Obrigado por visitar este projeto.

</div>
