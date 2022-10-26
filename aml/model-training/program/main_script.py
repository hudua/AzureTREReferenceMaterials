from azureml.core.authentication import MsiAuthentication
from azureml.core import Workspace, Datastore, Dataset, Model
import pandas as pd
import pickle
from testmethods import add
from sklearn.linear_model import LinearRegression
import sklearn
import numpy as np


#this workspace object is needed to register the model
subscription_id =
resource_group =
workspace_name =
msi_auth = MsiAuthentication()

ws = Workspace(subscription_id, resource_group, workspace_name,auth=msi_auth)

# or you can use the direct dataset connector to data lake
# dataset = Dataset.get_by_name(ws, name='samplefile3')
# df = dataset.to_pandas_dataframe()

# example to show how to import a custom Python module
x = add.add_example_weird(2, 34)
print(x)

df = pd.read_csv('data/iris.csv')
model = LinearRegression()
X = np.array(df['sepal.width']).reshape(-1, 1)
y = np.array(df['petal.length']).reshape(-1, 1)

#model training here
#sample hardcoded model, but of course in practice this would be a xgboost model or sklearn model, etc.
model.fit(X, y)

pickle.dump(model, open('./model.pkl', 'wb'))
model = Model.register(workspace = ws,
                       model_name="tmlsmodel",
                       model_path = "./model.pkl",
                       description = 'Regression Example Model'
                      )
