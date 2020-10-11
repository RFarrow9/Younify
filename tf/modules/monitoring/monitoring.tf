resource "aws_budgets_budget" "main" {
  name = "younify_costs"
  budget_type = "COST"
  limit_amount = "50"
  limit_unit = "USD"
  time_period_start = "2017-07-01_00:00"
  time_period_end = "2087-06-15_00:00"
  time_unit = "MONTHLY"
  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = ["rob.farrow@hotmail.com"]
  }
  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = ["rob.farrow@hotmail.com"]
  }
  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 50
    threshold_type             = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = ["rob.farrow@hotmail.com"]
  }
  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 50
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = ["rob.farrow@hotmail.com"]
  }

}