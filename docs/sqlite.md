# SQLite Tips

There are some settings that can be tuned for performance or compatibility.

## `PRAGMA foreign_keys = ON;`

[Foreign Key](https://sqlite.org/foreignkeys.html) constraints must be enabled per connection, and there is no reason not to.

## `PRAGMA journal_mode = wal;`

[WAL mode](https://sqlite.org/wal.html) improves performance, but there are some downsides. This creates a couple of additional files alongside the database that should always be kept together. It cannot be used with databases over the network. The WAL can sometimes grow excessively, deteriorating performance.

## `PRAGMA synchronous = normal;`

[Synchronous](https://sqlite.org/pragma.html#pragma_synchronous) mode can performance. When operating with WAL, this is the recommended mode.

## `PRAGMA temp_store = memory;`

Improve performance at the expense of [memory usage](https://sqlite.org/pragma.html#pragma_temp_store).

## `PRAGMA mmap_size = 268435456;`

Use [memory-mapped I/O](https://www.sqlite.org/mmap.html) to improve performance and reduce memory usage. The value is the maximum database size that will be memory-mapped (256 MiB).

## `PRAGMA threads = 4;`

Use additional [helper threads](https://sqlite.org/pragma.html#pragma_threads) to improve performance.

## `PRAGMA secure_delete = on;`

[Overwrite deleted content](https://sqlite.org/pragma.html#pragma_secure_delete) with zeros. This is somewhat ineffective on solid state storage which uses flash translation layers.

## `PRAGMA trusted_schema = on;`

[Increase security](https://www.sqlite.org/pragma.html#pragma_trusted_schema).

## `PRAGMA recursive_triggers = on`

[Recursive triggers](https://www.sqlite.org/pragma.html#pragma_recursive_triggers) may be enabled.

## TODO

- [shared cache mode]https://sqlite.org/sharedcache.html? (probably slower)
- `pragma optimize;` on connection close
- `pragma vacuum;` sometimes (or auto_vacuum=incremental) - if expecting shrinkage.
- `pragma locking_mode;` maybe

## References

1. <https://phiresky.github.io/blog/2020/sqlite-performance-tuning/>
2. <https://manski.net/2012/10/sqlite-performance/>
