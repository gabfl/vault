
import os, sys, json

class ImportExport:

    vault = None # Vault instance
    fileFormat = None # File format (default: 'json')
    path = None # Import of export path

    def __init__(self, vault, path, fileFormat = 'json'):
        self.vault = vault
        self.path = path
        self.fileFormat = fileFormat

    def importItems(self):
        """
            Routing to format specific import methods
        """

        if self.fileFormat == 'json':
            self.importFromJson()
        else:
            raise ValueError('%s is not a supported file format' % (self.fileFormat))

    def export(self):
        """
            Routing to format specific export methods
        """

        if self.fileFormat == 'json':
            self.exportToJson()
        else:
            raise ValueError('%s is not a supported file format' % (self.fileFormat))

    def importFromJson(self):
        """
            Import items to the vault
        """

        from lib.Misc import confirm

        # Unlock the vault with the existing key
        self.vault.unlock(False) # `False` = don't load menu after unlocking
        print()

        # Read import file
        fileContent = self.readFile()

        # Decode json
        items = json.loads(fileContent)
        # print (items)

        # Display items for confirmation
        results = []
        for i, item in enumerate(items):
            # Throw an error if the category is invalid
            if item['category'] and not self.vault.categoryCheckId(item['category']):
                print ("Category `%s` for item `%s`/`%s` is invalid" % (item['category'], item['name'], item['login']))
                print ("Please correct this error before proceeding.")
                sys.exit()

            # Add to import list
            results.append([
                i,
                self.vault.categoryName(item['category']),
                item['name'],
                item['login']
            ]);

        # If we have items
        if len(results) > 0:
            print("The following items will be imported:");

            # Show results table
            from tabulate import tabulate
            print()
            print (tabulate(results, headers=['Item', 'Category', 'Name / URL', 'Login']))

            # Request confirmation
            print()
            if confirm('Confirm import?', False):
                # Loop thru items
                for item in items:
                    # Import item
                    self.vault.addItem(str(item['category']), item['name'], item['login'], item['password'], item['notes']);

                    # Confirmation message
                    print ("* Item `%s`/`%s` has been imported" % (item['name'], item['login']))
        else:
            print("No items where found in the import file.");

        sys.exit()

    def exportToJson(self):
        """
            Export the vault content to a specific file
        """

        # Unlock the vault with the existing key
        self.vault.unlock(False) # `False` = don't load menu after unlocking

        # If we have a valid vault
        if self.vault.vault.get('secrets'):
            # Iterate thru the items
            output = []
            for item in self.vault.vault['secrets']:
                # Add to output
                output.append({
                    'category': item['category'],
                    'categoryName': self.vault.categoryName(item['category']),
                    'name': item['name'],
                    'login': item['login'],
                    'password': item['password'],
                    'notes': item['notes']
                });

            self.saveFile(json.dumps(output))
        else:
            print("There are no secrets in the vault.")

        sys.exit()

    def readFile(self):
        """
            Read an import file and return its content
        """

        # Read import file
        try:
            file = open(self.path)
            fileContent = file.read()
            file.close()

            return fileContent
        except Exception as e:
            print("The file `%s` could not be opened." % (self.path));
            print(e)
            sys.exit()

    def saveFile(self, content):
        """
            Save exported items to a file
        """

        # Save to file
        try:
            print("The vault has been exported to the file `%s`." % (self.path))

            file = open(self.path, 'w')
            file.write(content)
            file.close()
        except Exception as e:
            print("The vault could not be exported to the file `%s`." % (self.path))
            print(e)
