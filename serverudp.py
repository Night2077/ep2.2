import io
import socket
from imgen import im_generation

SEG_SIZE = 1024  # Tamanho do segmento de dados

def convert_to_byte_arr(image, format):  # Converte a imagem para bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=format)
    return img_byte_arr.getvalue()

def processar_mensagem(mensagem):  # Processa mensagem do cliente
    linhas = mensagem.strip().split('\n')
    if len(linhas) < 3:
        raise ValueError("Formato inválido. Esperado: nome_arquivo, texto_cima, texto_baixo")

    comando_arquivo = linhas[0].split()
    if len(comando_arquivo) > 3:
        raise ValueError("Erro no comando do arquivo")

    nome_arquivo = comando_arquivo[0]
    texto_cima = linhas[1]
    texto_baixo = linhas[2]

    return nome_arquivo, texto_cima, texto_baixo

def segmentar_dados(dados, seg_size):  # Divide em segmentos
    return [dados[i:i + seg_size] for i in range(0, len(dados), seg_size)]

def main():
    HOST = ''
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, PORT))
        print(f"Servidor UDP ouvindo na porta {PORT}")

        
        while True:
            data, addr = sock.recvfrom(1024)

            try:
                mensagem = data.decode()
                print(f"Mensagem recebida: {mensagem}")

                nome_arquivo, texto_cima, texto_baixo = processar_mensagem(mensagem)
                img = im_generation.generate_image_macro(nome_arquivo, texto_cima, texto_baixo)
                img_bytes = convert_to_byte_arr(img, 'JPEG')

                segmentos = segmentar_dados(img_bytes, SEG_SIZE) 
                seg_count = len(segmentos) 

                # Envia primeiro o número total de segmentos
                seg_count_bytes = seg_count.to_bytes(2, byteorder='big')
                sock.sendto(seg_count_bytes, addr)
                print(f"Enviado número total de segmentos: {seg_count}")

                for i, segmento in enumerate(segmentos): # envia cada segmento
                    header = i.to_bytes(2, byteorder='big')  
                    sock.sendto(header + segmento, addr) # envia índice + dados
                    print(f"Enviado segmento {i+1}/{seg_count} ({len(segmento)} bytes)")

                print(f"Imagem enviada para {addr} em {seg_count} segmentos")

            except Exception as e: 
                print(f"Erro ao atender {addr}: {e}")
                erro_msg = f"ERRO: {e}"
                sock.sendto(erro_msg.encode(), addr)


if __name__ == "__main__":
    main()

#testeoyth