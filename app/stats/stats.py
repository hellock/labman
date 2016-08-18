from collections import Counter, defaultdict, OrderedDict

from app import CONFIG
from app.db import get_db
from app.member import Member


class Stats(object):

    @classmethod
    def by_supervisor(cls):
        db = get_db()
        members = db.members.find(
            {'uid': {'$gte': 1000},
             'state': {'$eq': 'Present'},
             'supervisor': {'$ne': 'None'}}
        )
        positions = []
        counters = defaultdict(Counter)
        for member in members:
            if member['supervisor']:
                counters[member['supervisor']].update([member['position']])
                if member['position'] not in positions:
                    positions.append(member['position'])
        position_map = {}
        for position_id, position in CONFIG['positions']:
            position_map[position_id] = position
        ret_data = {}
        ret_data['x_val'] = list(counters.keys())
        ret_data['y_val'] = defaultdict(list)
        for position in positions:
            for supervisor in ret_data['x_val']:
                ret_data['y_val'][position_map[position]].append(
                    counters[supervisor][position])
        return ret_data

    @classmethod
    def by_admission_year(cls):
        db = get_db()
        members = db.members.find(
            {'uid': {'$gte': 1000},
             'position': {'$nin': CONFIG['supervisor_positions']},
             'state': {'$ne': 'Candidate'}}
        )
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

    @classmethod
    def pubs_by_year(cls):
        years = defaultdict(int)
        for pub in Member.list_publications():
            years[pub['year']] += 1
        years = OrderedDict(sorted(years.items()))
        ret_data = {}
        ret_data['x_val'] = list(years.keys())
        ret_data['y_val'] = {'Student': list(years.values())}
        return ret_data
