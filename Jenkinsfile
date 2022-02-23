pipeline {
   
   agent {
      kubernetes {
         yamlFile 'KubernetesPod.yaml'
      }
   }
   parameters {
      choice(
         choices: ['all', 'nodejs', 'python'],
         description: '',
         name: 'BUILD_APP'
      )
   }
   
   environment { 

	DOCKER_IMAGE = 'nodejs'
	
      APP_VERSION = "${BUILD_ID}"
      APP_ENV = "${BRANCH_NAME}"
      
      AWS_ACCESS_KEY_ID     = credentials('AWS_ACCESS_KEY_ID')
      AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
      AWS_DEFAULT_REGION    = 'ap-southeast-1'
	//AWS_DEFAULT_REGION    = 'us-east-1'
	AWS_DEFAULT_OUTPUT    = 'json'
	   
	//ECR_REPO = '007293158826.dkr.ecr.' + ${AWS_DEFAULT_REGION} + '.amazonaws.com/nodejs'
	//ECR_REPO = '007293158826.dkr.ecr.us-east-1.amazonaws.com/nodejs'
	ECR_REPO_NODEJS = '130228678771.dkr.ecr.ap-southeast-1.amazonaws.com/nodejs'
   ECR_REPO_PYTHON = '130228678771.dkr.ecr.ap-southeast-1.amazonaws.com/python'
	   
   }

   stages {
      stage('[NODEJS] Build & push nodejs') {
         when {
            expression {
               params.BUILD_APP == 'nodejs'
            }
         }
         steps {
            container('docker') {
               sh '''
                 apk add --no-cache python3 py3-pip && pip3 install --upgrade pip && pip3 install awscli && rm -rf /var/cache/apk/*
                 aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID}
                 aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY}
                 aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin 130228678771.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com
                 cd nodejs/
                 docker build -t ${ECR_REPO_NODEJS}:${BUILD_ID} .
                 docker push ${ECR_REPO_NODEJS}:${BUILD_ID}
               '''
            }
         }
      }  
      stage('[NODEJS] Build & push python') {
         when {
            expression {
               params.BUILD_APP == 'python'
            }
         }
         steps {
            container('docker') {
               sh '''
                 apk add --no-cache python3 py3-pip && pip3 install --upgrade pip && pip3 install awscli && rm -rf /var/cache/apk/*
                 aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID}
                 aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY}
                 aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin 130228678771.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com
                 cd python/
                 docker build -t ${ECR_REPO_PYTHON}:${BUILD_ID} .
                 docker push ${ECR_REPO_PYTHON}:${BUILD_ID}
               '''
            }
         }
      }

      stage('[NODEJS] Deploy Nodejs') {
         when {
            expression{
               params.BUILD_APP == 'nodejs'
            }
         }
         steps {
            container('deploy-helm') {
               sh '''
                 apk add --no-cache python3 py3-pip && pip3 install --upgrade pip && pip3 install awscli && apk add --no-cache curl && rm -rf /var/cache/apk/*
                 curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
                 chmod +x ./kubectl && mv ./kubectl /usr/local/bin/kubectl
                 mkdir -p $HOME/.kube
                 cat <<< $KUBE_CONFIG > $HOME/.kube/config
                 helm upgrade --install -n nodejs nodejs-deployment deployment --set image="${ECR_REPO_NODEJS}:${BUILD_ID}"
               '''
            }
         }
      }
      
      stage('[PYTHON] Deploy Python') {
         when {
            expression {
               params.BUILD_APP == 'python'
            }
         }
         steps {
            container('deploy-helm') {
               sh '''
                 apk add --no-cache python3 py3-pip && pip3 install --upgrade pip && pip3 install awscli && apk add --no-chace curl && rm -rf /var/cache/apk/*
                 curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
                 chmod +x ./kubectl && mv ./kubectl /usr/local/bin/kubectl
                 mkdir -p $HOME/.kube
                 echo $KUBE_CONFIG > $HOME/.kube/config
                 helm upgrade --install -n python python-deployment deployment/python --set image="${ECR_REPO_NODEJS}:${BUILD_ID}"
               '''
            }
         }
      }

      stage('[ALL] Build and Push all') {
         when {
            expression {
               params.BUILD_APP == 'all'
            }
         }
         parallel {
            stage('[NODEJS] Build & push nodejs') {
               steps {
                  container('docker') {
                     sh '''
                       apk add --no-cache python3 py3-pip && pip3 install --upgrade pip && pip3 install awscli && rm -rf /var/cache/apk/*
                       aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID}
                       aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY}
                       aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin 130228678771.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com
                       docker build -t ${ECR_REPO_NODEJS}:${BUILD_ID} .
                       docker push ${ECR_REPO_NODEJS}:${BUILD_ID}
                     '''
                  }
               }
            }
            stage('[PYTHON] Build & push python') {
               steps {
                  container('docker') {
                     sh '''
                       apk add --no-cache python3 py3-pip && pip3 install --upgrade pip && pip3 install awscli && rm -rf /var/cache/apk/*
                       aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID}
                       aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY}
                       aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin 130228678771.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com
                       docker build -t ${ECR_REPO_PYTHON}:${BUILD_ID} .
                       docker push ${ECR_REPO_PYTHON}:${BUILD_ID}
                     '''
                  }
               }
            }
         }
      }
      stage('[all] Deploy all') {
         when {
            expression{
               params.BUILD_APP == 'all'
            }
         }
         parallel {
            stage('[NODEJS] Deoloy nodejs') {
               steps {
                  container('deploy-helm') {
                     sh '''
                       apk add --no-cache python3 py3-pip && pip3 install --upgrade pip && pip3 install awscli && apk add --no-chace curl && rm -rf /var/cache/apk/*
                       curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
                       chmod +x ./kubectl && mv ./kubectl /usr/local/bin/kubectl
                       mkdir -p $HOME/.kube
                       cat <<< $KUBE_CONFIG > $HOME/.kube/config
                       helm upgrade --install -n nodejs nodejs-deployment deployment --set image="${ECR_REPO_NODEJS}:${BUILD_ID}"
                     '''
                  }
               }
            }
            stage('[PYTHON] Deploy python') {
               steps {
               container('deploy-helm') {
                  sh '''
                    apk add --no-cache python3 py3-pip && pip3 install --upgrade pip && pip3 install awscli && apk add --no-chace curl && rm -rf /var/cache/apk/*
                    curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
                    chmod +x ./kubectl && mv ./kubectl /usr/local/bin/kubectl
                    mkdir -p $HOME/.kube
                    cat <<< $KUBE_CONFIG > $HOME/.kube/config
                    helm upgrade --install -n python python-deployment deployment/python --set image="${ECR_REPO_NODEJS}:${BUILD_ID}"
                  '''
                  }
               }
            }
         }
      }
   }
}