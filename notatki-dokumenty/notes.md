---
title: "NOTES - PROJEKT GRUPOWY"
geometry: "left=2cm,right=2cm,top=3cm,bottom=3cm"
---


## Sprzęt

1. nRF52840 Dongle 
    - nadajnik bluetooth

1. nRF52833-DK
    - mikrokontroler do reflektorów/direktorów
 
1. Particle Argon 
    - odczyt przez antenę

1. MCP23018 
    - I2C ekspander GPIO na antenie

1. Antena ESPAR


## Założenia w skrócie

* Nadajemy sygnał przez dongle
* podpinamy nordic-DK w celu zmiany direktorów/reflektorów
* przez Argon zczytujemy sygnał z anteny, badamy kiedy jest najsilniejszy 


## Zadania

- połączenie nordic - MCP
    * Przygotowanie środowiska do pracy z Nordiciem, prosty hello world
    * Realizacja wymiany najprostszych komunikatów z MCP
    * Opracowanie API do obsługi direktorów 

- połączenie Argon - antena

- nadajnik bluetooth


## ESPAR

Rotowanie pięcioma direktorami działa, możnaby ew. uporządkować kod i 
przygotować na odbiór statusu z Argona i zatrzymywanie się na danej pozycji
dla najlepszego sygnału

**Proponowany algorytm**

* ESPAR obraca się
* dla każdej pozycji odbiera i przypisuje z Argona poziom sygnału
* po obrocie o 360st typuje maksimum i ustawia się do pozycji z przypisanym
    tym właśnie maksimum
* ew. dalej pobiera dane z Argona i patrzy, czy poziom sygnału nie zmienia się;
    w wypadku zmiany poniżej X% ponownie przechodzi do skanowania 


## Particle Argon

Będzie miał podpiętą antenę i odbierał przez nią sygnał z nadajnika.
Teoretycznie do "łatwego" programowania po USB przez webowe IDE. 

Praktycznie:

### Pierwszy status

Argon po USB świecił na stały kolor, co wskazywało na problem z wgranym kodem. 
Nie wykrywał się nigdzie w Linuksie ani Windowsie, tym bardziej w aplikacjach
webowych particle.io.

### Drugi status

Po przewaleniu połowy internetu, udało się trafić na stockowy firmware na 
oficjalnej stronie, oraz na komendę na zapyziałym forum do "ręcznego" wgrywania
hexów, korzystając z J-Linka w NRF52-DK po połączeniu tasiemką:

```
 nrfjprog -f NRF52 --program argon.hex --chiperase --reset
```

Od tego momentu Argon miga na spodziewany kolor, wykrywa się w systemach jako
urządzenie blokowe ("jakby pendrive") i wykrywa się też w webowej aplikacji 
do programowania. Aplikacja jest w stanie się z nim komunikować, zmieniać mu 
stan (kolor diody). 

Problem w tym, że na którymś etapie zestawiania w tej 
aplikacji "traci połączenie" i każe zaczynać od początku. Skoro np. aplikacja 
na Androida przestała działać i wycofali ją ze sklepu, to pewnie nie są 
najlepsi w te klocki i webowa aplikacja też się po prostu popsuła.

Trzeba będzie go więc ręcznie programować przez w/w komendę, podpiętego do 
NRF52-DK. Tak też chyba robili to ci technicy z PG. Do tego potrzeba będzie 
znaleźć dla niego konkretny toolchain/SDK.

**Zadania**

* poczytaj o samym argonie, jaki mikrokontroler tam siedzi, co to za 
    architektura
* poszukaj albo "particle argon toolchain/SDK" albo toolchain/SDK dla 
    technicznej nazwy uc jaki tam siedzi - być może to jakiś nordic soc

### Ważne

Factory reset
```
1. Begin holding the MODE button down.
2. While holding the MODE button down, tap the RESET button briefly.
3. After 3 seconds the core will begin blinking yellow, KEEP HOLDING the MODE button.
4. After 10 seconds the core will begin blinking white. When this happens the factory reset process has begun. Let go of the MODE button.
5. When it stops blinking white, it should begin blinking blue, indicating that it is listening for WiFi credentials.
```

```
Device ID: e00fce68812c878ef08a8c68
Device Secret: G8F5XFL7SGTL8JN
Serial Number: ARNHAD2142DVAKL
```

**ZADZIAŁAŁO:**

* factory reset
* `particle setup`
* `particle serial --wifi`
* `Particle: Cloud flash`
* `Particle: Flash device for debug` 
* `particle list`

[claiming guide](https://diotlabs.daraghbyrne.me/docs/getting-started/4-claim-it/) 


### Trzeci status

Udało się przeflashować basic program testowy migający D7 i dający output
po serialu. W takim razie - można zacząć pracę nad

- odczytem sygnału z koncentryka
- komunikacją (jakąś) z NRF52-DK


## Pytania

* Jak chcemy realizować połączenie między argonem a nordiciem - serial?

