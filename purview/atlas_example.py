from azure.identity import AzureCliCredential

from pyapacheatlas.core import PurviewClient

cred = AzureCliCredential()

# Create a client to connect to your service.
client = PurviewClient(
    account_name = "purview-shared-tre",
    authentication = cred
)

!az login --tenant <id>

from pyapacheatlas.core.glossary import PurviewGlossaryTerm

default_glossary = client.glossary.get_glossary()

term = PurviewGlossaryTerm(
    name="This is my term 2",
    qualifiedName = "This is my term@Glossary",
    glossaryGuid = default_glossary["guid"],
    longDescription = "This is a long description",
    status = "Draft" # Should be Draft, Approved, Alert, or Expired
)

client.glossary.upload_term(term)
