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

You can easily adapt [the import script](../lib/ImportExport.py) to any format.

## Usage

```
./vault.py --import_items path/to/file.json
```

## Sample import file

```json
[
	{
		"category": 0,
		"name": "some item",
		"login": "gab@notarealemail.com",
		"password": "password1",
		"notes": "my notes\nmore notes"
	},
	{
		"category": 1,
		"name": "some other item",
		"login": "one@notarealemail.com",
		"password": "password2",
		"notes": "notes"
	},
	{
		"category": 3,
		"name": "another kind of item",
		"login": "two@notarealemail.com",
		"password": "password3 is very complicated!",
		"notes": "sdasd"
	},
	{
		"category": 0,
		"name": "my stuff",
		"login": "three@notarealemail.com",
		"password": "password4 is even more complicated!",
		"notes": ""
	},
	{
		"category": null,
		"name": "multi line item",
		"login": "foor@notarealemail.com",
		"password": "password5",
		"notes": "multi\nline\nitem"
	}
]
```