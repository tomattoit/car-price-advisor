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

                sshagent(['ssh-credentials']) {
                    sh 'ssh -o StrictHostKeyChecking=no ubuntu@ec2-18-198-1-37.eu-central-1.compute.amazonaws.com kubectl delete -f car-price-advisor/k8s_yaml/react-app.yaml'
                    sh 'ssh -o StrictHostKeyChecking=no ubuntu@ec2-18-198-1-37.eu-central-1.compute.amazonaws.com kubectl delete -f car-price-advisor/k8s_yaml/flask-api.yaml'
                    sh 'ssh -o StrictHostKeyChecking=no ubuntu@ec2-18-198-1-37.eu-central-1.compute.amazonaws.com kubectl delete -f car-price-advisor/k8s_yaml/otomoto-crawler-job.yaml'
                    sh 'ssh -o StrictHostKeyChecking=no ubuntu@ec2-18-198-1-37.eu-central-1.compute.amazonaws.com kubectl delete -f car-price-advisor/k8s_yaml/retrain-job.yaml'
                    
                    sh 'ssh -o StrictHostKeyChecking=no ubuntu@ec2-18-198-1-37.eu-central-1.compute.amazonaws.com kubectl apply -f car-price-advisor/k8s_yaml/react-app.yaml'
                    sh 'ssh -o StrictHostKeyChecking=no ubuntu@ec2-18-198-1-37.eu-central-1.compute.amazonaws.com kubectl apply -f car-price-advisor/k8s_yaml/flask-api.yaml'
                    sh 'ssh -o StrictHostKeyChecking=no ubuntu@ec2-18-198-1-37.eu-central-1.compute.amazonaws.com kubectl apply -f car-price-advisor/k8s_yaml/otomoto-crawler-job.yaml'
                    sh 'ssh -o StrictHostKeyChecking=no ubuntu@ec2-18-198-1-37.eu-central-1.compute.amazonaws.com kubectl apply -f car-price-advisor/k8s_yaml/retrain-job.yaml'
                }
                
        }
    }
    }

  }

}
