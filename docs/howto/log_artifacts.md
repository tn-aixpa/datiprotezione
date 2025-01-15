# Log aritfacs

To log the artifacts, it is possible to use ``convert-list`` operation that performs conversion of dataset using the meta data (siat-trentino)

1. Initialize the project

```python
import digitalhub as dh
PROJECT_NAME = "datiprotezione" # here goes the project name that you are creating on the platform
project = dh.get_or_create_project(PROJECT_NAME)
```

2. Define the function

Register the ``convert-list`` function in the project. It is required to update the 'code_src' url with github username and personal access token in the code cell below

```python
func = proj.new_function(
    name="create", 
    kind="python", 
    python_version="PYTHON3_10", 
    code_src="git+https://<username>:<access_token>@github.com/tn-aixpa/datiprotezione",
    handler="src.create:create_list",
	requirements=["deep_translator"]
)
```
The function represents a Python operation and may be invoked directly locally or on the cluster. It will read the list of metadata and fetch the actual dataset using corresponding link. The dataset will be registered in side the project contexts as artifacts.
