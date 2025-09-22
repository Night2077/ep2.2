
from pdb import main
from imgen import im_generation
#from PIL import Image

NOME_DA_IMAGEM = 'img.jpg'
TEXTO_CIMA = 'Persona 6'
TEXTO_BAIXO = 'Nunca Sai'

img = im_generation.generate_image_macro(NOME_DA_IMAGEM, TEXTO_CIMA, TEXTO_BAIXO)

img.show()
img.save('output.jpg')
print('Imagem macro gerada e salva como output.jpg')



if __name__ == "__main__":
    main()
