## Bảng: InvoiceLine
### Schema:
- InvoiceLineId (INTEGER) [PK]
- InvoiceId (INTEGER)
- TrackId (INTEGER)
- UnitPrice (NUMERIC(10,2))
- Quantity (INTEGER)

### Sample Data:
|   InvoiceLineId |   InvoiceId |   TrackId |   UnitPrice |   Quantity |
|----------------:|------------:|----------:|------------:|-----------:|
|               1 |           1 |         2 |        0.99 |          1 |
|               2 |           1 |         4 |        0.99 |          1 |
|               3 |           2 |         6 |        0.99 |          1 |
|               4 |           2 |         8 |        0.99 |          1 |
|               5 |           2 |        10 |        0.99 |          1 |