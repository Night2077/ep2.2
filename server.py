import io
import socket
from pdb import main
from imgen import im_generation


def convert_to_byte_arr(image, format):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=format)
    return img_byte_arr.getvalue()

def processar_mensagem(mensagem):
    linhas = mensagem.strip().split('\n')
    if len(linhas) < 3:
        raise ValueError("erro")

    comando_arquivo = linhas[0].split() 
    if len(comando_arquivo) > 3:
        raise ValueError("erro")

    nome_arquivo = comando_arquivo[0]
    texto_cima = linhas[1]
    texto_baixo = linhas[2]

    return nome_arquivo, texto_cima, texto_baixo

def main():

    HOST = '127.0.0.1' # Endereço IP do servidor
    PORT = 65432       # Porta que o servidor está escutando

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT)) # Vincular o socket ao endereço e porta
        s.listen() 
        print(f'Servidor escutando em {HOST}:{PORT}')

        while True: 
            conn, addr = s.accept() # Aceitar uma conexão

            try:
                with conn: # Manter a conexão aberta
                    print(f'Conectado por {addr}') 

                    dados = conn.recv(1024).decode() # Receber dados do cliente

                    print(f"Dados recebidos: {dados}")

                    nome_arquivo, texto_cima, texto_baixo = processar_mensagem(dados) # Processar a mensagem
                    img = im_generation.generate_image_macro(nome_arquivo, texto_cima, texto_baixo) # Gerar a image macro
                    img_bytes = convert_to_byte_arr(img, 'JPEG') # Converter para bytes
                    conn.sendall(img_bytes) # Enviar a imagem para o cliente
                    
                    print(f"Imagem enviada para {addr}")

            except Exception as e: # Manter a conexão aberta mesmo em caso de erro
                print(f"Erro ao atender {addr}: {e}")

if __name__ == "__main__":
    main()

