# Vault: rebuild the vault

If for some reason you wanted to completely rebuild your vault (for example to make bulk changes), here is how to proceed.

## Rebuilding the vault

Process to rebuild the vault:

 - Export all secrets
 - Delete the vault
 - Create a new vault and import the secrets

## How to proceed

### Export all secrets
```
./vault.py --export all.json
# ...type master key
```

### Write down the list of categories

Open the vault and take note of all categories and their IDs.
At this time, categories cannot be exported and imported automatically.

```
./vault.py
# ...type master key
# ...type 'cat'
# ...write down all categories
```

### Delete the vault and configuration file

```
./vault.py --erase_vault
# ...type 'y' to confirm
```

### Setup a new vault

```
./vault.py
# Choose a new master key and confirm
# and unlock the vault
```

### Re-create the categories

```
# ...type 'cat'
# ...re-create the categories (make sure they have the same IDs)
```

### Re-import all the secrets

```
./vault.py --import_items all.json
# ...type master key
# ...review list and type `y` to confirm import
```
