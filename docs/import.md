# Vault: import

Items can be imported with a Json array in the following format:

```json
[
    {
        "name": "Paypal",
        "url": "https://www.paypal.com",
        "login": "myemail@gmail.com",
        "password": "secret",
        "notes": "Some notes",
        "category": "Business items"
    }
]
```

You can easily adapt [the import script](../src/views/import_export.py) to any format.

## Usage

```
vault --import_items path/to/file.json
```

## Sample import file

See [import sample](../sample/export.json).
