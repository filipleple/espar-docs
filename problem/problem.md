# Komunikacja między nordic nrf52833-DK a chipem MCP2018 na antenie

Między 52833-DK a chipem na antenie komunikujemy się, żeby ustawić direktory i
reflektory - czyli po prostu ustawić piny z nimi zwarte na stan niski albo
wysoki.

## MCP2018

MCP2018 to ekspander GPIO ( "przedłużacz pinów" ). Komunikacja jest po I2C,
można czytać i zapisywać do rejestrów. Jest 16 **GPIO** (czyli po prostu pinów,
które sobie ustawiamy na niski albo wysoki) w dwóch bankach (zestawach, jeden na
lewą drugi na prawą stronę chipa) **A i B**. 

Interesują nas rejestry:
* IODIRA i IODIRB - kierunek pina, input czy output
* GPIOA i GPIOB - faktyczny aktualny stan pina; jak mamy input to sczytujemy z
niego wartość pinów, jak output to też. Możemy do niego zapisywać, żeby ustawić
stan pina.
* OLATA i OLATB - jak mamy input, to tu ustawiamy/czytamy jaka ma być wartość po 
zmianie na output.

Każdy rejestr ma przypisany adres i posiada 8 bitów. Do wysyłania i odbierania 
danych jest gotowa funkcja.

### Zapis:

Podajemy w skrócie adres rejestru, dane jakie chcemy zapisać i ile bajtów tych
danych, do funkcji write.

Przykładowo:
```
i2c_buffer[0] = IODIRA_ADDR;
i2c_buffer[1] = 0xFF;
i2c_write(i2c0_device, i2c_buffer, 2, CHIP_I2C_ADDR);
```
wpisuje adres rejestru IODIRA i wartość 0xFF - czyli ustawia w rejestrze IODIRA
11111111.


### Odczyt:

Podajemy tylko adres rejestru do funkcji write, odpalamy funkcję read z 
parametrem ile bajtów chcemy odczytać.

Przykładowo:
```
i2c_buffer[0] = IODIRA_ADDR;
i2c_write(i2c0_device, i2c_buffer, 1, CHIP_I2C_ADDR);
i2c_read(i2c0_device, i2c_buffer, 1, CHIP_I2C_ADDR);
```
wpisuje adres IODIRA i sczytuje jego zawartość (jeden bajt)
