pipeline {
    agent none

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Build & Test') {
            parallel {

                stage('Backend (Python)') {
                    agent { docker { image 'python:3.13-slim' } }
                    environment {
                        PYTHONPATH = "${WORKSPACE}/bend/src"
                        HOME = "${WORKSPACE}"
                    }
                    stages {
                        stage('Build') {
                            steps {
                                sh '''
                                    python -m venv .venv
                                    . .venv/bin/activate
                                    pip install --upgrade pip
                                    pip install -r requirements.txt
                                '''
                            }
                        }
                        stage('Test') {
                            steps {
                                sh '''
                                    . .venv/bin/activate
                                    mkdir -p reports
                                    pytest bend/src/recsys/tests \
                                        --junitxml=reports/pytest.xml \
                                        --cov=recsys \
                                        --cov-report=xml:reports/coverage-back.xml \
                                        --cov-report=html:reports/htmlcov-back
                                '''
                            }
                            post {
                                always {
                                    junit 'reports/pytest.xml'
                                    recordCoverage(
                                        tools: [[parser: 'COBERTURA', pattern: 'reports/coverage-back.xml']],
                                        id: 'cov-back', name: 'Cobertura Backend'
                                    )
                                    publishHTML(target: [
                                        reportDir: 'reports/htmlcov-back',
                                        reportFiles: 'index.html',
                                        reportName: 'Cobertura Backend (HTML)',
                                        keepAll: true, alwaysLinkToLastBuild: true
                                    ])
                                }
                            }
                        }
                    }
                }

                stage('Frontend (Node)') {
                    agent { docker { image 'node:22-alpine' } }
                    environment {
                        HOME = "${WORKSPACE}"
                        npm_config_cache = "${WORKSPACE}/.npm"
                    }
                    stages {
                        stage('Build') {
                            steps {
                                dir('fend') {
                                    sh 'npm ci'
                                    sh 'npm run lint'
                                    sh 'npm run build'
                                }
                            }
                        }
                        stage('Test') {
                            steps {
                                dir('fend') {
                                    sh '''
                                        npx vitest run \
                                            --reporter=default --reporter=junit \
                                            --outputFile.junit=reports/vitest.xml \
                                            --coverage.enabled \
                                            --coverage.reporter=cobertura \
                                            --coverage.reporter=html \
                                            --coverage.reportsDirectory=reports/coverage
                                    '''
                                }
                            }
                            post {
                                always {
                                    junit 'fend/reports/vitest.xml'
                                    recordCoverage(
                                        tools: [[parser: 'COBERTURA', pattern: 'fend/reports/coverage/cobertura-coverage.xml']],
                                        id: 'cov-front', name: 'Cobertura Frontend'
                                    )
                                    publishHTML(target: [
                                        reportDir: 'fend/reports/coverage',
                                        reportFiles: 'index.html',
                                        reportName: 'Cobertura Frontend (HTML)',
                                        keepAll: true, alwaysLinkToLastBuild: true
                                    ])
                                }
                            }
                        }
                    }
                }
            }
        }

        stage('Deploy') {
            agent any
            when { branch 'main' }
            steps {
                sh 'docker compose -p recsys up -d --build'
            }
        }
    }

    post {
        failure { echo 'Pipeline falhou: veja os relatórios de teste acima.' }
    }
}
