# Implementação de um servidor HTTP/1.1 para interpretação de métodos GET e POST

import socket

# Endereço IP vazio aceita conexões de qualquer host local
SERVER_HOST = ""
# A porta deve ser a 80 para acessar diretamente http://localhost:80
SERVER_PORT = 80

# Criação e configuração do socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)

print(f"Servidor em execução...")
print(f"Escutando por conexões na porta {SERVER_PORT}")

# Loop para listening de conexões
while True:
    client_connection, client_address = server_socket.accept()

    # Recebendo os dados do cliente em formato de bytes (4096 bytes é um bom tamanho inicial)
    request_bytes = client_connection.recv(4096)
    
    if request_bytes:
        # Separar o cabeçalho HTTP do Corpo da requisição
        partes = request_bytes.split(b"\r\n\r\n", 1)
        headers_raw = partes[0].decode() # Decodificando apenas o cabeçalho para string
        body_bytes = partes[1] if len(partes) > 1 else b""
        
        # Analisar a primeira linha da requisição (Ex: "GET /index.html HTTP/1.1")
        linhas_header = headers_raw.split("\n")
        primeira_linha = linhas_header[0].split()
        
        if len(primeira_linha) >= 2:
            metodo = primeira_linha[0] # "GET" ou "POST"
            filename = primeira_linha[1] # Caminho solicitado
            
            print(f"Recebido -> Método: {metodo} | arquivo: {filename}")

            # Se pediu a raiz, direcionando para o index
            if filename == "/":
                filename = "/index.html"
            
            # Removendo barra inicial (ex: "/index.html" para "index.html"), isso garante que ele procure no diretório raiz atual do script
            filepath = filename[1:]

            # ==========================================
            # LÓGICA DO MÉTODO GET
            # ==========================================
            if metodo == "GET":
                try:
                    # Lendo o arquivo em modo read binary (rb) para suportar textos E imagens
                    with open(filepath, "rb") as fin:
                        content = fin.read()
                    
                    # Resposta de Sucesso
                    response_header = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
                    
                    # Enviando o cabeçalho convertido em bytes + o conteúdo do arquivo
                    client_connection.sendall(response_header.encode() + content)
                    
                except FileNotFoundError:
                    # Se o arquivo não for encontrado, respondemos com o erro 404
                    response = "HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>ERRO 404!</h1><p>arquivo Nao Encontrado!</p>"
                    client_connection.sendall(response.encode())
            
            # ==========================================
            # LÓGICA DO MÉTODO POST
            # ==========================================
            elif metodo == "POST":
                # Se o método for POST, vamos armazenar o corpo da requisição em um "Banco de dados"
                nome_novo_arquivo = "BD.txt"
                
                # Salvando o corpo da requisição num novo arquivo (em modo append binary para não sobrescrever os dados anteriores)
                with open(nome_novo_arquivo, "ab") as fout:
                    fout.write(b"\n--- Nova Submissao POST ---\n") # Adiciona um separador visual
                    fout.write(body_bytes)
                    fout.write(b"\n") # Adiciona uma quebra de linha no final
                
                # Respondendo o cliente confirmando a criação
                response = 'HTTP/1.1 201 Created\r\n\r\n<h1>Sucesso!</h1><p>Recurso criado no servidor via POST.</p><br><a href="index.html"><button>Voltar para a tela inicial</button></a>'
                client_connection.sendall(response.encode())

    # Fechar a conexão dedicada com este cliente
    client_connection.close()