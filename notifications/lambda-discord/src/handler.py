import json
import os
import requests

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]


def lambda_handler(event, context):
    alarm = json.loads(event["Records"][0]["Sns"]["Message"])

    alarm_name = alarm.get("AlarmName", "Unknown")
    state = alarm.get("NewStateValue", "Unknown")
    reason = alarm.get("NewStateReason", "No reason provided")
    region = alarm.get("Region", "Unknown")
    time = alarm.get("StateChangeTime", "Unknown")

    dimensions = alarm.get("Trigger", {}).get("Dimensions", [])
    function_name = "Unknown"

    for d in dimensions:
        if d.get("name") == "FunctionName":
            function_name = d.get("value")
            break

    content = (
        "🚨 **AWS Pipeline Failure**\n\n"
        f"**Lambda Function:** `{function_name}`\n"
        f"**Alarm:** `{alarm_name}`\n"
        f"**State:** 🔴 {state}\n\n"
        f"**Reason:**\n{reason}\n\n"
        f"**Region:** {region}\n"
        f"**Time:** {time}"
    )

    response = requests.post(
        WEBHOOK_URL,
        json={"content": content},
        timeout=10,
    )

    response.raise_for_status()

    return {
        "statusCode": 200,
        "body": json.dumps("Notification sent.")
    }