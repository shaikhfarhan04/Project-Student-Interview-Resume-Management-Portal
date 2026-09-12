# Project-Student-Interview-Resume-Management-Portal
AWS, Terraform, Docker, Kubernetes/EKS, Jenkins, Ansible, SonarQube, Prometheus and Grafana, I recommend using this Student Interview &amp; Resume Management Portal as your flagship project.

## 1. Final project architecture

```text
                         ┌─────────────────────┐
                         │       Student       │
                         │ Browser / Mobile    │
                         └──────────┬──────────┘
                                    │ HTTPS
                                    ▼
                         ┌─────────────────────┐
                         │   Route 53 / DNS    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   AWS ALB / Ingress │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
             ┌──────────────┐                ┌──────────────┐
             │ Flask Frontend│                │ Flask Backend│
             │ / Web App     │                │ REST API     │
             └───────┬──────┘                └───────┬──────┘
                     │                               │
                     └───────────────┬───────────────┘
                                     │
                              ┌──────┴──────┐
                              │    EKS      │
                              │ Kubernetes  │
                              └──────┬──────┘
                                     │
                  ┌──────────────────┼──────────────────┐
                  │                  │                  │
                  ▼                  ▼                  ▼
             ┌─────────┐       ┌──────────┐       ┌──────────┐
             │   RDS   │       │    S3    │       │ Secrets  │
             │  MySQL  │       │ Resumes  │       │ Manager  │
             └─────────┘       └──────────┘       └──────────┘


                     CI/CD PIPELINE
                     ==============

Developer
    │
    ▼
 GitHub
    │
    ▼
 Jenkins
    │
    ├── Checkout
    ├── Unit Tests
    ├── SonarQube
    ├── Docker Build
    ├── Docker Scan
    ├── Push Image
    │
    ▼
 Amazon ECR
    │
    ▼
 Kubernetes / EKS
    │
    ▼
 Rolling Deployment


                     MONITORING
                     ==========

 EKS
  │
  ├── Prometheus
  │      │
  │      ▼
  │    Grafana
  │
  └── CloudWatch
```

---

# 2. What the application will do

### Student side

The student gets:

```text
Login
  ↓
Register
  ↓
Student Dashboard
  ↓
Profile
  ↓
Upload Resume
  ↓
Resume stored in S3
```

The database stores:

```text
Student
├── ID
├── Name
├── Email
├── Phone
├── Password Hash
├── Resume S3 Key
└── Created Date
```

The resume itself goes into:

```text
S3 Bucket
│
└── resumes/
    ├── 101/
    │   └── uuid-resume.pdf
    ├── 102/
    │   └── uuid-resume.pdf
    └── 103/
        └── uuid-resume.pdf
```

---

# 3. DevOps technologies

We'll deliberately cover the technologies an interviewer expects from a DevOps Engineer:

| Area                | Technology            |
| ------------------- | --------------------- |
| Application         | Python Flask          |
| Frontend            | HTML/CSS              |
| Database            | AWS RDS MySQL         |
| File storage        | AWS S3                |
| Containerization    | Docker                |
| Registry            | Amazon ECR            |
| Infrastructure      | Terraform             |
| Cloud               | AWS                   |
| Orchestration       | Kubernetes            |
| Kubernetes platform | EKS                   |
| CI/CD               | Jenkins               |
| Code quality        | SonarQube             |
| Security            | IAM + Secrets Manager |
| Monitoring          | Prometheus            |
| Dashboard           | Grafana               |
| Logging             | CloudWatch            |
| Source control      | Git/GitHub            |
| Networking          | VPC                   |
| Load balancing      | AWS ALB               |
| DNS                 | Route 53              |
| TLS                 | ACM                   |
| Configuration       | ConfigMap/Secrets     |

---

# 4. We will build it in phases

I strongly recommend **not trying to create everything at once**.

We'll build it like an actual company project.

