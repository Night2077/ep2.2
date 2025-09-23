import io
import socket
from pdb import main
from imgen import im_generation

NOME_DA_IMAGEM = 'img.jpg'
TEXTO_CIMA = 'Persona 6'
TEXTO_BAIXO = 'Nunca Sai'


def convert_to_byte_arr(image, format):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=format)
    return img_byte_arr.getvalue()

def main():

    HOST = '127.0.0.1' # Endereço IP do servidor
    PORT = 65432       # Porta que o servidor está escutando

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT)) # Vincular o socket ao endereço e porta
        s.listen() 
        print(f'Servidor escutando em {HOST}:{PORT}')

        while True: 
            conn, addr = s.accept() # Aceitar uma conexão

            with conn: # Manter a conexão aberta
                print(f'Conectado por {addr}') 
                
                img = im_generation.generate_image_macro(NOME_DA_IMAGEM, TEXTO_CIMA, TEXTO_BAIXO) # Gerar a image macro
                img_bytes = convert_to_byte_arr(img, 'JPEG') # Converter para bytes
                conn.sendall(img_bytes) # Enviar a imagem para o cliente
                
                print(f"Imagem enviada para {addr}")

if __name__ == "__main__":
    main()

