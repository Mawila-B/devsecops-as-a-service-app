resource "aws_ecs_cluster" "devsecops_cluster" {
  name = "devsecops-cluster"
  
  setting {
    name = "containerInsights"
    value = "enabled"
  }
  
  tags = {
    Environment = "production"
  }
}

resource "aws_ecs_cluster_capacity_providers" "cluster_cp" {
  cluster_name = aws_ecs_cluster.devsecops_cluster.name
  capacity_providers = ["FARGATE"]
}

resource "aws_cloudwatch_log_group" "ecs_logs" {
  name = "/ecs/devsecops"
  retention_in_days = 30
}