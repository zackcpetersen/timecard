locals {
  nginx_container_name = "${var.name}_nginx"
  web_container_name   = "${var.name}_web"
  ports                = [80, 443]
}

data "aws_ecr_image" "web" {
  repository_name = var.ecr_web_repo_name
  image_tag       = var.latest_tag
}

data "aws_ecr_image" "nginx" {
  repository_name = var.ecr_nginx_repo_name
  image_tag       = var.latest_tag
}

data "aws_ecr_repository" "web" {
  name = var.ecr_web_repo_name
}

data "aws_ecr_repository" "nginx" {
  name = var.ecr_nginx_repo_name
}

# Configure logging for service
resource "aws_cloudwatch_log_group" "ecs_logs" {
  name              = "${var.name}_${var.env}"
  retention_in_days = 30
  tags              = var.tags
}

# create task definition
# TODOS
#  - update DEBUG to False
#  - set SECURE_SSL_REDIRECT to True
resource "aws_ecs_task_definition" "api" {
  family                   = "${var.name}-api"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 1024 # TODO maybe?
  memory                   = 2048 # TODO maybe?
  execution_role_arn       = var.ecs_task_execution_role
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
      # TODO update env vars to match timecard
      environment : [
        {
          "name" : "DEBUG",
          "value" : var.debug
        },
        {
          "name" : "ENV",
          "value" : var.env
        },
        {
          "name" : "DJANGO_SETTINGS_MODULE",
          "value" : "${var.github_repo}.settings.docker"
        },
        {
          "name" : "SECURE_SSL_REDIRECT",
          "value" : var.ssl_redirect
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
          "name" : "EMAIL_HOST",
          "value" : var.email_host
        },
        {
          "name" : "EMAIL_PORT",
          "value" : tostring(var.email_port)
        },
        {
          "name" : "EMAIL_HOST_USER",
          "value" : var.email_host_user
        },
        {
          "name" : "EMAIL_USE_TLS",
          "value" : var.email_use_tls
        },
        {
          "name" : "DEFAULT_FROM_EMAIL",
          "value" : var.default_from_email
        },
        {
          "name" : "CELERY_TASK_ALWAYS_EAGER",
          "value" : "True"
        },
        {
          "name" : "DEFAULT_FILE_STORAGE",
          "value" : "${var.github_repo}.storage_backends.PublicMediaStorage"
        },
        {
          "name" : "STATICFILES_STORAGE",
          "value" : "${var.github_repo}.storage_backends.StaticStorage"
        },
        {
          "name" : "USE_S3",
          "value" : "True"
        },
        {
          "name" : "AWS_STORAGE_BUCKET_NAME",
          "value" : var.s3_static_bucket_name
        },
        {
          "name" : "AWS_QUERYSTRING_AUTH",
          "value" : "False"
        },
        {
          "name" : "DB_PORT",
          "value" : tostring(var.db_port)
        },
        {
          "name" : "DB_USER",
          "value" : var.db_user
        },
        {
          "name" : "DB_NAME",
          "value" : var.db_name
        },
        {
          "name" : "DB_HOST",
          "value" : var.db_host
        },
      ],
      mountPoints : [],
      secrets : [
        {
          "valueFrom" : aws_ssm_parameter.django_secret_key.arn,
          "name" : reverse(split("/", aws_ssm_parameter.django_secret_key.name))[0]
        },
        {
          "valueFrom" : data.aws_ssm_parameter.db_password.arn,
          "name" : reverse(split("/", data.aws_ssm_parameter.db_password.name))[0]
        },
        {
          "valueFrom" : aws_ssm_parameter.aws_access_key_id.arn,
          "name" : reverse(split("/", aws_ssm_parameter.aws_access_key_id.name))[0]
        },
        {
          "valueFrom" : aws_ssm_parameter.aws_secret_access_key.arn,
          "name" : reverse(split("/", aws_ssm_parameter.aws_secret_access_key.name))[0]
        },
        {
          "valueFrom" : aws_ssm_parameter.email_host_password.arn,
          "name" : reverse(split("/", aws_ssm_parameter.email_host_password.name))[0]
        }
      ],
      memoryReservation : 1792, # TODO maybe?
      volumesFrom : [],
      image : "${data.aws_ecr_repository.web.repository_url}:${var.latest_tag}@${data.aws_ecr_image.web.image_digest}",
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
      image : "${data.aws_ecr_repository.nginx.repository_url}:${var.latest_tag}@${data.aws_ecr_image.nginx.image_digest}",
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
  depends_on                         = [var.ecs_task_execution_role, aws_lb_target_group.ecs_lb_api_target_group]
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
    matcher             = "200-499" # TODO "200,418" # 418 is custom status code returned by nginx for DisallowedHosts errors
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

# add listener for port 443 on load balancer
resource "aws_lb_listener" "port_443" {
  load_balancer_arn = aws_lb.ecs_api_lb.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = "arn:aws:acm:us-west-2:253104389312:certificate/dc5098e7-e45a-41a9-ab5b-c0de03c27165"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.ecs_lb_api_target_group.arn
  }

  tags = var.tags
}

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
