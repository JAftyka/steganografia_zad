import cv2
import numpy as np
  
def embed(image_path, message, output_path):
  cover = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
  if cover is None:
    raise FileNotFoundError(f"Nie znaleziono obrazu {image_path}")
  message_bits = ''.join(format(ord(char), '08b') for char in message)
  num_bits = len(message_bits)
    
  flat_cover = cover.flatten()

  if num_bits > len(flat_cover):
    raise ValueError("Wiadomość jest za długa!")
    
  for i in range(len(message_bits)):
    bit = int(message_bits[i])
    # wyzerowanie LSB i ustawienie nowego bitu
    flat_cover[i] = (flat_cover[i] & 254) | bit
    
  stego_image = flat_cover.reshape(cover.shape)
  cv2.imwrite(output_path, stego_image)
  print(f"Ukryto wiadomość w {output_path}")
  
def extract(stego_path, message_length):
  stego = cv2.imread(stego_path, cv2.IMREAD_UNCHANGED)
  
  if stego is None:
    raise FileNotFoundError(f"Nie znaleziono obrazu {stego_path}")
  
  flat_stego = stego.flatten()
  
  message = ""
    
  for i in range(message_length):
    byte_value = 0
    for j in range(8):          
        bit = flat_stego[i * 8 + j] & 1            
        byte_value |= (bit << (7 - j))
    message += chr(byte_value)
    
  return message

def calculate_psnr(img1_path, img2_path, max_value=255):
    """"Calculating peak signal-to-noise ratio (PSNR) between two images."""
    img1 = cv2.imread(img1_path, cv2.IMREAD_UNCHANGED)
    img2 = cv2.imread(img2_path, cv2.IMREAD_UNCHANGED)
    mse = np.mean((np.array(img1, dtype=np.float32) - np.array(img2, dtype=np.float32)) ** 2)
    if mse == 0:
        return 100
    return 20 * np.log10(max_value / (np.sqrt(mse)))


if __name__ == "__main__":
    
    message = input("Podaj wiadomość do zaszyfrowania: ").strip()
    
    message_len = len(message)
    
    embed("cover.png", message, "stego.png")
    
    decrypted = extract("stego.png", message_len)
    print("Odszyfrowana wiadomość:", decrypted)
    print("PSNR pomiędzy obrazami:",calculate_psnr("cover.png", "stego.png", max_value=255))
