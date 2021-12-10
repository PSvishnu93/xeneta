from rest_framework import serializers
from rates.services import execute_query
from rates.models import Port, Region
from functools import reduce

class RateRequestSerializer(serializers.Serializer):
    date_from = serializers.DateField(required=True)
    date_to = serializers.DateField(required=True)
    origin = serializers.CharField(required=True)
    destination = serializers.CharField(required=True)

    class Query:
        FETCH_PORT = '''select id from port where code = '{}';'''
        FETCH_REGION = '''select id from region where slug = '{}';'''
        FETCH_PORT_IN_REGION = '''select port_id from port_region where region_id = '{}';'''

    def validate(self, validated_data):
        if validated_data['date_from'] > validated_data['date_to']:
            raise serializers.ValidationError("date_to should be greater than or equal to date_from")
        return validated_data
    
    def get_port(self, port: str)-> bool:
        query = self.Query.FETCH_PORT.format(port)
        return self.flatten(execute_query(query))

    def get_region(self, region: str)-> bool:
        query = self.Query.FETCH_REGION.format(region)
        return self.flatten(execute_query(query))

    def validate_origin(self, origin: str):
        return self.validate_site(origin)

    def validate_destination(self, destination: str):
        return self.validate_site(destination)

    def validate_site(self, site: str):
        port = self.get_port(site)
        if len(port) == 1:
            return '({})'.format(port[0])
        region = self.get_region(site)
        if len(region) == 1:
            ports = '{}'.format(self.get_all_ports_in_the_region (region[0]))
            if len(ports) == 0:
                raise serializers.ValidationError("No ports found in this region")
            return ports
        raise serializers.ValidationError("Invalid port or region")

    def get_all_ports_in_the_region(self, region: Region) -> list:
        query = self.Query.FETCH_PORT_IN_REGION.format(region)
        return self.flatten(execute_query(query))
    
    def flatten(self, data):
        return tuple([row[0] for row in data])
