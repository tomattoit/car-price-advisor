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
                def dockerImage = docker.build('tomattoid/postgres', './python-crawler')
                docker.withRegistry( 'https://registry.hub.docker.com', 'dockerhub-credentials' ) {
                    dockerImage.push("tagname")
                }
            }
        }
      }
    }
    
    

    stage('Deploying python job container to Kubernetes') {
      steps {
        script{
            kubernetesDeploy(configs: "python-app-depl.yaml")
        }
    }
    }

  }

}
