# Vault: import

Items can be imported with a Json array in the following format:

```json
[
	{
		"category": 0,
		"name": "My item name",
		"login": "My login",
		"password": "Super secret password",
		"notes": "my notes\nmore notes"
	}
]
```

You can easily adapt [the import script](../src/lib/ImportExport.py) to any format.

## Usage

```
vault --import_items path/to/file.json
```

## Sample import file

See [import sample](../sample/import.json).
