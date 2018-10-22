from rest_framework import serializers
from app.core.models import MessageChannels, MessageTypes


class SendMessageRequestSerializer(serializers.Serializer):
    """
    Serialize class for a send message request
    """
    messageId = serializers.CharField(max_length=64, required=True)
    senderId = serializers.CharField(max_length=64, required=True)
    recipients = serializers.ListField(
        child=serializers.CharField(max_length=64), allow_empty=False
    )
    messageType = serializers.ChoiceField(
        choices=MessageTypes.yield_choices(), required=True
    )
    channel = serializers.ChoiceField(
        choices=MessageChannels.yield_choices(), required=True
    )
    message = serializers.CharField(max_length=200)
    priority = serializers.CharField(max_length=64)
