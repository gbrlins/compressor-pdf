Aplicação que comprime um arquivo PDF

Pronto para ser usado no Kubernetes como exemplo.

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
          terminationMessagePath: /dev/termination-log
          terminationMessagePolicy: File   
          resources: {}
      initContainers:
        - command:
            - sh
            - '-c'
            - ulimit -n 65536
          image: alpine
          imagePullPolicy: Always
          name: ulimit-init
          terminationMessagePath: /dev/termination-log
          terminationMessagePolicy: File
      restartPolicy: Always
      schedulerName: default-scheduler   
      terminationGracePeriodSeconds: 30
