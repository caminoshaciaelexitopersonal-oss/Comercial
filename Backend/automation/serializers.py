from rest_framework import serializers
from .models import Workflow, Node, Edge

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['id', 'node_type', 'config_json', 'position_x', 'position_y']

class EdgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edge
        fields = ['id', 'source_node', 'target_node', 'condition_path']

class WorkflowDetailSerializer(serializers.ModelSerializer):
    nodes = NodeSerializer(many=True, read_only=True)
    edges = EdgeSerializer(many=True, read_only=True)

    class Meta:
        model = Workflow
        fields = ['id', 'name', 'is_active', 'nodes', 'edges']


class WorkflowCreateSerializer(serializers.ModelSerializer):
    nodes = serializers.ListField(child=serializers.DictField(), write_only=True)
    edges = serializers.ListField(child=serializers.DictField(), write_only=True)

    class Meta:
        model = Workflow
        fields = ['id', 'name', 'is_active', 'nodes', 'edges']

    def create(self, validated_data):
        nodes_data = validated_data.pop('nodes')
        edges_data = validated_data.pop('edges')

        workflow = Workflow.objects.create(**validated_data)

        node_map = {}
        for node_data in nodes_data:
            temp_id = node_data.pop('id')
            # Extraer campos que no son del modelo Node
            position_x = node_data.pop('position_x', 0)
            position_y = node_data.pop('position_y', 0)

            node = Node.objects.create(
                workflow=workflow,
                position_x=position_x,
                position_y=position_y,
                **node_data
            )
            node_map[temp_id] = node.id

        for edge_data in edges_data:
            source_id = node_map.get(str(edge_data['source_node']))
            target_id = node_map.get(str(edge_data['target_node']))

            if source_id and target_id:
                Edge.objects.create(
                    workflow=workflow,
                    source_node_id=source_id,
                    target_node_id=target_id,
                    condition_path=edge_data.get('condition_path')
                )
        return workflow

    def update(self, instance, validated_data):
        # La lógica de actualización es más compleja y se implementará si es necesario.
        # Implica borrar y recrear nodos/edges o unirlos de forma inteligente.
        instance.name = validated_data.get('name', instance.name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()

        # (Lógica de actualización de nodos y edges omitida por simplicidad inicial)

        return instance
