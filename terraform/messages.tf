resource "aws_sns_topic" "spam_topic" {
  name = "spam-topic"
}

resource "aws_sns_topic_policy" "email_notification_topic_policy" {
  arn    = aws_sns_topic.spam_topic.arn
  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "sns:Publish",
      "Resource": "${aws_sns_topic.spam_topic.arn}"
    }
  ]
}
POLICY
}

resource "aws_sqs_queue" "spam_filter_queue" {
  name                       = "spam-filter-queue"
  visibility_timeout_seconds = 120
  message_retention_seconds  = 86400
  receive_wait_time_seconds  = 10
}

resource "aws_sqs_queue_policy" "spam_filter_queue_policy" {
  queue_url = aws_sqs_queue.spam_filter_queue.id
  policy    = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "sqs:SendMessage",
      "Resource": "${aws_sqs_queue.spam_filter_queue.arn}"
    }
  ]
}
POLICY
}

resource "aws_lambda_event_source_mapping" "sqs_trigger" {
  event_source_arn = aws_sqs_queue.spam_filter_queue.arn
  function_name    = module.dockerized_lambdas.lambdas["spam_detector"].arn
  batch_size       = 10
  enabled          = true
}
