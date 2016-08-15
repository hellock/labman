from collections import Counter, defaultdict, OrderedDict

from app.db import get_db


class Stats(object):

    @classmethod
    def by_supervisor(cls):
        db = get_db()
        members = db.members.find(
            {'uid': {'$gte': 1000}, 'supervisor': {'$ne': 'None'}})
        positions = []
        counters = defaultdict(Counter)
        for member in members:
            if member['supervisor']:
                counters[member['supervisor']].update([member['position']])
                if member['position'] not in positions:
                    positions.append(member['position'])
        ret_data = {}
        ret_data['x_val'] = list(counters.keys())
        ret_data['y_val'] = defaultdict(list)
        for position in positions:
            for supervisor in ret_data['x_val']:
                ret_data['y_val'][position].append(counters[supervisor][position])
        return ret_data

    @classmethod
    def by_admission_year(cls):
        db = get_db()
        members = db.members.find(
            {'uid': {'$gte': 1000}, 'position': {'$ne': 'Professor'}})
        years = defaultdict(int)
        for member in members:
            if not member['from_date']:
                years['unknown'] += 1
            else:
                year = member['from_date'].split('/')[-1]
                years[year] += 1
        years = OrderedDict(sorted(years.items()))
        ret_data = {}
        ret_data['x_val'] = list(years.keys())
        ret_data['y_val'] = {'Student': list(years.values())}
        return ret_data
