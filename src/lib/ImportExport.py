
import sys
import json

from tabulate import tabulate

"""
    Adding import or export formats:

    To add an import or export format, you need to add a file format name to
    `self.importItems()` or `self.export()` and create an associated method
    called `importFrom[SomeFormat]()` or `exportTo[SomeFormat]()`.

    The format name must also be added to `../vault.py` in argparse choices.

    The easiest solution to create the import and/or export method would be to duplicate
    `self.importFromJson()` or `self.exportToJson()` as they are fairly standard.

    If you create a format that can be useful to others, please fork the project
    first and submit a merge request!
"""


class ImportExport:

    vault = None  # Vault instance
    fileFormat = None  # File format (default: 'json')
    path = None  # Import or export path

    def __init__(self, vault, path, fileFormat='json'):
        self.vault = vault
        self.path = path
        self.fileFormat = fileFormat

    def importItems(self):
        """
            Routing to format specific import methods
        """

        if self.fileFormat == 'json':
            self.importFromJson()
        elif self.fileFormat == 'native':
            self.importFromNative()
        else:
            raise ValueError('%s is not a supported file format' %
                             (self.fileFormat))

    def export(self):
        """
            Routing to format specific export methods
        """

        if self.fileFormat == 'json':
            self.exportToJson()
        elif self.fileFormat == 'native':
            self.exportToNative()
        else:
            raise ValueError('%s is not a supported file format' %
                             (self.fileFormat))

    def importFromJson(self):
        """
            Format: json
            Import items to the vault
        """

        from .Misc import confirm

        # Unlock the vault with the existing key
        self.unlockVault()
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
                print("Category `%s` for item `%s`/`%s` is invalid" %
                      (item['category'], item['name'], item['login']))
                print("Please correct this error before proceeding.")
                sys.exit()

            # Add to import list
            results.append([
                i,
                self.vault.categoryName(item['category']),
                item['name'],
                item['login']
            ])

        # If we have items
        if len(results) > 0:
            print("The following items will be imported:")

            # Show results table
            print()
            print(tabulate(results,
                           headers=['Item', 'Category', 'Name / URL', 'Login']))

            # Request confirmation
            print()
            if confirm('Confirm import?', False):
                # Loop thru items
                for item in items:
                    # Import item
                    self.vault.addItem(str(
                        item['category']), item['name'], item['login'], item['password'], item['notes'])

                    # Confirmation message
                    print("* Item `%s`/`%s` has been imported" %
                          (item['name'], item['login']))
        else:
            print("No items where found in the import file.")

        sys.exit()

    def importFromNative(self):
        """
            Format: native
            Replace the vault content with a native format import file
        """

        import pickle

        from .Misc import confirm

        # Unlock the vault with the existing key
        self.unlockVault()

        # Get import file content
        content = self.readFile('rb')

        # Unpickle the content
        content = pickle.loads(content)

        print()
        if confirm('Importing from a native format will erase and replace the vault content. Continue?', False):
            # Replace and save vault content
            self.vault.vault = content
            self.vault.saveVault()

            print("The vault has been imported.")

        sys.exit()

    def exportToJson(self):
        """
            Format: json
            Export the vault content to a file
        """

        # Unlock the vault with the existing key
        self.unlockVault()

        # Check if the vault has some content
        self.checkEmptyVault()

        # Iterate thru the items
        output = []
        for item in self.vault.getVault()['secrets']:
            # Add to output
            output.append({
                'category': item['category'],
                'categoryName': self.vault.categoryName(item['category']),
                'name': item['name'],
                'login': item['login'],
                'password': item['password'],
                'notes': item['notes']
            })

        self.saveFile(json.dumps(output))

        sys.exit()

    def exportToNative(self):
        """
            Format: native
            Export the vault content to a file
        """

        import pickle

        # Unlock the vault with the existing key
        self.unlockVault()

        # Check if the vault has some content
        self.checkEmptyVault()

        # Pickle the vault using the highest protocol available.
        output = pickle.dumps(self.vault.getVault(), pickle.HIGHEST_PROTOCOL)

        # Save to file
        self.saveFile(output, 'wb')

        sys.exit()

    def readFile(self, mode='r'):
        """
            Read an import file and return its content
        """

        # Read import file
        try:
            file = open(self.path, mode=mode)
            fileContent = file.read()
            file.close()

            return fileContent
        except Exception as e:
            print("The file `%s` could not be opened." % (self.path))
            print(e)
            sys.exit()

    def saveFile(self, content, mode='w'):
        """
            Save exported items to a file
        """

        # Save to file
        try:
            file = open(self.path, mode)
            file.write(content)
            file.close()

            print("The vault has been exported to the file `%s`." % (self.path))
        except Exception as e:
            print("The vault could not be exported to the file `%s`." %
                  (self.path))
            print(e)

    def unlockVault(self):
        """
            Ask user to unlock the vault
        """

        self.vault.unlock(False)  # `False` = don't load menu after unlocking

    def checkEmptyVault(self):
        """
            Will raise an error if the user tries to export an empty vault
        """

        if not self.vault.getVault().get('secrets'):
            raise ValueError(
                'There are no secrets in the vault stored at `%s`.' % (self.path))
