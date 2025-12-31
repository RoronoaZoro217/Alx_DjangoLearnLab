from rest_framework import serializers
from .models import ActivityLog

class ActivityLogSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id',read_only=True)
    username = serializers.CharField(source='user.username',read_only=True)

    class Meta:
        model = ActivityLog

        fields = ['id','user_id','username','action','details','ip_address','status','timestamp',]
        read_only_fields = fields