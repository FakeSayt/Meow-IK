# HAH Outlet — bezpośrednie śledzenie przesyłki

Poprawka do wcześniejszej paczki zamówień/filtrów. Wgraj oba pliki z folderu `hahoutlet/` do istniejącego sklepu, zastępując starsze: `mail_templates.php` i `order_fulfillment.php`.

Link w nowym mailu o wysyłce (HTML oraz wersji tekstowej) i w panelu administratora ma postać `https://www.epaka.pl/sledzenie-przesylek/NUMER`, gdzie NUMER pochodzi z pola numeru przesyłki. Zachowuje zera na początku. Znaki specjalne są kodowane jako jeden fragment adresu URL.

Nie trzeba importować SQL. Wcześniej wysłane wiadomości pozostają bez zmian. Testy sprawdzają generowany adres; nie weryfikują statusu rzeczywistej paczki w ePaka.
