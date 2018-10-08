from rest_framework import serializers


class SendMessageRequestSerializer(serializers.Serializer):
    """
    Serialize class for a send message request
    """
    messageId = serializers.CharField(max_length=64)
    messageType = serializers.CharField(max_length=16)
