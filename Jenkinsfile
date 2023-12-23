pipeline {

  agent {
      kubernetes{
            defaultContainer 'jnlp'
            yaml '''
                apiVersion: v1
                
                kind: Pod
                
                metadata:
                
                  labels:
                
                    some-label: pod
                
                spec:
                
                  containers:
                
                    - name: maven
                
                      image: maven:3.3.9-jdk-8-alpine
                
                      command:
                
                        - cat
                
                      tty: true
                
                      volumeMounts:
                
                        - name: m2
                
                          mountPath: /root/.m2
                
                    - name: docker
                
                      image: docker:19.03
                
                      command:
                
                        - cat
                
                      tty: true
                
                      privileged: true
                
                      volumeMounts:
                
                        - name: dockersock
                
                          mountPath: /var/run/docker.sock
                
                  volumes:
                
                    - name: dockersock
                
                      hostPath:
                
                        path: /var/run/docker.sock
                
                    - name: m2
                
                      hostPath:
                
                        path: /root/.m2
                    '''
      }
  }

  stages {

    stage('Checkout Source') {
      steps {
        git branch: 'main', url: 'https://github.com/tomattoit/car-price-advisor.git'
      }
    }

    stage('Build image') {
      steps{
        container('docker'){
            sh 'docker build -t postgres ./python-job'
        }
      }
    }

    stage('Pushing Image') {
      steps{
          container('docker'){
            sh 'docker tag postgres tomattoid/postgres:tagname'
            sh 'docker push tomattoid/postgres:tagname'
          }
      }
    }

    stage('Deploying python job container to Kubernetes') {
      steps {
        sh 'curl -LO "https://storage.googleapis.com/kubernetes-release/release/v1.20.5/bin/linux/amd64/kubectl"'  
        sh 'chmod u+x ./kubectl'  
        sh './kubectl apply -f k8s_yaml/python-app-depl.yaml'
    }
    }

  }

}
