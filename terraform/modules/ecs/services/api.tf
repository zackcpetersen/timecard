locals {
  nginx_container_name = "${var.name}_nginx"
  web_container_name   = "${var.name}_web"
  ports                = [80, 443]
}

# Configure logging for service
resource "aws_cloudwatch_log_group" "ecs_logs" {
  name              = "${var.name}_${var.env}"
  retention_in_days = 30
  tags              = var.tags
}

# create task definition
resource "aws_ecs_task_definition" "api" {
  family                   = "${var.name}-api"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 1024 # TODO maybe?
  memory                   = 2048 # TODO maybe?
  execution_role_arn       = var.ecs_execution_role
  task_role_arn            = var.ecs_task_role
  tags                     = var.tags
  container_definitions = jsonencode([
    {
      logConfiguration : {
        "logDriver" : "awslogs",
        "options" : {
          "awslogs-group" : aws_cloudwatch_log_group.ecs_logs.name,
          "awslogs-region" : var.aws_region,
          "awslogs-stream-prefix" : "ecs"
        }
      },
      portMappings : [
        {
          "hostPort" : 8000,
          "protocol" : "tcp",
          "containerPort" : 8000
        }
      ],
      cpu : 768,
      environment : [
        {
          "name" : "DJANGO_SETTINGS_MODULE",
          "value" : "timecard.settings.docker"
        },
        {
          "name" : "DEBUG",
          "value" : var.debug
        },
        {
          "name" : "CORS_ALLOW_ALL_ORIGINS",
          "value" : var.cors_allow_all_origins
        },
        {
          "name" : "CORS_ALLOWED_ORIGIN_REGEXES",
          "value" : var.cors_allowed_regexes
        },
        {
          "name" : "ALLOWED_HOSTS",
          "value" : var.allowed_hosts
        },
        {
          "name" : "SECURE_SSL_REDIRECT",
          "value" : var.ssl_redirect
        },
        {
          "name" : "DEFAULT_DOMAIN",
          "value" : var.default_domain
        },
        {
          "name" : "FRONTEND_URL",
          "value" : var.frontend_url
        },
        {
          "name" : "DB_NAME",
          "value" : var.db_name
        },
        {
          "name" : "DB_USER",
          "value" : var.db_user
        },
        {
          "name" : "DB_HOST",
          "value" : var.db_host
        },
        {
          "name" : "DB_PORT",
          "value" : tostring(var.db_port)
        },
        {
          "name" : "AWS_STORAGE_BUCKET_NAME",
          "value" : var.s3_static_bucket_name
        },
        {
          "name" : "USE_S3",
          "value" : "True"
        },
        {
          "name" : "STATICFILES_STORAGE",
          "value" : "storages.backends.s3boto3.S3Boto3Storage"
        },
        {
          "name" : "DEFAULT_FILE_STORAGE",
          "value" : "storages.backends.s3boto3.S3Boto3Storage"
        },
        {
          "name" : "GMAIL_CLIENT_ID",
          "value" : var.gmail_client_id
        },
        {
          "name" : "GMAIL_PROJECT_ID",
          "value" : var.gmail_project_id
        }
      ],
      mountPoints : [],
      secrets : [
        {
          "valueFrom" : aws_secretsmanager_secret_version.gmail_client_secret.arn,
          "name" : "GMAIL_CLIENT_SECRET",
        },
        {
          "valueFrom" : aws_secretsmanager_secret_version.django_secret_key.arn,
          "name" : "SECRET_KEY",
        },
        {
          "valueFrom" : aws_secretsmanager_secret_version.db_password.arn,
          "name" : "DB_PASSWORD",
        }
      ],
      memoryReservation : 1792, # TODO maybe?
      volumesFrom : [],
      image : "${var.ghcr_base_url}/web:${var.image_tag}",
      repositoryCredentials : {
        "credentialsParameter" : aws_secretsmanager_secret_version.github_token.arn
      },
      healthCheck : {
        "retries" : 3,
        "command" : [
          "CMD-SHELL",
          "python manage.py check"
        ],
        "timeout" : 5,
        "interval" : 30,
        "startPeriod" : 60
      },
      essential : true,
      links : [],
      dockerLabels : {
        "name" : "${local.web_container_name}-${var.env}",
        "env" : var.env
      },
      name : local.web_container_name
    },
    {
      logConfiguration : {
        "logDriver" : "awslogs",
        "options" : {
          "awslogs-group" : aws_cloudwatch_log_group.ecs_logs.name,
          "awslogs-region" : var.aws_region,
          "awslogs-stream-prefix" : "ecs"
        }
      },
      entryPoint : [],
      portMappings : [
        {
          "hostPort" : 80,
          "protocol" : "tcp",
          "containerPort" : 80
        }
      ],
      command : [],
      cpu : 0,
      environment : [],
      mountPoints : [],
      memoryReservation : 256,
      volumesFrom : [],
      image : "${var.ghcr_base_url}/nginx:${var.image_tag}",
      repositoryCredentials : {
        "credentialsParameter" : aws_secretsmanager_secret_version.github_token.arn
      },
      dependsOn : [
        {
          "containerName" : local.web_container_name,
          "condition" : "HEALTHY"
        }
      ],
      essential : true,
      links : [],
      name : local.nginx_container_name
    }
    ],
  )
}

