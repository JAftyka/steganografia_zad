import math
import io
from PIL import Image


def calc_max_message_length(image_path):
    cover = Image.open(image_path)
    height, width = cover.size[1], cover.size[0]
    channels = len(cover.getbands())
    return (height * width * channels)//8
  
  
def embed(image_path, message, output_path):
    cover = Image.open(image_path)
    if cover.mode not in ('RGB', 'RGBA'):
        cover = cover.convert('RGB')
    
    message_bits = ''.join(format(ord(char), '08b') for char in message)
    num_bits = len(message_bits)
    
    flat_cover = [channel for pixel in cover.get_flattened_data() for channel in pixel]

    if num_bits > len(flat_cover):
        raise ValueError("Wiadomość jest za długa!")
    
    for i in range(len(message_bits)):
        bit = int(message_bits[i])
        # wyzerowanie LSB i ustawienie nowego bitu
        flat_cover[i] = (flat_cover[i] & 254) | bit # 254 = 11111110
    
    channels = len(cover.getbands())
    new_pixels = []
    for i in range(0, len(flat_cover), channels):
        new_pixels.append(tuple(flat_cover[i:i+channels]))
    
    stego_image = Image.new(cover.mode, cover.size)
    stego_image.putdata(new_pixels)
    stego_image.save(output_path)
  
    print(f"Ukryto wiadomość w {output_path}")
  
  
def extract(stego_path, message_length):
    stego = Image.open(stego_path)
  
    flat_stego = [channel for pixel in stego.get_flattened_data() for channel in pixel]
  
    message = ""
    
    for i in range(message_length):
        byte_value = 0
        for j in range(8):          
            bit = flat_stego[i * 8 + j] & 1            
            byte_value |= (bit << (7 - j))
        message += chr(byte_value)
    
    return message


def calculate_psnr(img1_path, img2_path, max_value=255):
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)
    if img1.mode not in ('RGB', 'RGBA'): img1 = img1.convert('RGB')
    if img2.mode not in ('RGB', 'RGBA'): img2 = img2.convert('RGB')
    
    flat_1 = [channel for pixel in img1.get_flattened_data() for channel in pixel]
    flat_2 = [channel for pixel in img2.get_flattened_data() for channel in pixel]
    
    squared_errors = [(a - b) ** 2 for a, b in zip(flat_1, flat_2)]
    mse = sum(squared_errors) / len(squared_errors)
    
    if mse == 0:
        return 100
    return 20 * math.log10(max_value / (math.sqrt(mse)))


def test_jpeg_compression_impact(stego_path, original_message):
    stego_img = Image.open(stego_path)
    
    true_bits = ''.join(format(ord(char), '08b') for char in original_message)
    num_bits = len(true_bits)
    
    qualities = [95, 90, 75, 50, 25]
    
    print("\n=== WPŁYW KOMPRESJI JPEG NA POPRAWNOŚĆ WIADOMOŚCI ===")
    print(f"Długość testowanej wiadomości: {len(original_message)} znaków ({num_bits} bitów)\n")
    print(f"{'Jakość JPEG':<14} | {'Poprawnie odczytane bity':<25}")
    print("-" * 45)
    
    for q in qualities:
        jpeg_buffer = io.BytesIO()
        if stego_img.mode == 'RGBA':
            rgb_stego = stego_img.convert('RGB')
            rgb_stego.save(jpeg_buffer, format="JPEG", quality=q)
        else:
            stego_img.save(jpeg_buffer, format="JPEG", quality=q)
            
        jpeg_buffer.seek(0)
        compressed_img = Image.open(jpeg_buffer)
        
        flat_compressed = [channel for pixel in compressed_img.get_flattened_data() for channel in pixel]
        
        correct_bits_count = 0
        for i in range(num_bits):
            extracted_bit = flat_compressed[i] & 1
            expected_bit = int(true_bits[i])
            if extracted_bit == expected_bit:
                correct_bits_count += 1
                
        percentage = (correct_bits_count / num_bits) * 100
        print(f"{q:<14} | {correct_bits_count:<8} / {num_bits:<8} ({percentage:.2f}%)")


if __name__ == "__main__":
    #with open("example_message.txt") as f:
    #  message = f.read()
    message = input("Podaj wiadomość do zaszyfrowania (maks. długość: " + str(calc_max_message_length("cover.png")) + "): ").strip()
    
    message_len = len(message)
    
    embed("cover.png", message, "stego.png")
    
    decrypted = extract("stego.png", message_len)
    print("Odszyfrowana wiadomość:", decrypted)
    print("PSNR pomiędzy obrazami:",calculate_psnr("cover.png", "stego.png", max_value=255))
    
    test_jpeg_compression_impact("stego.png", message)
    
