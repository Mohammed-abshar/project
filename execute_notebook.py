import nbformat
from nbclient import NotebookClient

with open('Healthcare_Cloud_Cost_Intelligence.ipynb', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

client = NotebookClient(nb, timeout=600, kernel_name='python3')
try:
    client.execute()
    print("Notebook executed successfully.")
except Exception as e:
    print(f"Error during execution: {e}")

with open('Healthcare_Cloud_Cost_Intelligence.ipynb', 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)
