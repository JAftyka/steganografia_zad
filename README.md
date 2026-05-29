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

---

## Maksymalna pojemność

Wzór na maksymalną liczbę znaków ASCII wiadomości:

<div align="center">

$$\text{Pojemność} = \frac{\text{Szerokość} \times \text{Wysokość} \times \text{Liczba kanałów}}{\text{Liczba bitów na znak}}$$

</div>

W przypadku przykładowego pliku cover.png, maksymalna długość wiadomości wynosi więc:

<div align="center">

$$\frac{1200 \times 901 \times 3}{8} = 405450$$

</div>

Dla obrazu RGB 256×256 będzie to z kolei:

<div align="center">

$$\frac{256 \times 256 \times 3}{8} = 24576$$

</div>

---

## Wyniki eksperymentów i raport

### 1. Porównanie wizualne i jakość (PSNR)
Obrazy `cover.png` oraz `stego.png` są całkowicie **nierozróżnialne dla ludzkiego oka**. Modyfikacja najmniej znaczącego bitu (LSB) zmienia składowe koloru piksela o maksymalnie 1 jednostkę w skali 0-255. 

Wyliczona wartość wskaźnika PSNR wynosi **~61.32 dB**. W cyfrowym przetwarzaniu obrazów wartości PSNR powyżej 40 dB oznaczają, że zniekształcenia wprowadzone do pliku są całkowicie pomijalne i niezauważalne wizualnie.

### 2. Wpływ kompresji stratnej (PNG → JPEG → PNG)
Próba zapisu obrazu stego do formatu JPEG (nawet przy wysokiej jakości, np. `quality=90`), a następnie ponowna próba ekstrakcji wiadomości kończy się **całkowitym niepowodzeniem**. Odczytana wiadomość staje się losowym ciągiem znaków, ponieważ LSB zostają utracone wskutek kompresji stratnej.

### 3. Tabela wpływu jakości kompresji JPEG
Eksperyment przeprowadzony dla testowej wiadomości o długości 21 znaków (168 bitów) dał następujące wyniki:

| Jakość zapisu JPEG | Poprawnie odczytane bity | Procentowy sukces |
| :---: | :---: | :---: |
| **95** | 88 / 168 | 52.38% |
| **90** | 90 / 168 | 53.57% |
| **75** | 88 / 168 | 52.38% |
| **50** | 80 / 168 | 47.62% |
| **25** | 88 / 168 | 52.38% |

### Wnioski końcowe
1. **Wrażliwość algorytmu LSB:** Metoda steganografii LSB jest skrajnie wrażliwa na jakiekolwiek przetwarzanie sygnału. Działa poprawnie **wyłącznie w formatach bezstratnych** (takich jak PNG lub BMP), które gwarantują, że zapisany na dysku bajt zachowa identyczną wartość po ponownym otwarciu pliku.
2. **Dlaczego JPEG niszczy LSB:** Algorytm kompresji JPEG wykorzystuje dyskretną transformację kosinusową (DCT) oraz kwantyzację. Jego zadaniem jest odrzucenie informacji o wysokich częstotliwościach (drobnych zmianach kolorystycznych), które i tak są niewidoczne dla oka. Ponieważ zmiana bitu LSB modyfikuje kolor zaledwie o $\pm 1$, kompresja stratna traktuje te dane jako szum i bezpowrotnie je nadpisuje/wygładza.
3. **Statystyczny przypadek (50%):** Wynik oscylujący w okolicach 50% poprawnie odczytanych bitów przy kompresji JPEG nie oznacza częściowego sukcesu. Wynika on czysto z rachunku prawdopodobieństwa – każdy uszkodzony bit przyjmuje wartość `0` lub `1`, więc losowo uszkodzona struktura pokrywa się z wiadomością dokładnie w połowie przypadków.
