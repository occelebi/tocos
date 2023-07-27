## A very simple API

This Python Flask service implements a simple API to get data.

## Infrastructure Setup

Terraform creates private container registry, load balancer, security group, iam role, ECS Fargate. I used default VPC and subnet for the sake of simplicity. I did not use LocalStack. I keep it simple using tfstate directly instead of storing encyrpted state file in S3

## Containerization

I used Multi-stage docker build and python:alpine to optimise for a small image size. I am sure there are space to implement further.

## CI/CD Setup

Github action builds the image and pushes it to AWS private(secured) repository once the code pushed into main branch.

## Monitoring

I instrumented the code that exposes HTTP request duration in seconds by path, method and status code. 

I did not want to create whole prometheus stack on k8s. Nor prometheus managed service. Instead I created docker-compose file to give you an idea how it would look although I did not implement authentication to private ECR repository to let docker-compose pull image from there. 

It seems there is a way to use metric filters to extract metric observations from ingested events and transform them to data points in a CloudWatch metric. However I did not dig into deeper whether it supports exposed metrics from "/metrics" directly.

## API

### GET /tocos

Get all users with Tocos variable:

```sh
curl 'http://localhost:5000/tocos'
```

### GET /tocos/:user

Get specific user with Tocos variable:

```sh
curl 'http://localhost:5000/tocos/Cem'
```

### GET /metrics

Get all metrics instrumented by prometheus client:

```sh
curl 'http://localhost:5000/metrics'
```

#### After deployment

```
% curl tocos-alb-1622905611.eu-central-1.elb.amazonaws.com/tocos
[{"user": "John", "tocos": 100}, {"user": "Sam", "tocos": 200}, {"user": "Cem", "tocos": 300}]%

% curl tocos-alb-1622905611.eu-central-1.elb.amazonaws.com/tocos/Sam
{"user": "Sam", "tocos": 200}%

% curl tocos-alb-1622905611.eu-central-1.elb.amazonaws.com/tocos/Cem
{"user": "Cem", "tocos": 300}%

```