## Phase 1 — Application

First we make the application completely functional locally.

```text
Student
   ↓
Register
   ↓
Login
   ↓
Dashboard
   ↓
Upload Resume
   ↓
S3
   +
RDS
```

You'll learn:

* Flask
* REST APIs
* MySQL
* authentication
* password hashing
* file upload
* S3 integration
* database operations

You already have the starter application from the previous step:

**[Download Student Resume Portal](sandbox:/mnt/data/student-interview-resume-portal.zip)**

---

# 5. Phase 2 — Git/GitHub

We'll create a professional repository:

```text
student-interview-portal/
│
├── app/
│   ├── app.py
│   ├── requirements.txt
│   ├── templates/
│   └── static/
│
├── tests/
│
├── docker/
│   └── Dockerfile
│
├── terraform/
│   ├── provider.tf
│   ├── variables.tf
│   ├── vpc.tf
│   ├── iam.tf
│   ├── s3.tf
│   ├── rds.tf
│   ├── eks.tf
│   └── outputs.tf
│
├── kubernetes/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   └── ingress.yaml
│
├── Jenkinsfile
│
├── monitoring/
│   ├── prometheus/
│   └── grafana/
│
├── README.md
└── architecture/
    └── architecture.png
```

This structure itself will look much more professional during an interview.

---

# 6. Phase 3 — Docker

We'll containerize Flask.

```text
                Docker
                  │
                  ▼
        ┌──────────────────┐
        │ Student Portal   │
        │ Flask Application │
        └──────────────────┘
```

We'll implement:

* Dockerfile
* `.dockerignore`
* non-root container user
* environment variables
* health endpoint
* container health check

For example:

```text
GET /health

{
    "status": "healthy"
}
```

Then:

```powershell
docker build -t student-portal .
docker run -p 5000:5000 student-portal
```

---

# 7. Phase 4 — AWS infrastructure with Terraform

This is where the project becomes a serious DevOps project.

We'll create:

```text
AWS
│
├── VPC
│
├── Public Subnets
│   └── ALB
│
├── Private Subnets
│   ├── EKS
│   └── RDS
│
├── Internet Gateway
│
├── NAT Gateway
│
├── Route Tables
│
├── Security Groups
│
├── EKS
│
├── ECR
│
├── RDS
│
├── S3
│
└── IAM
```

### Important interview point

We will **not** put RDS publicly accessible.

Instead:

```text
Internet
   |
   v
ALB
   |
   v
EKS
   |
   v
RDS Private Subnet
```

This gives you a strong answer when an interviewer asks:

> "How did you secure your database?"

---

# 8. Phase 5 — ECR

Jenkins will build the Docker image:

```text
student-portal:BUILD_NUMBER
```

and push it to:

```text
Amazon ECR
     │
     ├── student-portal:latest
     ├── student-portal:101
     ├── student-portal:102
     └── student-portal:103
```

We'll use immutable/versioned image tags in the actual deployment.

---

# 9. Phase 6 — Kubernetes / EKS

The application becomes:

```text
                   EKS
                    │
             Namespace: student
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
    Flask Pod 1          Flask Pod 2
          │                   │
          └─────────┬─────────┘
                    │
                    ▼
                Service
                    │
                    ▼
                   ALB
```

We'll create:

### Deployment

```yaml
replicas: 2
```

### Service

```text
student-portal-service
```

### ConfigMap

Non-sensitive configuration:

```text
AWS_REGION
S3_BUCKET
DB_NAME
```

### Secret

Sensitive information:

```text
DB_USERNAME
DB_PASSWORD
```

But in the production version, we'll improve this further with **AWS Secrets Manager + External Secrets**, rather than keeping database credentials directly in Git/Kubernetes YAML.

---

# 10. Phase 7 — Jenkins CI/CD

This is one of the most important parts for your interview.

The pipeline will be:

