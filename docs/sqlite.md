# SQLite Tips

- `PRAGMA foreign_keys = ON;` (per connection)
- `PRAGMA mmap_size pragma = 268435456` (ALL connections; CAVEATS!)
- multithreading... how?
- shared cache mode...?
- `PRAGMA journal_mode=WAL;` WAL (not over network; not for read-heavy)
