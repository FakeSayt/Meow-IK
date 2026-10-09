# HAH Outlet — zamówienia, wysyłka, e-maile, voucher i LIVE

Aktualizacja na podstawie przesłanego `new.zip`. Wgraj ją do istniejącego sklepu.

## Wgranie

1. Zrób kopię plików sklepu i bazy danych przed aktualizacją.
2. Rozpakuj `HAH-Outlet-zamowienia-live-maile.zip`.
3. Wgraj wszystkie 10 plików z folderu `hahoutlet/` do `public_html/hahoutlet/`, zastępując istniejące i dodając nowe. Wgraj komplet razem.
4. Nie podmieniaj konfiguracji `private/`, sesji ani katalogu `uploads/`. Nie importuj ponownie starego SQL.
5. Otwórz panel i odśwież Ctrl+F5. Bootstrap automatycznie dodaje potrzebne kolumny do tabeli zamówień; istniejące produkty i zamówienia zostają zachowane. Użytkownik bazy musi mieć uprawnienie ALTER, podobnie jak przy dotychczasowych aktualizacjach sklepu.

Pliki zastępowane: `admin.php`, `api.php`, `app.js`, `bootstrap.php`, `design.css`, `index.php`, `prywatnosc.php`, `voucher_template.php`.

Nowe pliki: `mail_templates.php`, `order_fulfillment.php`.

## Obsługa zamówień

1. Oczekujące zamówienie: kliknij **Potwierdź wpłatę** po faktycznym zaksięgowaniu przelewu.
2. Opłacone zamówienie: kliknij **Kompletuj zamówienie**.
3. Przy kompletowaniu sprawdź e-mail odbiorcy, wpisz przewoźnika i numer przesyłki.
4. Po nadaniu kliknij **Oznacz jako wysłane i wyślij e-mail**.

Przy nowych zamówieniach e-mail zapisuje się automatycznie. Przy starszych trzeba wpisać go w formularzu wysyłki, na podstawie wiadomości z zamówieniem. Dane adresowe nadal znajdują się w wiadomości do sklepu, nie w tabeli zamówień.

Stan magazynowy jest odejmowany wyłącznie przy potwierdzeniu wpłaty. Kompletowanie i wysyłka nie odejmują go ponownie. Licznik opłaconych zamówień i przychód obejmują także zamówienia kompletowane i wysłane.

E-mail wysyłkowy zawiera numer zamówienia, pozycje, kwotę, przewoźnika, numer przesyłki i przycisk do strony ePaka. Numer należy wpisać na stronie śledzenia; aktualizacja nie zamawia kuriera ani nie tworzy etykiet.

Jeśli hosting odrzuci wiadomość, zamówienie pozostaje oznaczone jako wysłane. W tabeli pojawi się możliwość **Ponów e-mail**. Po zaakceptowaniu wiadomości przez pocztę kolejne kliknięcie nie wyśle jej ponownie. Przekazanie wiadomości do poczty nie potwierdza jej doręczenia klientowi. Próba przerwana w trakcie wysyłania może być ponowiona po pięciu minutach; sprawdź stan poczty przed ręcznym ponowieniem.

## Wygląd wiadomości i vouchery

Potwierdzenie zakupu dla klienta i informacja dla sklepu mają szablon kremowo-bordowy. Wiadomości zawierają też wersję tekstową. Dane do przelewu, sprzedawcy, termin rezerwacji i informacje o zakupie pozostają w potwierdzeniu.

Voucher pokazuje rzeczywisty tytuł i dedykację zamiast dosłownych `$title` i `$dedication`. Podgląd i wysyłany e-mail korzystają z tego samego szablonu; długie kody mieszczą się na telefonie.

W **Ustawieniach** zmień pole **Adres sklepu w e-mailach i voucherach**. Domyślny adres: https://autobothub.pl/hahoutlet/index.php. Zmiana dotyczy przyszłych wiadomości i aktualnego podglądu; wcześniej wysłanych e-maili nie da się zmienić.

Folder `podglady/` zawiera przykładowe wiadomości HTML i PNG na fikcyjnych danych, w tym przykładowy rachunek bankowy. Nie wgrywaj tego folderu jako konfiguracji sklepu.

## Facebook LIVE

Główny przycisk otwiera transmisję bezpośrednio na Facebooku. W sklepie nadal działają kody, produkty i rezerwacje LIVE. W panelu wpisuj bezpośredni link do publicznego filmu lub transmisji.

Odtwarzacz na stronie uruchamia się dopiero po kliknięciu **Spróbuj oglądać na tej stronie**. Gdy Brave, Firefox lub Facebook blokuje osadzenie, nadal działa główny przycisk do Facebooka. Aktualizacja nie omija zabezpieczeń przeglądarki ani ograniczeń Meta i nie obiecuje odtwarzania osadzonego filmu w każdej przeglądarce.

## Baza i poprzednia wersja

Aktualizacja dodaje kolumny, nie usuwa danych. Po rozpoczęciu używania nowych etapów starszy panel może nie rozpoznawać statusów `packing` i `shipped`. Zachowaj kopię sprzed aktualizacji; nie przywracaj starej bazy w sposób, który usunąłby późniejsze zamówienia.

Zmiany przygotowano i przetestowano lokalnie. Paczkę trzeba wgrać na hosting; rzeczywiste doręczanie e-maili i możliwość osadzania konkretnego filmu Facebooka sprawdza się na docelowym serwerze.
