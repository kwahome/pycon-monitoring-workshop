from rest_framework import serializers
from app.core.models import MessageModel


class APIHeaderSerializer(serializers.Serializer):
    messageId = serializers.CharField(max_length=64)
    timestamp = serializers.DateTimeField()


class MessageObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageModel
        fields = (
            'messageId',
            'senderId',
            'recipientId',
            'messageType',
            'channel',
            'message',
            'priority'
        )


class SendMessageRequestSerializer(serializers.Serializer):
    """
    Serialize class for a send message request
    """
    header = APIHeaderSerializer(required=True)
    body = MessageObjectSerializer(many=True, allow_empty=False)