```text
Developer
    │
    │ git push
    ▼
 GitHub
    │
    │ webhook
    ▼
 Jenkins
    │
    ├── 1. Checkout
    │
    ├── 2. Install dependencies
    │
    ├── 3. Unit tests
    │
    ├── 4. SonarQube
    │
    ├── 5. Docker build
    │
    ├── 6. Security scan
    │
    ├── 7. ECR login
    │
    ├── 8. Push image
    │
    ├── 9. kubectl
    │
    └── 10. Rolling deployment
             │
             ▼
            EKS
```

A professional Jenkins pipeline could contain:

```text
Checkout
   ↓
Test
   ↓
SonarQube
   ↓
Build Docker Image
   ↓
Trivy Scan
   ↓
Push to ECR
   ↓
Deploy to EKS
   ↓
Smoke Test
```

---

# 11. Phase 8 — SonarQube

Jenkins sends the source code to SonarQube:

```text
Jenkins
   │
   ▼
SonarQube
   │
   ├── Bugs
   ├── Vulnerabilities
   ├── Code Smells
   ├── Coverage
   └── Quality Gate
```

If the quality gate fails:

```text
❌ Pipeline STOP
```

If it passes:

```text
✅ Continue deployment
```

That's a very good interview talking point.

---

# 12. Phase 9 — Security

We'll include several layers.

### IAM

Instead of:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

inside the application, we'll use:

```text
EKS Pod
   ↓
IAM Role
   ↓
S3
```

This demonstrates **IAM least privilege**.

### S3

The bucket will remain:

```text
Private
```

No:

```text
Public Read
```

The application gets permission to upload resumes.

### RDS

```text
Private Subnet
      +
Security Group
      +
3306 only from application SG
```

### Resume validation

We'll restrict:

```text
PDF
DOC
DOCX
```

and enforce a maximum file size.

---

# 13. Phase 10 — Monitoring

We'll deploy:

```text
                 Kubernetes
                     │
                     ▼
                Prometheus
                     │
                     ▼
                  Grafana
```

We'll monitor:

* CPU
* memory
* pod status
* pod restarts
* request rate
* application health
* node health

Example dashboard:

```text
Grafana

┌────────────────────────────────────┐
│ EKS Cluster                        │
├─────────────┬──────────────────────┤
│ CPU         │ ███████░░░  70%      │
│ Memory      │ █████░░░░░  52%      │
│ Pods        │ 4                      │
│ Restarts    │ 0                      │
├─────────────┴──────────────────────┤
│ Request Rate                        │
│       /\      /\                    │
│  ____/  \____/  \_____             │
└────────────────────────────────────┘
```

---

# 14. Phase 11 — Logging

We'll use:

```text
Application
     │
     ▼
Container logs
     │
     ▼
CloudWatch
```

This lets you answer:

> "How do you troubleshoot a production issue?"

Your answer can include:

```text
1. Check ALB
2. Check Kubernetes pods
3. kubectl logs
4. Check Prometheus/Grafana
5. Check CloudWatch
6. Check RDS
7. Check application errors
```

---

# 15. Phase 12 — High Availability

We'll intentionally run multiple replicas:

```text
             ALB
              |
       ┌──────┴──────┐
       │             │
       ▼             ▼
     Pod 1         Pod 2
       │             │
       └──────┬──────┘
              │
             RDS
```

If Pod 1 fails:

```text
Pod 1 ❌

Pod 2 ✅
```

Kubernetes creates another pod.

This gives you a strong answer to:

> "How does your application achieve high availability?"

---

# 16. Phase 13 — Autoscaling

We'll add:

```text
Horizontal Pod Autoscaler
```

Example:

```text
Normal traffic

Pod 1
Pod 2


High traffic

Pod 1
Pod 2
Pod 3
Pod 4
Pod 5
```

Based on CPU/memory utilization.

---

# 17. Phase 14 — Disaster recovery

We'll discuss:

### RDS