# ECS service
resource "aws_ecs_service" "ecs_api" {
  name                               = "${var.name}_api"
  cluster                            = var.cluster_id
  task_definition                    = aws_ecs_task_definition.api.arn
  desired_count                      = 1
  depends_on                         = [var.ecs_execution_role, var.ecs_task_role, aws_lb_target_group.ecs_lb_api_target_group]
  launch_type                        = "FARGATE"
  wait_for_steady_state              = true
  force_new_deployment               = true
  deployment_minimum_healthy_percent = 100
  tags                               = var.tags

  load_balancer {
    target_group_arn = aws_lb_target_group.ecs_lb_api_target_group.arn
    container_name   = local.nginx_container_name
    container_port   = 80
  }

  network_configuration {
    subnets          = var.public_subnets
    security_groups  = [aws_security_group.ecs_api_lb_sg.id]
    assign_public_ip = true
  }

  lifecycle {
    ignore_changes = [desired_count]
  }
}

# create security group for ECS load balancer
resource "aws_security_group" "ecs_api_lb_sg" {
  name        = "${var.name}-ecs-api-sg"
  description = "Allows access to port 80, 443 inside ${var.name} ECS tasks from load balancer"
  vpc_id      = var.vpc_id
  tags        = var.tags

  dynamic "ingress" {
    for_each = local.ports

    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

# create load balancer
resource "aws_lb" "ecs_api_lb" {
  name               = "${var.env}-${var.name}-ecs-api-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.ecs_api_lb_sg.id]
  subnets            = var.public_subnets
  # enable_deletion_protection = true # TODO

  #   access_logs {
  #     bucket = ""  # TODO create bucket for all ECS logs
  #     prefix = "${var.env}-${var.name}-ecs-lb"
  #     enabled = true
  #   }

  tags = var.tags
}

# load balancer target group for ECS
resource "aws_lb_target_group" "ecs_lb_api_target_group" {
  name        = "ecs-${var.name}-api-${var.env}"
  port        = 80
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = var.vpc_id
  tags        = var.tags

  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 4
    interval            = 60
    matcher             = "200-499"
    path                = "/api/"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 20
  }
}

# add listener for port 80 on loadbalancer
resource "aws_lb_listener" "port_80" {
  load_balancer_arn = aws_lb.ecs_api_lb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.ecs_lb_api_target_group.arn
  }

  tags = var.tags
}

# TODO: add listener for port 443 on loadbalancer
# add listener for port 443 on load balancer
# resource "aws_lb_listener" "port_443" {
#   load_balancer_arn = aws_lb.ecs_api_lb.arn
#   port              = "443"
#   protocol          = "HTTPS"
#   ssl_policy        = "ELBSecurityPolicy-2016-08"
#   certificate_arn   = "arn:aws:acm:us-west-2:253104389312:certificate/dc5098e7-e45a-41a9-ab5b-c0de03c27165"

#   default_action {
#     type             = "forward"
#     target_group_arn = aws_lb_target_group.ecs_lb_api_target_group.arn
#   }

#   tags = var.tags
# }

# Add Application Autoscaling for ECS Service
resource "aws_appautoscaling_target" "api_scaling_target" {
  max_capacity       = 3
  min_capacity       = 1
  resource_id        = "service/${var.cluster_name}/${aws_ecs_service.ecs_api.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "api_scaling_policy" {
  name               = "scale-up-70"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.api_scaling_target.resource_id
  scalable_dimension = aws_appautoscaling_target.api_scaling_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.api_scaling_target.service_namespace

  target_tracking_scaling_policy_configuration {
    target_value       = 70
    scale_out_cooldown = 300
    scale_in_cooldown  = 300

    customized_metric_specification {
      metric_name = "ECSServiceAverageCPUUtilization"
      namespace   = "ECSCPUAutoScaling"
      statistic   = "Average"
      unit        = "Percent"
    }
  }
}
