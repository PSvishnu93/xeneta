import pandas as pd
from django.conf import settings
from rates.models import Port, Region, Price, PortRegion
from django.db import connection

def execute_query(query):
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def add_regions(regions: pd.DataFrame):
        Region.objects.all().delete()
        for _, row in regions.iterrows():
            parent = None
            if row['parent_slug']:
                parent = Region.objects.get(slug=row['parent_slug'])
            Region.objects.create(
                slug=row['slug'], parent=parent, name=row['name']
            )

def add_ports(ports: pd.DataFrame):
    Port.objects.all().delete()
    for _, row in ports.iterrows():
        port = Port.objects.create(
            name=row['name'], code=row['code'])
        region = Region.objects.get(slug=row['parent_slug'])
        port_region = PortRegion.objects.create(port=port, region=region)
        while port_region.region.parent:
            port_region = PortRegion.objects.create(port=port, region=port_region.region.parent)

def add_prices(prices: pd.DataFrame):
    Price.objects.all().delete()
    for _, row in prices.iterrows():
        origin = Port.objects.get(code=row['orig_code'])
        destination = Port.objects.get(code=row['dest_code'])
        Price.objects.create(
            origin=origin, destination=destination,
            day=row['day'], price=row['price']
        )