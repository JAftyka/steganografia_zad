# steganografia_zad

## Program korzysta z biblioteki OpenCV do obsługi plików w formacie PNG oraz z biblioteki NumPy do obliczania PSNR. 

## Przykład działania programu

Oryginalny obraz:
![steganografia_zad/cover.png](https://github.com/JAftyka/steganografia_zad/blob/main/cover.png?raw=true)

Obraz po zaszyfrowaniu wiadomości:
![steganografia_zad/stego.png](https://github.com/JAftyka/steganografia_zad/blob/main/stego.png?raw=true)

PSNR między tymi obrazami wynosi: 70.38911.

## Maksymalna pojemność

Wzór na maksymalną pojemność:

$$ \text{Pojemność} = \frac{\text{Szerokość} \times \text{Wysokość} \times \text{Liczba kanałów}}{\text{Liczba bitów na znak}} $$
