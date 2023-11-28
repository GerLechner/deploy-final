pipeline {
    agent any
    
    environment {
        DOCKER_CREDENTIALS = credentials('DOCKER_CREDENTIALS')
        DOCKER_USER = credentials('DOCKER_USER')
        IP_PRODU = credentials('IP_PRODUCCION')
        USER_PRODU = credentials('USER_PRODUCCION')
    }
    
    stages {
        stage('Git Clone'){
            steps {
                git credentialsId: 'GIT_CREDENTIALS', url: 'https://github.com/GerLechner/deploy-final'
            }
        }
    
        stage('test de la imagen') {
            steps {
                
                sh "docker-compose up -d --build"
                sleep(time:5, unit: "SECONDS")
            
                sh "docker exec flask-app-container python tests.py"
                
                sh "docker stop flask-app-container"
                sh "docker stop flask-app-db-container"
                
                sh "docker rm flask-app-container"
                sh "docker rm flask-app-db-container"
                
            }
        }

        stage('SonarQube Analysis') {
            steps{
                script{
                    sh "docker start sonarqube"
                    //sleep(time:60, unit: "SECONDS")
                    
                    def scannerHome = tool name: 'SonarScanner'
                    withSonarQubeEnv('SonarQubeServer') {
                        sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=analisis-deploy-flask-pruebas -Dsonar.scanner.config.file=sonar-project.properties -X"   
                    }
                }
            }
        }/*
    
        stage('Build Docker Image'){
            steps {
                sh "docker-compose build"
            }
        }
    
    
        stage('Push Docker Image') {
            steps {
                sh "docker login -u ${DOCKER_USER} -p ${DOCKER_CREDENTIALS}"
                sh "docker push ${DOCKER_USER}/flask-app"
            }
        }
    
    
        stage('Deploy Kubernetes'){
            steps {
                script {
                    
                    def produccion = "${USER_PRODU}@${IP_PRODU}"
                    
                    sh "mkdir -p /$HOME/deploy-final"
                    sh "scp -r Kubernetes ${produccion}:/$HOME/deploy-final"
                    sh "ssh ${produccion} 'sudo service docker restart'"
                    sh "ssh ${produccion} 'minikube start'"
                    sh "ssh ${produccion} 'kubectl apply -f \$(printf \"%s,\" $HOME/deploy-final/*.yaml | sed \"s/,\$//\")'"
                    sleep(time:4, unit: "SECONDS")
                    sh "ssh ${produccion} 'minikube service app --url'"
        
                    def minikubeIp = sh(script:"ssh ${produccion} 'minikube ip'", returnStdout: true).trim()
                    def puerto = sh(script:"ssh ${produccion} 'kubectl get service app --output='jsonpath={.spec.ports[0].nodePort}' --namespace=default'", returnStdout: true).trim()
                    
                    sh(script: "echo ssh -L 192.168.192.130:${puerto}:${minikubeIp}:${puerto}")
                    
                    //sh "ssh ${produccion} 'kubectl delete deployments,services app db'" 
                    
                    sh "ssh ${produccion} 'rm /$HOME/deploy-final/*.yaml'"
                    sh "ssh ${produccion} 'rmdir /$HOME/deploy-final'"
                
                }
            }
        }*/
    }
}
