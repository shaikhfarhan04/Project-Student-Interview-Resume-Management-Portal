# Student Interview Resume Portal

Interview-ready AWS project:

Student -> Flask Web App -> Amazon RDS MySQL
                         -> Amazon S3 (Resume)

## Features

- Student registration
- Secure password hashing
- Login/logout
- Student profile
- Resume upload
- Resume stored in S3
- Student details and S3 object key stored in RDS MySQL
- Docker-ready Flask application

## 1. Create RDS MySQL

Recommended interview architecture:
- Engine: MySQL
- Private subnet in production
- Security group allows TCP 3306 only from the application security group
- Database: student_portal

Run schema.sql on the database.

## 2. Create S3 bucket

Create a unique bucket, for example:
student-interview-resumes-<unique-suffix>

Recommended:
- Block all public access: ON
- Versioning: ON
- Server-side encryption: SSE-S3 or SSE-KMS
- Do NOT make resumes public

The application uploads objects under:
resumes/<student-id>/<uuid>.<extension>

## 3. IAM

For an EC2/ECS/EKS application, prefer an IAM role instead of access keys.

Minimum S3 permissions for the application:

s3:PutObject
s3:GetObject
s3:DeleteObject (only if deletion is implemented)

Restrict the permissions to the resume bucket/prefix.

## 4. Local setup

Windows PowerShell:

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Copy .env.example to .env and fill in the values.

Run:

python app.py

Open:
http://localhost:5000

## 5. Production interview architecture

Internet
   |
Application Load Balancer
   |
Flask application (EC2/ECS/EKS)
   |----------------------|
   v                      v
Amazon RDS MySQL       Amazon S3
student details        resumes

## Security points to explain in interview

1. Passwords are never stored as plain text; Werkzeug hashes them.
2. S3 bucket remains private.
3. Application uses an IAM role rather than hard-coded AWS keys.
4. RDS should be private and reachable only from the application security group.
5. HTTPS should terminate at the ALB.
6. Database credentials should be stored in AWS Secrets Manager/SSM Parameter Store in production.
7. Resume uploads have extension and size validation.
8. S3 object names use UUIDs to avoid filename collisions.

## Next DevOps stages

GitHub -> Jenkins CI -> Docker build -> ECR -> deploy to EKS
                                           |
                                      Flask pods
                                           |
                              RDS MySQL + S3
