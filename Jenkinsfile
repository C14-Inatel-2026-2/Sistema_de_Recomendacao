pipeline {
    // Roda no proprio container do Jenkins (Python e Node ja estao na imagem).
    agent any

    options {
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        // permite "from recsys... import ..." (o codigo fica em bend/src)
        PYTHONPATH = "${WORKSPACE}/bend/src"
        CI = 'true'
    }

    stages {
        // BUILD: prepara e valida o projeto (back e front em paralelo)
        stage('Build') {
            parallel {
                stage('Backend') {
                    steps {
                        sh '''
                            python3 -m venv .venv
                            . .venv/bin/activate
                            pip install --upgrade pip
                            pip install -r requirements.txt pytest-cov
                            python -c "import main"
                        '''
                    }
                }
                stage('Frontend') {
                    steps {
                        dir('fend') {
                            sh 'npm ci'
                            sh 'npm run lint'
                            sh 'npm run build'
                        }
                    }
                }
            }
        }

        // TEST: testes automatizados + relatorio + cobertura
        stage('Test') {
            parallel {
                stage('Backend') {
                    steps {
                        sh '''
                            . .venv/bin/activate
                            pytest bend/src/recsys/tests \
                                --junitxml=reports/back/junit.xml \
                                --cov=bend/src/recsys \
                                --cov-report=xml:reports/back/coverage.xml \
                                --cov-report=html:reports/back/htmlcov
                        '''
                    }
                    post {
                        always {
                            junit allowEmptyResults: true, testResults: 'reports/back/junit.xml'
                            recordCoverage(
                                tools: [[parser: 'COBERTURA', pattern: 'reports/back/coverage.xml']],
                                id: 'cobertura-back',
                                name: 'Cobertura Backend'
                            )
                            publishHTML(target: [
                                reportDir: 'reports/back/htmlcov',
                                reportFiles: 'index.html',
                                reportName: 'Cobertura Backend (HTML)',
                                keepAll: true,
                                alwaysLinkToLastBuild: true,
                                allowMissing: true
                            ])
                        }
                    }
                }
                stage('Frontend') {
                    steps {
                        dir('fend') {
                            sh '''
                                npx vitest run \
                                    --reporter=default --reporter=junit \
                                    --outputFile.junit=reports/junit.xml \
                                    --coverage.enabled \
                                    --coverage.provider=v8 \
                                    --coverage.reporter=cobertura \
                                    --coverage.reporter=html \
                                    --coverage.reportsDirectory=reports/coverage
                            '''
                        }
                    }
                    post {
                        always {
                            junit allowEmptyResults: true, testResults: 'fend/reports/junit.xml'
                            recordCoverage(
                                tools: [[parser: 'COBERTURA', pattern: 'fend/reports/coverage/cobertura-coverage.xml']],
                                id: 'cobertura-front',
                                name: 'Cobertura Frontend'
                            )
                            publishHTML(target: [
                                reportDir: 'fend/reports/coverage',
                                reportFiles: 'index.html',
                                reportName: 'Cobertura Frontend (HTML)',
                                keepAll: true,
                                alwaysLinkToLastBuild: true,
                                allowMissing: true
                            ])
                        }
                    }
                }
            }
        }

        // DEPLOY: so na branch main, dispara os dois Deploy Hooks do Render
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                withCredentials([
                    string(credentialsId: 'render-hook-api', variable: 'HOOK_API'),
                    string(credentialsId: 'render-hook-front', variable: 'HOOK_FRONT')
                ]) {
                    sh '''
                        curl -fsS -X POST "$HOOK_API"
                        curl -fsS -X POST "$HOOK_FRONT"
                    '''
                }
                echo 'Deploy disparado! Acompanhe no painel do Render.'
            }
        }
    }

    post {
        success { echo 'Pipeline VERDE: tudo certo.' }
        failure { echo 'Pipeline VERMELHA: pare tudo e conserte antes de seguir!' }
    }
}
