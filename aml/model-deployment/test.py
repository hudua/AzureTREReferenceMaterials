from azureml.core import Workspace, Dataset, Model
import os

subscription_id =
resource_group = 
workspace_name = 

ws = Workspace(subscription_id, resource_group, workspace_name)


model = Model(workspace=ws, name="tmlsmodel")
model.download(target_dir=os.getcwd())


import pickle
import numpy
import json


model = pickle.load(open('model.pkl','rb'))


raw_data = '{"data":[1,2]}'


data = json.loads(raw_data)["data"]
data = numpy.array(data).reshape(-1, 1)
result = model.predict(data)


result.tolist()
