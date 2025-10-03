# AWS Deployment Guide for Finnie

## 🚀 Deployment Complexity: **EASY to MODERATE**

Finnie is well-architected for AWS deployment with modern containerization and cloud-native patterns.

## 📊 Deployment Architecture Options

### Option 1: **Simple Container Deployment** (Easiest - 30 minutes)
```mermaid
graph TB
    subgraph "AWS Simple Setup"
        A[EC2 Instance] --> B[Docker Container]
        B --> C[Streamlit App]
        B --> D[SQLite DB]
        B --> E[Local Vector Store]
    end
    
    F[Route 53] --> G[Application Load Balancer]
    G --> A
    H[CloudWatch] --> A
```

### Option 2: **Production-Ready Architecture** (Moderate - 2-3 hours)
```mermaid
graph TB
    subgraph "AWS Production Setup"
        A[CloudFront CDN] --> B[Application Load Balancer]
        B --> C[ECS Fargate Cluster]
        
        subgraph "ECS Services"
            D[Streamlit Service]
            E[LangGraph Workers]
            F[RAG Service]
        end
        
        subgraph "Data Layer"
            G[RDS PostgreSQL]
            H[OpenSearch/Elasticsearch]
            I[S3 Bucket]
        end
        
        subgraph "External APIs"
            J[Market Data APIs]
            K[News APIs]
        end
        
        C --> D
        C --> E
        C --> F
        D --> G
        E --> H
        F --> I
        E --> J
        E --> K
    end
```

## 🛠️ Step-by-Step Deployment

### **Quick Start (Option 1) - 30 minutes**

#### 1. **Prepare for Deployment**
```bash
# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.12-slim

WORKDIR /app
COPY . .

# Install uv and dependencies
RUN pip install uv
RUN uv sync --all-extras

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
EOF

# Build and test locally
docker build -t finnie-app .
docker run -p 8501:8501 finnie-app
```

#### 2. **Deploy to EC2**
```bash
# Launch EC2 instance (t3.medium recommended)
# Install Docker
sudo yum update -y
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker

# Deploy your app
git clone https://github.com/your-username/finnie.git
cd finnie
docker build -t finnie-app .
docker run -d -p 80:8501 --name finnie finnie-app
```

#### 3. **Configure Load Balancer**
- Create Application Load Balancer
- Point to EC2 instance
- Configure health checks on port 8501
- Set up Route 53 domain

### **Production Deployment (Option 2) - 2-3 hours**

#### 1. **Container Registry Setup**
```bash
# Build and push to ECR
aws ecr create-repository --repository-name finnie
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

docker build -t finnie .
docker tag finnie:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/finnie:latest
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/finnie:latest
```

#### 2. **ECS Fargate Setup**
```yaml
# ecs-task-definition.json
{
  "family": "finnie",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "finnie-app",
      "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/finnie:latest",
      "portMappings": [
        {
          "containerPort": 8501,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "postgresql://user:pass@rds-endpoint:5432/finnie"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/finnie",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### 3. **Database Setup**
```bash
# RDS PostgreSQL
aws rds create-db-instance \
  --db-instance-identifier finnie-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username finnie \
  --master-user-password YourSecurePassword123 \
  --allocated-storage 20
```

#### 4. **Vector Store Setup**
```bash
# OpenSearch (for production vector search)
aws opensearch create-domain \
  --domain-name finnie-vectors \
  --cluster-config InstanceType=t3.small.search,InstanceCount=1
```

## 💰 Cost Estimation

### **Simple Deployment (Option 1)**
- **EC2 t3.medium**: ~$30/month
- **Application Load Balancer**: ~$16/month
- **Route 53**: ~$0.50/month
- **Total**: ~$46.50/month

### **Production Deployment (Option 2)**
- **ECS Fargate (1 vCPU, 2GB)**: ~$25/month
- **RDS PostgreSQL t3.micro**: ~$15/month
- **OpenSearch t3.small**: ~$30/month
- **Application Load Balancer**: ~$16/month
- **S3 Storage**: ~$5/month
- **Total**: ~$91/month

## 🔧 Required AWS Services

| Service | Purpose | Required |
|---------|---------|----------|
| **EC2** | Compute (simple) | Option 1 |
| **ECS Fargate** | Container orchestration | Option 2 |
| **ECR** | Container registry | Option 2 |
| **RDS** | Database | Option 2 |
| **OpenSearch** | Vector search | Option 2 |
| **S3** | File storage | Option 2 |
| **ALB** | Load balancing | Both |
| **Route 53** | DNS | Both |
| **CloudWatch** | Monitoring | Both |
| **IAM** | Security | Both |

## 🚀 Deployment Scripts

### **Quick Deploy Script**
```bash
#!/bin/bash
# quick-deploy.sh

