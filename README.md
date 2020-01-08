# S3QL Prometheus Exporter
export your s3ql metrics to prometheus.


## Build
---

### Docker
```
docker build -t segator/s3qlprometheus .
```

## Run
---
#### Docker
```
docker run -p 6530:6530 -v /mnt/s3ql/series:/data segator/s3qlprometheusexporter
```


### Kubernetes
```
kubectl apply -f https://raw.githubusercontent.com/segator/s3ql-prometheus-exporter/master/kubernetes.yml
```

### bash

- **Help Usage**
```
usage: s3qlprometheus [s3ql mount path] [options]

List the content of a folder

optional arguments:
  -h, --help            show this help message and exit
  -p s3qlMountPath, --path s3qlMountPath
                        the path to mounted s3ql
  -P prometheusListenPort, --port prometheusListenPort
                        Prometheus listen port. DEFAULT: 6530
```

- **Run Example**
```

python3 s3qlprometheus.py --path /mnt/s3ql/
```
