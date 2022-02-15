# Python-django-app with IaC and CI/CD

This repo contain a simple Django App deployed in a Amazon Elastic Kubernetes Service throught a CI/CD Pïpeline build in Azure DevOps, the infrastructure were define as code (IaC) with eksctl and Helm.

## Software used

* [Kubernetes](https://github.com/kubernetes/kubernetes)
* [Docker](https://github.com/docker/docker-ce)
* [Helm](https://helm.sh/docs/)
* [Eksctl](https://eksctl.io/introduction/)
* [Python](https://www.python.org)
* [Django](https://www.djangoproject.com)

## Structure of the repo

This repo contains the  folder cool_counters, an Django app developed by [deparkes](https://github.com/deparkes/simple-django-app) througth Docker. In the root there is a folder named deploy_resources, where is all the code necesary to deploy the kubernetes cluster on AWS, including a helm chart to deploy the app on Kubernetes (k8s-deployment-app) and the helm chart to create the ingress of the cluster. the pipeline is located on the root of the project.

## Explanation

1. Containerized the app with Docker.

```
FROM python:3.10-alpine

WORKDIR /home/app
COPY . /home/app/
RUN pip install django
RUN python manage.py migrate

ENTRYPOINT ["python", "./manage.py", "runserver", "0.0.0.0:80"]
```

2.  Create the Kubernetes cluster on AWS with 2 worker nodes.

cluster.yaml

```
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata:
  name: devops-catalog
  region: us-east-2
  version: "1.21"
managedNodeGroups:
- name: primary
  instanceType: t2.small
  minSize: 2
  maxSize: 3
  spot: true
```

```sh
eksctl create cluster -f cluster.yaml
```

In order to connect our AWS Resources with Azure DevOps is necesary create a Service Account and a Cluster Role Biding in the cluster.

```
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: azure-devops-admin
subjects:
- kind: ServiceAccount
  name: azure-devops
  namespace: default
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
```

```
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: azure-devops-admin
subjects:
- kind: ServiceAccount
  name: azure-devops
  namespace: default
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
```

3. There are a few manual steps relate to the configuration of the Elastic Container Registry on AWS, the  creation of Service Connection and Environment on Azure DevOps (To connect AzDevOps with AWS), creation and configuration of a EC2 instance to be used as a Pipeline Agent on Azure DevOps. Those steps are not going to be shown on this Markdown.

4. Installing Kubernetes Ingress-Controller with helm.

```sh
 helm repo add nginx-stable https://helm.nginx.com/stable
 helm repo update
 kubectl create ns nginx-ingress
 helm install <Name of relase> nginx-stable/nginx-ingress -n nginx-ingress 
```

5. Creating helm chart for cool_counters app.

```sh
 helm create k8s-deployment-app
```
Edit Chart.yaml in orden to use a replace tokens task on the pipeline for versioning the chart.

Chart.yaml
```
...
type: application
version: __Build.BuildNumber__
appVersion: "__Build.BuildNumber__"
```

Edit values.yaml to put a pipeline variable related to the AWS ECR and the tag of the image.

values.yaml

```
...
image:
  repository: __AWS_ECR_REPO_FULL_NAME__
  pullPolicy: IfNotPresent
  # Overrides the image tag whose default is the chart appVersion.
  tag: "__Build.BuildNumber__"
 ...
```
Also is necessary specify the ingress path that is going to be used for reaching the app through Ingress.

```
ingress:
  enabled: true
  className: "nginx"
  annotations: {}
    # kubernetes.io/ingress.class: nginx
    # kubernetes.io/tls-acme: "true"
  hosts:
    - host: myapp-django.app
      paths:
        - path: /
          pathType: ImplementationSpecific
```

6. Pipeline explanation

The first line called name, with Major.Minor.Rev:r is a simple way to versioning the build, on this part of the Pipeline also are present some variables used on the pipeline, the AWS-ECR-Variables are going to be shown ahead.

```
name: $(Major).$(Minor).$(Rev:r)

trigger:
- main

pool: Default

variables:
- name: Application
  value: 'cool_counters'

- name: Major
  value: '0'

- name: Minor
  value: '0'

- group: AWS-ECR-Variables
```

AWS-ECR-Variables
```
AWS_ACCOUNT_ID
AWS_CREDENTIALS
AWS_ECR_REPO_FULL_NAME
AWS_ECR_REPOSITORY
AWS_ECR_REPOSITORY
AWS_REGION
```

###Continious Integration Phase

There is a simple bash script to build the Docker Image and a task to push it into the AWS ECR

```
stages:
- stage: CI
  jobs:
  - job:
    steps:
    - bash: |
        docker build -t $(AWS_ECR_REPOSITORY):$(Build.BuildNumber) $(Build.SourcesDirectory)/$(Application)
      displayName: 'Build docker image'
    
    - task: ECRPushImage@1
      displayName: Push image to AWS ECR
      inputs:
         awsCredentials: $(AWS_CREDENTIALS)
         regionName: $(AWS_REGION)
         imageSource: 'imagename'
         sourceImageName: $(AWS_ECR_REPOSITORY)
         sourceImageTag: $(Build.BuildNumber)
         pushTag: $(Build.BuildNumber)
         repositoryName: $(AWS_ECR_REPOSITORY)
         logRequest: true
         logResponse:
```

###Continious Integration Phase

First is necesary replace the tokens decribed on the Helm chart of k8s-deployment-app, this is made by the task ReplaceTokens


```
- stage: CD
  pool: Default
  jobs:
  - deployment:
    environment: dev
    displayName: Deployment
    strategy:
      runOnce:
        deploy:
          steps:
          
          - task: replacetokens@4
            displayName: Replace tokens in values.yaml
            inputs:
               rootDirectory: '$(Build.SourcesDirectory)/deploy_resources/k8s-deployment-app'
               targetFiles: 'values.yaml'
               tokenPattern: custom
               actionOnNoFiles: fail
               tokenPrefix: '__'
               tokenSuffix: '__'

          - task: replacetokens@4
            displayName: Replace tokens in Chart.yaml
            inputs:
               rootDirectory: '$(Build.SourcesDirectory)/deploy_resources/k8s-deployment-app'
               targetFiles: 'Chart.yaml'
               tokenPattern: custom
               actionOnNoFiles: fail
               tokenPrefix: '__'
               tokenSuffix: '__'
```
This task create a helm package besides, there is a task on charge of Deploy the app to the Kubernetes Cluster throught thd helm chart, this task uses the Service Connection and the environment to this lavour.

```
          - task: HelmDeploy@0
            displayName: Package Helm Chart for $(Application)
            inputs:
             command: 'package'
             chartPath: '$(Build.SourcesDirectory)/deploy_resources/k8s-deployment-app'


          - task: HelmDeploy@0
            continueOnError: true
            displayName: Deploy to cluster
            inputs:
               namespace: 'python-app'
               command: 'upgrade'
               connectionType: Kubernetes Service Connection
               kubernetesCluster: 'devops-catalog'
               KubernetesServiceEndpoint: 'dev-python-app-1644715730033'
               releaseName: 'counter'
               chartType: filepath
               chartPath: '$(Build.StagingDirectory)/k8s-deployment-app-$(Build.BuildNumber).tgz'
```

> Due to there is not DNS Record is necessary edit /etc/hosts file with the public IP of the Elastic Load Balancer, the IP is taken by nslookup the ELB URL.
