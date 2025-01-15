# How to prepare data for logging

To prepare the metadata, it is required to fetch such information from online service and create a list of dataset 'siat_trentino' in the project context 

1. Initialize the project

```python
import digitalhub as dh
PROJECT_NAME = "datiprotezione" # here goes the project name that you are creating on the platform
project = dh.get_or_create_project(PROJECT_NAME)
```

2. Define the function

Register the ``create-list`` function in the project. It is required to update the 'code_src' url with github username and personal access token in the code cell below

```python
func_create = project.new_function(
    name="create", 
    kind="python", 
    python_version="PYTHON3_10", 
    code_src="git+https://<username>:<personal_access_token>@github.com/tn-aixpa/datiprotezione", 
    handler="src.create-list:create_list",
    requirements= ["deep_translator"]
)
```
The function represents a Python operation and may be invoked directly locally or on the cluster. The function will fetch the list of documents from online service and register a metadata list as dataitem inside project.

2. Run the function

```python
run_create_list = func_create.run(action="job",inputs={},outputs={}, local_execution=False)
```
The resulting metadata list will be registered as the project dataitem in the datalake under the name ``siat_trentino``.
