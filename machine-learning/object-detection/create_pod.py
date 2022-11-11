from kubernetes import client, config

def create_pod(data , string_data , client_api):
    secret = client.V1Secret(
        api_version="v1",
        kind="Pod",
        metadata=client.V1ObjectMeta(name="my-pod"),
        data=data ,
        string_data=string_data
    )

    api = client_api.create_namespaced_pod(namespace="default", body=secret)
    return api
