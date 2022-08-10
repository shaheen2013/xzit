from rest_framework import serializers
from .models import ReportReason

class ReportReasonSerializers(serializers.ModelSerializer):
    class Meta:
        model = ReportReason
        fields = ('id', 'reason')
        extra_kwargs = {
            'id': {'read_only': True}
        }