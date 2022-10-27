Please use an unique endpoint name, which you should change ```endpoint.yml``` as well as in the ```deployment.yml``` files.

Then just need to run the following lines of code in your compute instance

```
az login --tenant 7aa7ddbc-6504-4dc8-a6e4-ff73df71c91d
az account set --subscription "Azure subscription 2"
az configure --defaults workspace=ml-treshenv-ws-a127-svc-513c group=rg-treshenv-ws-a127

az ml online-endpoint create -f endpoint.yml
az ml online-deployment create -f deployment.yml
```
