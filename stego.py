import cv2
import numpy as np

def loadImage(filename):
    return cv2.imread(filename, cv2.IMREAD_UNCHANGED)

def showImage(img):
    if img is not None:
        cv2.imshow('Display Window', img)
        cv2.waitKey(0) # Waits until any key is pressed
        cv2.destroyAllWindows()
    else:
        print("Error: Could not load the image. Check the file path!")

def text_to_bits(text):
    text += '\0'
    bits = ""
    for char in text:
        bits += f"{ord(char):08b}"
    return bits

def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        char_code = int(byte, 2)
        if char_code == 0: # napotkano znacznik końca wiadomości
            break
        chars.append(chr(char_code))
    return "".join(chars)

def getFilename():
    filename = input("Podaj nazwę pliku png: ").strip()
    filename = filename if filename[-4:] == ".png" else filename + ".png"
    return filename

def lsb_embed(cover, bits):
    original_shape = cover.shape

    flat_cover = cover.flatten()

    if len(bits) > len(flat_cover):
        print("Błąd: Wiadomość jest za długa, aby zmieścić się w tym obrazie!")
        return cover

    for i in range(len(bits)):
        bit = int(bits[i])
        flat_cover[i] = (flat_cover[i] & 254) | bit

    return flat_cover.reshape(original_shape)

def UI():
    if input("Wybierz czynność:\n1. Ukryj wiadomość w pliku png\n2. Wyodrębnij wiadomość z pliku png\n").strip()=="1":
        filename = getFilename()
        img = loadImage(filename)

        if img is None:
            print("Nie można wczytać pliku źródłowego.")
            return

        message = input("Podaj wiadomość do ukrycia: ").strip()

        bit_message = text_to_bits(message)

        stego_img = lsb_embed(img, bit_message)

        output_filename = "stego_" + filename
        cv2.imwrite(output_filename, stego_img)
        print(f"Wiadomość została ukryta! Nowy plik to: {output_filename}")
        showImage(loadImage(output_filename))

UI()
