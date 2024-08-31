from rest_framework.serializers import ModelSerializer


class BaseProjectModelSerializer(ModelSerializer):

    def create(self, validated_data):
        raise NotImplementedError(
            "You must use service instead of serializer for this action!"
        )

    def update(self, instance, validated_data):
        raise NotImplementedError(
            "You must use service instead of serializer for this action!"
        )