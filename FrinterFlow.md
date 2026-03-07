# Frinter Stylistics & FrinterFlow CLI Guidelines

Ten dokument stanowi pełny obraz stylistyki **Frintera**, z naciskiem na stworzenie spójnego wizualnie narzędzia **FrinterFlow CLI** oraz innych nowych projektów. Stylistyka opiera się na estetyce "Retro Pixel" z wyraźną, stonowaną i wyrazistą paletą barw używaną m.in. w sesjach skupienia.

## 1. Główne Kolory (The 3 Core Colors)

Frinter opiera się na semantyce trzech głównych barw, z których każda odpowiada określonej kategorii zadań. W nowym projekcie CLI (oraz innych realizacjach), barw tych należy używać jako wiodących akcentów:

*   **Rozkwit (Turkus) – `#4a8d83`**
    *   *Ikona:* **Drzewko** (Symbol wzrostu i natury)
    *   *Znaczenie:* Rozwój osobisty, journaling, czytanie, świadomość, aktywność fizyczna.
    *   *Zastosowanie w CLI:* Komunikaty sukcesu, statusy działania, standardowe powiadomienia zdrowotne, proste statystyki.
*   **Relacje (Fiolet) – `#8a4e64`**
    *   *Ikona:* **Serce** (Symbol więzi społecznych)
    *   *Znaczenie:* Relacje z ludźmi, spotkania, zaangażowanie społeczne.
    *   *Zastosowanie w CLI:* Przypomnienia o kontakcie, sekcje współpracy, wyróżnienia logów systemowych związanych z użytkownikami.
*   **Praca Głęboka (Żółty/Złoty) – `#d6b779`**
    *   *Ikona:* **Mózg** (Symbol skupienia i wysiłku intelektualnego)
    *   *Znaczenie:* Praca w pełnym skupieniu, wymagająca głębokiej koncentracji.
    *   *Zastosowanie w CLI:* Tryb focus/sprint ("Pomodoro"), ostrzeżenia (uwaga), podświetlenia ważnych błędów, output z zadań wymagających najwyższej uwagi.
*   **Frint_bot (Zunifikowany Asystent)**
    *   *Ikona:* **Robot Pixel Art** (Zbudowany z 3 kolorów głównych: podstawa/ciało w Turkusie `#4a8d83`, oczy w Fiolecie `#8a4e64`, detale jak antena czy usta w Złocie `#d6b779`)
    *   *Znaczenie:* Wbudowany przewodnik, asystent i uosobienie systemu.
    *   *Zastosowanie w CLI:* Ekran powitalny, tryb pomocy (help / tour), interaktywne zapytania CLI, wyświetlanie podpowiedzi.

## 2. Retro Pixel Animation (Rozkład na czynniki)

Komponent `RetroPixelAnimation.tsx` stanowi serce motywu czasomierza Frintera. Buduje on klimat nostalgiczny i uspokajający. W przypadku przenoszenia tego do środowiska CLI lub terminala w nowym projekcie (np. w postaci znaków ASCII lub własnych wtyczek terminala z Canvasem), należy zwrócić uwagę na następujące cechy:

### A. Elementy graficzne i Skalowanie
Komponent wykorzystuje technikę rysowania piksel po pikselu z włączonym `image-rendering: 'pixelated'`, żeby uniknąć rozmyć. Rozdzielczość to celowo zaniżone **192x64 px**, aby powiększone bloki symulowały konsolowy, 16-bitowy feeling.
*   **Sprite'y (Obiekty):** Rysowane w prostej matrycy (ok. 12x12). Drzewo dla turkusu, serce dla fioletu, mózg dla złotego. Składają się z dwóch kolorów: koloru głównego (np. `#4a8d83`) i białego, lekko przezroczystego highlightu (`#ffffff80`). Wyjątkiem jest `Frint_bot`, który jako maskotka aplikacji łączy wszystkie trzy podstawowe kolory w jednej matrycy (ciało turkusowe, oczy fioletowe, detale i promienie złote). W CLI można to oddać stosując znaki blokowe o różnej gęstości (np. `█` oraz `░`).

### B. Matryce Pikseli (Kody Ikon)
Z racji tworzenia CLI, poniżej znajdują się dokładne wzory matryc do przeniesienia (tablice dwuwymiarowe, w których każda liczba oznacza odpowiedni kolor lub jego brak):

*   `0` – puste (transparentne)
*   `1` – główny kolor (turkus, fiolet, złoto dla pierwszych trzech; dla bota: turkus jako dół, złoto dla niektórych detali itp., patrz niżej)
*   `2` – kolor "highlight" (np. biały lekko przezroczysty) lub w przypadku Bota - fiolet.
*   `3` – dla Bota: kolor złoty (promienie energii / antena)

