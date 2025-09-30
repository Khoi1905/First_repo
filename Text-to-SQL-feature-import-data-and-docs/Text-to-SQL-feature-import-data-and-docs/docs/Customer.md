## Bảng: Customer
### Schema:
- CustomerId (INTEGER) [PK]
- FirstName (NVARCHAR(40))
- LastName (NVARCHAR(20))
- Company (NVARCHAR(80))
- Address (NVARCHAR(70))
- City (NVARCHAR(40))
- State (NVARCHAR(40))
- Country (NVARCHAR(40))
- PostalCode (NVARCHAR(10))
- Phone (NVARCHAR(24))
- Fax (NVARCHAR(24))
- Email (NVARCHAR(60))
- SupportRepId (INTEGER)

### Sample Data:
|   CustomerId | FirstName   | LastName    | Company                                          | Address                         | City                | State   | Country        | PostalCode   | Phone              | Fax                | Email                    |   SupportRepId |
|-------------:|:------------|:------------|:-------------------------------------------------|:--------------------------------|:--------------------|:--------|:---------------|:-------------|:-------------------|:-------------------|:-------------------------|---------------:|
|            1 | Luís        | Gonçalves   | Embraer - Empresa Brasileira de Aeronáutica S.A. | Av. Brigadeiro Faria Lima, 2170 | São José dos Campos | SP      | Brazil         | 12227-000    | +55 (12) 3923-5555 | +55 (12) 3923-5566 | luisg@embraer.com.br     |              3 |
|            2 | Leonie      | Köhler      |                                                  | Theodor-Heuss-Straße 34         | Stuttgart           |         | Germany        | 70174        | +49 0711 2842222   |                    | leonekohler@surfeu.de    |              5 |
|            3 | François    | Tremblay    |                                                  | 1498 rue Bélanger               | Montréal            | QC      | Canada         | H2G 1A7      | +1 (514) 721-4711  |                    | ftremblay@gmail.com      |              3 |
|            4 | Bjørn       | Hansen      |                                                  | Ullevålsveien 14                | Oslo                |         | Norway         | 0171         | +47 22 44 22 22    |                    | bjorn.hansen@yahoo.no    |              4 |
|            5 | František   | Wichterlová | JetBrains s.r.o.                                 | Klanova 9/506                   | Prague              |         | Czech Republic | 14700        | +420 2 4172 5555   | +420 2 4172 5555   | frantisekw@jetbrains.com |              4 |