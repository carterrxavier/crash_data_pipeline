from google.cloud import pubsub_v1
from datetime import datetime, timedelta
import os


def get_last_message_timestamp(project_id, subscription_name):
    # Initialize Pub/Sub client
    subscriber = pubsub_v1.SubscriberClient()
    
    # Construct the full subscription path
    subscription_path = subscriber.subscription_path(project_id, subscription_name)
    
    # Get the most recent message from the subscription
    response = subscriber.pull(request={"subscription": subscription_path, "max_messages": 20})
    
    # Extract the timestamp of the most recent message
    times = []
    if response.received_messages:
        for r in response.received_messages: 
            timestamp = datetime.fromisoformat(str(r.message.publish_time))
            times.append(timestamp)
        cst_offset = timedelta(hours=-6)
        timestamp_cst = max(times) + cst_offset
        print(timestamp_cst)
        return timestamp_cst
    else:
        return None
