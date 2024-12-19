#!/usr/bin/env python3

import boto3
import json
from datetime import datetime

"""
The response from boto3.client.filter_log_events has the form:
{
    'events': [
        {
            'logStreamName': 'instance-1-log-stream',
            'timestamp': 1672531200000,
            'message': '{"key": "value"}',
            'ingestionTime': 1672531234567
        },
        {
            'logStreamName': 'instance-2-log-stream',
            'timestamp': 1672531260000,
            'message': '{"key": "another-value"}',
            'ingestionTime': 1672531298765
        }
    ],
    'nextToken': 'eyJ2IjoiMSJ9...'  # A token for fetching the next page of results
}
"""


def download_logs(log_group_name, start_time, output_file):
    """
    Download logs from an AWS CloudWatch Log Group.

    Parameters:
    - log_group_name: Name of the CloudWatch Log Group
    - start_time: Start time for log filtering in ISO 8601 format
    - output_file: Filepath to save the logs in JSON format
    """
    # Convert start_time to milliseconds since epoch
    start_timestamp = int(datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S").timestamp() * 1000)

    # Initialize boto3 client
    client = boto3.client('logs')

    # Paginate through log events
    next_token = None
    all_events = []

    print(f"Fetching logs from '{log_group_name}' starting at {start_time}...")

    while True:
        params = {
            'logGroupName': log_group_name,
            'startTime': start_timestamp
        }
        if next_token:
            params['nextToken'] = next_token

        response = client.filter_log_events(**params)

        # Collect events
        events = response.get('events', [])
        all_events.extend(events)

        # Check if more results are available
        next_token = response.get('nextToken')
        if not next_token:
            break

    # Write events to JSON file
    with open(output_file, 'w') as f:
        json.dump([event['message'] for event in all_events], f, indent=4)

    print(f"Logs saved to {output_file}")


# Replace these with your values
log_group_name = "hyrax-sit"
start_time = "2024-12-18T12:15:00"  # ISO 8601 format
output_file = "cloudwatch_logs.12.18.24.json"

download_logs(log_group_name, start_time, output_file)
