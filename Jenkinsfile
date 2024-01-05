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
            script{
                def crawlerImage = docker.build('tomattoid/otomoto-crawler', './python-crawler')
                def reactImage = docker.build('tomattoid/react-app', './react-app/car-price-advisor-frontend')
                def flaskImage = docker.build('tomattoid/flask-api', './flask-api')
                def retrainjobImage = docker.build('tomattoid/retrain-app', './retrain-job')
                docker.withRegistry( 'https://registry.hub.docker.com', 'dockerhub-credentials' ) {
                    crawlerImage.push("latest")
                    reactImage.push("latest")
                    flaskImage.push("latest")
                    retrainjobImage.push("latest")
                }
            }
        }
      }
    }
    
    

    stage('Deploying python job container to Kubernetes') {
      steps {
        script{
                def remote = [:]
                remote.name = 'name'
                remote.host = 'host'
                remote.user = 'user'
                remote.password = 'password'
                remote.allowAnyHosts = true
                
                sshCommand remote: remote, command: "kubectl delete -f car-price-advisor/k8s_yaml/react-app.yaml"
                sshCommand remote: remote, command: "kubectl delete -f car-price-advisor/k8s_yaml/flask-api.yaml"
                sshCommand remote: remote, command: "kubectl delete -f car-price-advisor/k8s_yaml/otomoto-crawler-job.yaml"
                sshCommand remote: remote, command: "kubectl delete -f car-price-advisor/k8s_yaml/retrain-job.yaml"
                  
                sshCommand remote: remote, command: "kubectl apply -f car-price-advisor/k8s_yaml/react-app.yaml"
                sshCommand remote: remote, command: "kubectl apply -f car-price-advisor/k8s_yaml/flask-api.yaml"
                sshCommand remote: remote, command: "kubectl apply -f car-price-advisor/k8s_yaml/otomoto-crawler-job.yaml"
                sshCommand remote: remote, command: "kubectl apply -f car-price-advisor/k8s_yaml/retrain-job.yaml"
                
        }
    }
    }

  }

}
