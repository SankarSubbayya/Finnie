#!/bin/bash

# Finnie AWS Deployment Script
# Developed by Sankar Subbayya

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REGION="us-east-1"
ECR_REPO="finnie"
CLUSTER_NAME="finnie-cluster"
SERVICE_NAME="finnie-service"
TASK_FAMILY="finnie"

echo -e "${BLUE}🚀 Finnie AWS Deployment Script${NC}"
echo -e "${BLUE}Developed by Sankar Subbayya${NC}"
echo "=================================="

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI not found. Please install it first.${NC}"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Please install it first.${NC}"
    exit 1
fi

# Get AWS account ID
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com"

echo -e "${YELLOW}📋 Deployment Configuration:${NC}"
echo "  Region: $REGION"
echo "  ECR Registry: $ECR_REGISTRY"
echo "  Cluster: $CLUSTER_NAME"
echo "  Service: $SERVICE_NAME"
echo ""

# Function to create ECR repository
create_ecr_repo() {
    echo -e "${YELLOW}📦 Creating ECR repository...${NC}"
    
    if aws ecr describe-repositories --repository-names $ECR_REPO --region $REGION &> /dev/null; then
        echo -e "${GREEN}✅ ECR repository already exists${NC}"
    else
        aws ecr create-repository --repository-name $ECR_REPO --region $REGION
        echo -e "${GREEN}✅ ECR repository created${NC}"
    fi
}

# Function to build and push Docker image
build_and_push() {
    echo -e "${YELLOW}🔨 Building Docker image...${NC}"
    
    # Login to ECR
    aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ECR_REGISTRY
    
    # Build image
    docker build -t $ECR_REPO .
    
    # Tag image
    docker tag $ECR_REPO:latest $ECR_REGISTRY/$ECR_REPO:latest
    
    # Push image
    docker push $ECR_REGISTRY/$ECR_REPO:latest
    
    echo -e "${GREEN}✅ Docker image built and pushed${NC}"
}

# Function to create ECS cluster
create_ecs_cluster() {
    echo -e "${YELLOW}🏗️ Creating ECS cluster...${NC}"
    
    if aws ecs describe-clusters --clusters $CLUSTER_NAME --region $REGION &> /dev/null; then
        echo -e "${GREEN}✅ ECS cluster already exists${NC}"
    else
        aws ecs create-cluster --cluster-name $CLUSTER_NAME --region $REGION
        echo -e "${GREEN}✅ ECS cluster created${NC}"
    fi
}

# Function to create task definition
create_task_definition() {
    echo -e "${YELLOW}📝 Creating task definition...${NC}"
    
    cat > task-definition.json << EOF
{
  "family": "$TASK_FAMILY",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::$AWS_ACCOUNT_ID:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "finnie-app",
      "image": "$ECR_REGISTRY/$ECR_REPO:latest",
      "portMappings": [
        {
          "containerPort": 8501,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "PYTHONPATH",
          "value": "/app/src"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/$TASK_FAMILY",
          "awslogs-region": "$REGION",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
EOF

    # Create CloudWatch log group
    aws logs create-log-group --log-group-name "/ecs/$TASK_FAMILY" --region $REGION 2>/dev/null || true
    
    # Register task definition
    aws ecs register-task-definition --cli-input-json file://task-definition.json --region $REGION
    echo -e "${GREEN}✅ Task definition created${NC}"
}

# Function to create ECS service
create_ecs_service() {
    echo -e "${YELLOW}🚀 Creating ECS service...${NC}"
    
    # Get default VPC and subnets
    VPC_ID=$(aws ec2 describe-vpcs --filters "Name=is-default,Values=true" --query 'Vpcs[0].VpcId' --output text)
    SUBNET_IDS=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --query 'Subnets[].SubnetId' --output text | tr '\t' ',')
    
    # Create security group
    SECURITY_GROUP_ID=$(aws ec2 create-security-group \
        --group-name finnie-sg \
        --description "Security group for Finnie app" \
        --vpc-id $VPC_ID \
        --query 'GroupId' --output text 2>/dev/null || \
        aws ec2 describe-security-groups \
        --filters "Name=group-name,Values=finnie-sg" \
        --query 'SecurityGroups[0].GroupId' --output text)
    
    # Add inbound rule for port 8501
    aws ec2 authorize-security-group-ingress \
        --group-id $SECURITY_GROUP_ID \
        --protocol tcp \
        --port 8501 \
        --cidr 0.0.0.0/0 2>/dev/null || true
    
    # Create or update service
    if aws ecs describe-services --cluster $CLUSTER_NAME --services $SERVICE_NAME --region $REGION &> /dev/null; then
        aws ecs update-service --cluster $CLUSTER_NAME --service $SERVICE_NAME --task-definition $TASK_FAMILY --region $REGION
        echo -e "${GREEN}✅ ECS service updated${NC}"
    else
        aws ecs create-service \
            --cluster $CLUSTER_NAME \
            --service-name $SERVICE_NAME \
            --task-definition $TASK_FAMILY \
            --desired-count 1 \
            --launch-type FARGATE \
            --network-configuration "awsvpcConfiguration={subnets=[$SUBNET_IDS],securityGroups=[$SECURITY_GROUP_ID],assignPublicIp=ENABLED}" \
            --region $REGION
        echo -e "${GREEN}✅ ECS service created${NC}"
    fi
}

# Function to get service URL
get_service_url() {
    echo -e "${YELLOW}🔍 Getting service URL...${NC}"
    
    # Get task ARN
    TASK_ARN=$(aws ecs list-tasks --cluster $CLUSTER_NAME --service-name $SERVICE_NAME --region $REGION --query 'taskArns[0]' --output text)
    
    if [ "$TASK_ARN" != "None" ] && [ "$TASK_ARN" != "" ]; then
        # Get public IP
        PUBLIC_IP=$(aws ecs describe-tasks --cluster $CLUSTER_NAME --tasks $TASK_ARN --region $REGION --query 'tasks[0].attachments[0].details[?name==`networkInterfaceId`].value' --output text | xargs -I {} aws ec2 describe-network-interfaces --network-interface-ids {} --query 'NetworkInterfaces[0].Association.PublicIp' --output text)
        
        if [ "$PUBLIC_IP" != "None" ] && [ "$PUBLIC_IP" != "" ]; then
            echo -e "${GREEN}🎉 Deployment successful!${NC}"
            echo -e "${GREEN}🌐 Finnie is available at: http://$PUBLIC_IP:8501${NC}"
        else
            echo -e "${YELLOW}⚠️ Service is running but public IP not available yet${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️ Service is starting up...${NC}"
    fi
}

# Main deployment flow
main() {
    echo -e "${BLUE}Starting deployment process...${NC}"
    
    create_ecr_repo
    build_and_push
    create_ecs_cluster
    create_task_definition
    create_ecs_service
    
    echo -e "${YELLOW}⏳ Waiting for service to start...${NC}"
    sleep 30
    
    get_service_url
    
    echo -e "${GREEN}✅ Deployment completed!${NC}"
    echo -e "${BLUE}📊 Monitor your service in the AWS ECS console${NC}"
    echo -e "${BLUE}📝 Check CloudWatch logs for application logs${NC}"
    
    # Cleanup
    rm -f task-definition.json
}

# Run main function
main "$@"