```javascript
const SPRITES = {
  tree: [
    [0,0,0,0,1,1,1,1,0,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,0,0],
    [0,1,1,1,2,2,1,1,1,1,1,0],
    [1,1,1,1,2,2,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,2,2,1,1,1],
    [0,1,1,1,1,1,1,2,2,1,1,0],
    [0,0,1,1,1,1,1,1,1,1,0,0],
    [0,0,0,0,1,1,0,0,0,0,0,0],
    [0,0,0,0,1,1,0,0,0,0,0,0],
    [0,0,0,0,1,1,0,0,0,0,0,0],
    [0,0,0,1,1,1,1,0,0,0,0,0],
    [0,0,1,1,1,1,1,1,0,0,0,0],
  ],
  heart: [
    [0,0,1,1,1,0,0,0,1,1,1,0,0],
    [0,1,1,1,1,1,0,1,1,1,1,1,0],
    [1,1,1,2,2,1,1,1,1,1,1,1,1],
    [1,1,1,2,2,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1],
    [0,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,0,1,1,1,1,1,1,1,1,1,0,0],
    [0,0,0,1,1,1,1,1,1,1,0,0,0],
    [0,0,0,0,1,1,1,1,1,0,0,0,0],
    [0,0,0,0,0,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,0],
  ],
  brain: [
    [0,0,0,1,1,1,1,1,1,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,0,0],
    [0,1,1,2,2,1,1,1,2,2,1,0],
    [1,1,1,2,2,1,1,1,2,2,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,2,2,2,2,1,1,1,1,1],
    [0,1,1,1,1,1,1,1,1,1,1,0],
    [0,0,1,1,1,0,0,1,1,1,0,0],
    [0,0,0,1,1,0,0,1,1,0,0,0],
  ],
  bot: [
    [0,0,0,3,3,3,3,3,3,0,0,0],
    [0,0,0,0,0,3,3,0,0,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,2,2,1,1,2,2,1,1,0],
    [0,1,1,2,2,1,1,2,2,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,3,3,3,3,3,3,1,1,0],
    [0,0,1,1,1,1,1,1,1,1,0,0],
    [0,0,0,1,1,1,1,1,1,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,0,0],
    [0,0,1,1,0,0,0,0,1,1,0,0],
  ]
};
```

### C. Animacja (The Vibe)
Ruch w systemie jest powolny i celowo zaprojektowany, by nie rozpraszać w trakcie Pracy Głębokiej:
1.  **Paralaksa:** Pojawiają się dwie warstwy prędkości – obiekty "pierwszoplanowe" i drobne "gwiazdki/punkty" przemieszczające się jako tło. Szybkość to np. zaledwie `0.05` dla tła oraz `0.1` dla pierwszego planu.
2.  **Delikatny Bobbinging:** Obiekty lekko unoszą się w górę i dół (wykorzystując funkcję sinus). Ta delikatna sinusoida "ożywia" scenę bez inwazyjnej dynamiki – doskonałe do konsolowych progress-barów czy wskaźników długiego ładowania w CLI.

### C. Podłoże (The Grid / Scanlines)
Zastosowana jest klasyczna zasada perspektywy "synthwave / retro":
*   **Ruchoma podłoga:** Pionowe markery na dole ekranu, symulujące ruch poprzez przesuwanie w lewo.
*   **Scanline Overlay:** Kompozycja wykorzystuje efekt pasków kineskopowych (scanlines), dodając linearny gradient (opacity 5-10% i szerokości powtórzenia 4px) u góry nałożonego kontenera.
*   **W CLI:** Ten element można odtworzyć stosując znak podkreślenia (np. poruszające się `_` lub `-` w trybie pętli znakowej) lub symulować przeplatanie tła (parzyste linie terminala ciut ciemniejsze od nieparzystych).

## 3. Przełożenie punktów na FrinterFlow CLI

Budując nowe środowisko CLI, dąż do uzyskania efektu nostalgicznego retro, bez wchodzenia w sterylną szarość:

1.  **Kolory Terminala:** Przesłoń standardowe kolory ANSI. Niech "Success" będzie odzwierciedleniem `#4a8d83`, niech "Info" lub "Focus" stają się `#d6b779`.
2.  **Elementy Interfejsu (Layout):** Wszelkie loadery i progress bary implementuj z wolnym tempem, zastępując domyślne kropki czy wirujące kreski animacjami "block bouncingu" lub wolno kręcącą się ikonką przypominającą pixel-arta.
3.  **Czystość:** Nawet pomimo retro-stylistki animacji, ramki obiektów czy wykończenie terminala musi być maksymalnie czytelne i minimalistyczne (np. boxy w terminalu powinny unikać podwójnych zawiłych krawędzi, preferując jednorodne bloki bezszwowe). 

Zastosowanie tych zasad gwarantuje spójność tożsamości Frintera z narzędziami deweloperskimi terminala (FrinterFlow CLI).
