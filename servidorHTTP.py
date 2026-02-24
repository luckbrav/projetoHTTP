# Implementação de um servidor HTTP/1.1 para interpretação de métodos GET e POST

import socket

# Endereço IP vazio significa que aceita conexões de qualquer interface local
SERVER_HOST = ""
# A porta deve ser a 80 para acessar diretamente como http://localhost:80
SERVER_PORT = 80

# 1. Criação e configuração do socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)

print(f"Servidor em execução...")
print(f"Escutando por conexões na porta {SERVER_PORT}")

# 2. Loop principal para escutar conexões
while True:
    client_connection, client_address = server_socket.accept()

    # Recebemos os dados do cliente em formato de bytes (4096 bytes é um bom tamanho inicial)
    request_bytes = client_connection.recv(4096)
    
    if request_bytes:
        # 3. Separar o cabeçalho HTTP do Corpo da requisição
        # O padrão HTTP usa \r\n\r\n para dividir cabeçalhos do conteúdo (body)
        partes = request_bytes.split(b"\r\n\r\n", 1)
        headers_raw = partes[0].decode() # Decodificamos apenas o cabeçalho para string
        body_bytes = partes[1] if len(partes) > 1 else b""
        
        # 4. Analisar a primeira linha da requisição (Ex: "GET /index.html HTTP/1.1")
        linhas_header = headers_raw.split("\n")
        primeira_linha = linhas_header[0].split()
        
        if len(primeira_linha) >= 2:
            metodo = primeira_linha[0] # "GET" ou "POST"
            filename = primeira_linha[1] # Caminho solicitado
            
            print(f"Recebido -> Método: {metodo} | Ficheiro: {filename}")

            # Se pediu a raiz, direcionamos para o index
            if filename == "/":
                filename = "/index.html"
            
            # Removemos a barra inicial (ex: "/index.html" vira "index.html")
            # Isso garante que ele procure no diretório raiz atual do script
            filepath = filename[1:]

            # ==========================================
            # LÓGICA DO MÉTODO GET
            # ==========================================
            if metodo == "GET":
                try:
                    # Lemos o ficheiro em modo 'rb' (read binary) para suportar textos E imagens
                    with open(filepath, "rb") as fin:
                        content = fin.read()
                    
                    # Montamos a resposta de Sucesso
                    response_header = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
                    
                    # Enviamos o cabeçalho convertido em bytes + o conteúdo do ficheiro
                    client_connection.sendall(response_header.encode() + content)
                    
                except FileNotFoundError:
                    # Lógica para quando o objeto solicitado não existir [cite: 23]
                    response = "HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>ERRO 404!</h1><p>Ficheiro Nao Encontrado!</p>"
                    client_connection.sendall(response.encode())
            
            # ==========================================
            # LÓGICA DO MÉTODO POST
            # ==========================================
            elif metodo == "POST":
                # O objetivo aqui é armazenar novos recursos no servidor 
                nome_novo_ficheiro = "recurso_recebido.txt"
                
                # Salvamos o corpo da requisição num novo ficheiro
                with open(nome_novo_ficheiro, "wb") as fout:
                    fout.write(body_bytes)
                
                # Respondemos ao cliente confirmando a criação
                response = "HTTP/1.1 201 Created\r\n\r\n<h1>Sucesso!</h1><p>Recurso criado no servidor via POST.</p>"
                client_connection.sendall(response.encode())

    # Fechar a conexão dedicada com este cliente
    client_connection.close()