from collections import defaultdict
from datetime import datetime

from app.auth import Auth
from app.db import get_db
from app.profile import Member


class Admin(Member):

    @classmethod
    def list_members(cls):
        members = defaultdict(list)
        db = get_db()
        for info in db.members.find({'uid': {'$gte': 1000}}):
            members[info['position']].append(Member(info))
        # sort by admission date
        for position in members:
            members[position].sort(
                key=lambda x: ''.join(reversed(x.from_date.split('/'))))
        return members

    @classmethod
    def get_next_uid(cls):
        db = get_db()
        res = db.counters.find_one_and_update(
            {'_id': 'uid'}, {'$inc': {'next_uid': 1}})
        return res['next_uid']

    @classmethod
    def add_member(cls, form):
        created_time = datetime.utcnow()
        member_info = cls.form2info(form)
        member_info['created_time'] = created_time
        member_info['uid'] = cls.get_next_uid()
        member_info['publications'] = []
        member_info['avatar_url'] = '/static/img/avatar/default.png'
        db = get_db()
        try:
            db.members.insert_one(member_info)
        except:
            return False
        else:
            username = member_info['en_name'].replace(' ', '').lower()
            Auth.add_new_user(member_info['uid'], username)
            return True

    @classmethod
    def update_member(cls, uid, form):
        member_info = cls.form2info(form)
        db = get_db()
        db.members.update_one({'uid': uid}, {'$set': member_info})
        return True

    @classmethod
    def delete_member(cls, uid):
        db = get_db()
        db.members.delete_one({'uid': uid})
        db.auth.delete_one({'uid': uid})
        return True

    @classmethod
    def list_publications(cls):
        db = get_db()
        members = db.members.find({'publications': {'$exists': True}})
        publications = {}
        for member in members:
            for item in member['publications']:
                if item['ID'] not in publications:
                    publications[item['ID']] = item
        return publications.values()
