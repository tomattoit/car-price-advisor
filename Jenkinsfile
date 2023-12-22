pipeline {

  environment {
    dockerimagename = "tomattoid/postgres"
    dockerImage = ""
  }

  agent any

  stages {

    stage('Checkout Source') {
      steps {
        git 'https://github.com/tomattoit/car-price-advisor.git'
      }
    }

    stage('Build image') {
      steps{
        sh 'cd python-job/'
        script {
          dockerImage = docker.build dockerimagename
        }
      }
    }

    stage('Pushing Image') {
      environment {
               registryCredential = 'dockerhub-credentials'
           }
      steps{
        script {
          docker.withRegistry( 'https://registry.hub.docker.com', registryCredential ) {
            dockerImage.push("latest")
          }
        }
      }
    }

    stage('Deploying python job container to Kubernetes') {
      steps {
        sh 'cd k8s_yaml'
        script {
          kubernetesDeploy(configs: "python-app-depl.yaml")
        }
      }
    }

  }

}