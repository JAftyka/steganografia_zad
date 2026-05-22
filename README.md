# steganografia_zad

Program służy do ukrywania i odczytywania wiadomości tekstowych w obrazach (steganografia LSB). 
Projekt został napisany w Pythonie z wykorzystaniem biblioteki Pillow do obsługi plików PNG oraz modułu math do obliczania wskaźnika PSNR.

## Przykład działania programu

Oryginalny obraz:
![steganografia_zad/cover.png](https://github.com/JAftyka/steganografia_zad/blob/main/cover.png?raw=true)

Wiadomość: zawartość pliku example_message.txt

Obraz po zaszyfrowaniu wiadomości:
![steganografia_zad/stego.png](https://github.com/JAftyka/steganografia_zad/blob/main/stego.png?raw=true)

PSNR między tymi obrazami wynosi: 61.31729791520171.

## Maksymalna pojemność

Wzór na maksymalną liczbę znaków ASCII wiadomości:

$$ \text{Pojemność} = \frac{\text{Szerokość} \times \text{Wysokość} \times \text{Liczba kanałów}}{\text{Liczba bitów na znak}} $$

W przypadku przykładowego pliku cover.png, maksymalna długość wiadomości wynosi więc:

$$\frac{{1200} \times {901} \times {3}}{{8}} = {405450}$$
