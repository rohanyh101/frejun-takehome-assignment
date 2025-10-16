from rest_framework import serializers
from .models import User, Team


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 
            'email', 'age', 'gender', 'is_child'
        ]
        read_only_fields = ['id', 'is_child']


class TeamMemberSerializer(serializers.ModelSerializer):
    """Simplified serializer for team members."""
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'age', 'is_child']
        read_only_fields = ['id', 'is_child']


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model."""
    
    members = TeamMemberSerializer(many=True, read_only=True)
    member_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    member_count = serializers.ReadOnlyField()
    adult_member_count = serializers.ReadOnlyField()
    child_member_count = serializers.ReadOnlyField()
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Team
        fields = [
            'id', 'name', 'members', 'member_ids', 'created_by', 'created_by_name',
            'member_count', 'adult_member_count', 'child_member_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at']
    
    def create(self, validated_data):
        member_ids = validated_data.pop('member_ids', [])
        team = Team.objects.create(**validated_data)
        
        if member_ids:
            team.members.set(member_ids)
        
        return team
    
    def update(self, instance, validated_data):
        member_ids = validated_data.pop('member_ids', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if member_ids is not None:
            instance.members.set(member_ids)
        
        return instance
