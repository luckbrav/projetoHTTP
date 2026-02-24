# Projeto Servidor HTTP em Python

## Descrição do Projeto
Este projeto consiste na implementação de um servidor Web capaz de interpretar comandos HTTP de diferentes clientes. O servidor foi desenvolvido "from scratch" (do zero), utilizando a linguagem Python 3.x e a biblioteca nativa de `sockets`. 

O objetivo principal é entender o funcionamento interno da Web e do protocolo HTTP/1.1 , sem o uso de bibliotecas de alto nível ou frameworks que automatizem o processo, 61].

## Funcionalidades
* **Comunicação via Sockets:** Estabelece conexão direta na porta 80 usando a API de sockets do Python.
* **Método GET:** O servidor recebe requisições, localiza o arquivo solicitado no diretório raiz e o envia de volta ao cliente (suportando arquivos de texto, HTML e imagens).
* **Método POST:** O servidor é capaz de receber dados do cliente e armazená-los, criando novos recursos no servidor. O histórico de submissões é salvo no arquivo `recurso_recebido.txt`.
* **Tratamento de Erros:** Caso o cliente solicite um recurso que não existe, o servidor responde adequadamente com um erro `404 Not Found`.
* **Multi-cliente:** Projetado para responder a solicitações HTTP de forma geral, seja através de navegadores (como o Google Chrome) ou via terminal usando Telnet, 25, 26, 65].

## Estrutura de Arquivos
De acordo com os requisitos, todos os objetos ficam no diretório raiz:
* `servidorHTTP.py`: Código principal do servidor.
* `index.html`: Página inicial solicitada pelo navegador (`http://localhost:80`), contendo navegação e o formulário de teste.
* `ipsum.html`: Página secundária contendo texto de exemplo.
* `galeria.html`: Página secundária que exibe uma imagem carregada pelo servidor.
* `imagem.jpg`: Arquivo de imagem utilizado pela galeria.
* `recurso_recebido.txt`: Arquivo gerado dinamicamente para armazenar os dados enviados via formulário POST.

## Como Executar
1. Certifique-se de ter o **Python 3.x** instalado em seu sistema.
2. Abra o terminal (Ubuntu ou outro SO) e navegue até a pasta raiz do projeto.
3. Execute o script do servidor:
   ```bash
   python servidorHTTP.py