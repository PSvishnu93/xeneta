from datetime import timedelta
from dateutil import parser
from rates.utils import execute_query

class PriceQuery:
    DAY_AVERAGE = '''select day, round(avg(price), 2) from price
where day >= '{}' and day <= '{}'
and origin_id in {} and
destination_id in {}
group by day order by day;'''

def get_day_average(parameters: dict)-> dict:
    query = PriceQuery.DAY_AVERAGE.format(
        parameters.get("date_from"),
        parameters.get("date_to"),
        parameters.get("origin"),
        parameters.get("destination")
    )
    records = execute_query(query)
    return format_response(records=records, parameters=parameters)

def format_response(records: tuple, parameters: dict):
    day = parser.parse(parameters.get("date_from")).date()
    date_to = parser.parse(parameters.get("date_to")).date()
    idx = 0
    total = len(records)
    data = []
    while day <= date_to:
        average = None
        if idx < total and records[idx][0] == day:
            average = records[idx][1]
            idx += 1
        data.append(
            {'day': day,
            'average_price': average}
        )
        day = day + timedelta(days=1)
    return data
