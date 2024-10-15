Aplicação que comprime um arquivo PDF

Pronto para ser usado no Kubernetes como exemplo.

Exemplo de deployment.yaml
```jsx
apiVersion: apps/v1
kind: Deployment
metadata:
name: pdf-compressor-deployment
labels:
app: pdf-compressor
namespace: default
spec:
selector:
matchLabels:
app: pdf-compressor
template:
metadata:
labels:
app: pdf-compressor
spec:
containers:
- image: gabriellins/suse-compress-pdf:2.6
imagePullPolicy: IfNotPresent
name: pdf-compressor
ports:
- containerPort: 8080
name: 8080tcp
protocol: TCP
initContainers:
- command:
- sh
- '-c'
- ulimit -n 65536
image: alpine
imagePullPolicy: Always
name: ulimit-init
restartPolicy: Always
```

Exemplo service.yaml
```jsx
apiVersion: v1
kind: Service
metadata:
  name: pdf-compressor-service
  namespace: default
spec:
  type: NodePort
  selector:
    app: pdf-compressor
  ports:
    - protocol: TCP
      port: 8080
      targetPort: 8080
      nodePort: 30007
```
