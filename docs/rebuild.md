# Vault: rebuild the vault

If for some reason you wanted to completely rebuild your vault, here is how to proceed.

## Why rebuild the vault?

Here are some use cases tor rebuild the vault:

 - Rebuilding the vault is the only solution to change the configuration file salt
 - Make bulk changes

## Rebuilding the vault

Process to rebuild the vault:

 - Export the vault to a native file format
 - Import the native file to the new vault

## Security notice

For obvious reasons, **export files are not encrypted**, all the vault secrets will be stored in clear.
Make sure to safely store the export file and securely dispose of it after its use.

## How to proceed

### Backup the vault and configuration file

Importing and exporting is experimental, please backup the vault and configuration file before proceeding.

### Export the vault

```
vault --export vault.native --file_format native
# ...type master key
```

### Import the vault

```
vault --import_items vault.native --file_format native
# ...type master key
# ...confirm
```