echo "🚀 Deploying Finnie to AWS..."

# Build Docker image
docker build -t finnie-app .

# Launch EC2 instance
aws ec2 run-instances \
  --image-id ami-0c02fb55956c7d316 \
  --instance-type t3.medium \
  --key-name your-key-pair \
  --security-group-ids sg-12345678 \
  --user-data '#!/bin/bash
    yum update -y
    yum install -y docker
    systemctl start docker
    systemctl enable docker
    usermod -a -G docker ec2-user
  '

echo "✅ Deployment initiated! Check EC2 console for instance details."
```

### **Production Deploy Script**
```bash
#!/bin/bash
# production-deploy.sh

echo "🏗️ Deploying Finnie Production Environment..."

# Create ECR repository
aws ecr create-repository --repository-name finnie --region us-east-1

# Build and push image
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_REGISTRY
docker build -t finnie .
docker tag finnie:latest $ECR_REGISTRY/finnie:latest
docker push $ECR_REGISTRY/finnie:latest

# Create RDS database
aws rds create-db-instance \
  --db-instance-identifier finnie-prod \
  --db-instance-class db.t3.small \
  --engine postgres \
  --master-username finnie \
  --master-user-password $DB_PASSWORD \
  --allocated-storage 20

# Create ECS cluster
aws ecs create-cluster --cluster-name finnie-cluster

# Register task definition
aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json

# Create service
aws ecs create-service \
  --cluster finnie-cluster \
  --service-name finnie-service \
  --task-definition finnie:1 \
  --desired-count 1

echo "✅ Production deployment completed!"
```

## 🔒 Security Considerations

### **IAM Roles & Policies**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "rds:DescribeDBInstances",
        "opensearch:ESHttpGet",
        "opensearch:ESHttpPost",
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "*"
    }
  ]
}
```

### **Environment Variables**
```bash
# .env.production
DATABASE_URL=postgresql://user:pass@rds-endpoint:5432/finnie
OPENSEARCH_URL=https://search-finnie-vectors.us-east-1.es.amazonaws.com
S3_BUCKET=finnie-storage
OPENAI_API_KEY=your-key
ALPHA_VANTAGE_API_KEY=your-key
```

## 📊 Monitoring & Logging

### **CloudWatch Dashboard**
```json
{
  "widgets": [
    {
      "type": "metric",
      "properties": {
        "metrics": [
          ["AWS/ECS", "CPUUtilization"],
          ["AWS/ECS", "MemoryUtilization"],
          ["AWS/ApplicationELB", "TargetResponseTime"]
        ],
        "period": 300,
        "stat": "Average",
        "region": "us-east-1",
        "title": "Finnie Performance"
      }
    }
  ]
}
```

## 🚀 CI/CD Pipeline

### **GitHub Actions Workflow**
```yaml
# .github/workflows/deploy.yml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Build and push to ECR
        run: |
          aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_REGISTRY
          docker build -t finnie .
          docker tag finnie:latest $ECR_REGISTRY/finnie:latest
          docker push $ECR_REGISTRY/finnie:latest
      
      - name: Deploy to ECS
        run: |
          aws ecs update-service --cluster finnie-cluster --service finnie-service --force-new-deployment
```

## ✅ Pre-Deployment Checklist

- [ ] Docker image builds successfully
- [ ] Environment variables configured
- [ ] Database migrations ready
- [ ] SSL certificates obtained
- [ ] Domain configured
- [ ] Monitoring alerts set up
- [ ] Backup strategy defined
- [ ] Security groups configured
- [ ] IAM roles created
- [ ] Load balancer health checks configured

## 🎯 Deployment Difficulty Summary

| Aspect | Difficulty | Time Required |
|--------|------------|---------------|
| **Simple EC2 Deploy** | ⭐⭐ Easy | 30 minutes |
| **Production ECS** | ⭐⭐⭐ Moderate | 2-3 hours |
| **Database Setup** | ⭐⭐ Easy | 30 minutes |
| **Security Config** | ⭐⭐⭐ Moderate | 1 hour |
| **Monitoring Setup** | ⭐⭐ Easy | 30 minutes |
| **CI/CD Pipeline** | ⭐⭐⭐ Moderate | 1 hour |

## 🚀 Next Steps

1. **Choose your deployment option** (Simple vs Production)
2. **Set up AWS account** and configure CLI
3. **Run the deployment script** for your chosen option
4. **Configure monitoring** and alerts
5. **Set up CI/CD** for automated deployments

**Total deployment time: 30 minutes to 3 hours depending on complexity!**

---

*Developed by Sankar Subbayya | Finnie - Financial AI Engine*
