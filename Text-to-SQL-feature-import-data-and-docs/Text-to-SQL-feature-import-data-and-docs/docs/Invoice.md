## Bảng: Invoice
### Schema:
- InvoiceId (INTEGER) [PK]
- CustomerId (INTEGER)
- InvoiceDate (DATETIME)
- BillingAddress (NVARCHAR(70))
- BillingCity (NVARCHAR(40))
- BillingState (NVARCHAR(40))
- BillingCountry (NVARCHAR(40))
- BillingPostalCode (NVARCHAR(10))
- Total (NUMERIC(10,2))

### Sample Data:
|   InvoiceId |   CustomerId | InvoiceDate         | BillingAddress          | BillingCity   | BillingState   | BillingCountry   | BillingPostalCode   |   Total |
|------------:|-------------:|:--------------------|:------------------------|:--------------|:---------------|:-----------------|:--------------------|--------:|
|           1 |            2 | 2009-01-01 00:00:00 | Theodor-Heuss-Straße 34 | Stuttgart     |                | Germany          | 70174               |    1.98 |
|           2 |            4 | 2009-01-02 00:00:00 | Ullevålsveien 14        | Oslo          |                | Norway           | 0171                |    3.96 |
|           3 |            8 | 2009-01-03 00:00:00 | Grétrystraat 63         | Brussels      |                | Belgium          | 1000                |    5.94 |
|           4 |           14 | 2009-01-06 00:00:00 | 8210 111 ST NW          | Edmonton      | AB             | Canada           | T6G 2C7             |    8.91 |
|           5 |           23 | 2009-01-11 00:00:00 | 69 Salem Street         | Boston        | MA             | USA              | 2113                |   13.86 |