* automated backups
* snapshots
* Multi-AZ discussion

### S3

* versioning
* lifecycle policy
* encryption

### Infrastructure

Terraform:

```text
terraform/
```

means the environment can be recreated.

This is a very important DevOps principle:

> **Infrastructure should be reproducible.**

---

# 18. Final CI/CD architecture

Your final interview diagram can be:

```text
                         DEVELOPER
                             |
                             | git push
                             v
                         GITHUB
                             |
                          Webhook
                             |
                             v
                         JENKINS
                             |
            ┌────────────────┼────────────────┐
            │                │                │
            v                v                v
        Unit Test        SonarQube         Trivy
            │                │                │
            └────────────────┼────────────────┘
                             |
                        Docker Build
                             |
                             v
                           ECR
                             |
                             v
                          EKS
                             |
                     ┌───────┴───────┐
                     │               │
                  Pod 1            Pod 2
                     │               │
                     └───────┬───────┘
                             |
                            ALB
                             |
                          Internet

                    EKS
                     |
            ┌────────┼─────────┐
            │        │         │
            v        v         v
           RDS      S3     Secrets Manager
            |
       Student Data

                    EKS
                     |
                     v
                Prometheus
                     |
                     v
                  Grafana
```

---

# 19. What you should be able to explain in the interview

After completing this project, I want you to be able to confidently answer:

### AWS

* What is VPC?
* Public vs private subnet?
* NAT Gateway?
* Internet Gateway?
* Security Groups?
* ALB?
* RDS?
* S3?
* IAM?
* ECR?
* EKS?

### Terraform

* Why Terraform?
* `terraform init`
* `terraform plan`
* `terraform apply`
* State file
* Variables
* Outputs
* Modules
* Remote backend
* State locking
* Terraform dependency management

### Docker

* Image vs container
* Dockerfile
* Multi-stage builds
* Docker networking
* Volumes
* Docker Compose
* Container security

### Kubernetes

* Pod
* Deployment
* ReplicaSet
* Service
* Ingress
* ConfigMap
* Secret
* Namespace
* HPA
* Rolling deployment
* Rollback

### Jenkins

* CI vs CD
* Pipeline
* Jenkinsfile
* Webhook
* Credentials
* Agents
* Build artifacts
* Deployment strategy

### Monitoring

* Prometheus
* Grafana
* Metrics
* Logs
* Alerts
* Kubernetes monitoring

---

# 20. How I suggest we build it with you

We'll do this **hands-on**, not just give you a huge collection of files.

### Stage 1

**Build and test the Flask application locally**

### Stage 2

**Create GitHub repository + proper project structure**

### Stage 3

**Dockerize application**

### Stage 4

**Create AWS VPC using Terraform**

### Stage 5

**Create S3 + RDS + IAM**

### Stage 6

**Deploy application to EC2 first**

This gives us an intermediate checkpoint.

### Stage 7

**Create ECR + EKS**

### Stage 8

**Deploy Flask application to Kubernetes**

### Stage 9

**Create Jenkins CI/CD**

### Stage 10

**Integrate SonarQube + Trivy**

### Stage 11

**Add Secrets Manager**

### Stage 12

**Add Prometheus + Grafana**

### Stage 13

**Add ALB + HTTPS**

### Stage 14

**Add HPA + rolling deployment**

### Stage 15

**Complete documentation + architecture diagram + interview questions**

---

## One important point for your AWS account

Because you've been working with **AWS Free Tier/cost-conscious labs**, we should design the project so that we don't unnecessarily leave expensive resources running. **EKS, NAT Gateways, ALB, RDS and multi-AZ infrastructure can generate charges**, so we'll build and test in controlled stages and clean up resources when a stage is finished.

**I recommend we start with Stage 1 now: build the production-style Flask application locally, then connect it to S3 and RDS before touching EKS.** This gives us a working application to put through the entire DevOps pipeline.
