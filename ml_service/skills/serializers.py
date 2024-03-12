from rest_framework import serializers
from skills.models import Category, Skill
    
class SkillSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    value = serializers.CharField()
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category')

    class Meta:
        model = Skill
        fields = ['id', 'value', 'category_id']

    def create(self, validated_data):
        return Skill.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.value = validated_data.get('value', instance.value)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance
    
class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    value = serializers.CharField()
    category = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'value', 'category']

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.value = validated_data.get('value', instance.value)
        instance.save()
        return instance
