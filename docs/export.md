# Vault: export

Exporting items is easy. You just have to use the flag `--export`.

## Security notice

For obvious reasons, **export files are not encrypted**, all the vault secrets will be stored in clear.
Make sure to safely store the export file and securely dispose it after its use.

## Usage

```
./vault.py --export path/to/file.json
```

## Export sample

See [export sample](../sample/export.json).
