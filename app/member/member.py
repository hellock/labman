from collections import defaultdict, Mapping
from datetime import datetime

import bibtexparser

from app.db import get_db


class Member(object):

    @classmethod
    def get_next_uid(cls):
        db = get_db()
        res = db.counters.find_one_and_update(
            {'_id': 'uid'}, {'$inc': {'next_uid': 1}})
        return res['next_uid']

    @classmethod
    def get_by_uid(cls, uid):
        info = cls._db_find({'uid': uid}, target='one')
        return Member(info)

    @classmethod
    def list_all(cls, state='Present'):
        members = defaultdict(list)
        for info in cls._db_find({'state': state}):
            members[info['position']].append(Member(info))
        # sort by admission date
        for position in members:
            members[position].sort(
                key=lambda x: ''.join(reversed(x.from_date.split('/'))))
        return members

    @classmethod
    def list(cls, position, only_present=True):
        members = []
        conditions = {'position': position}
        if only_present:
            conditions['state'] = 'Present'
        for info in cls._db_find(conditions):
            members.append(Member(info))
        members.sort(
            key=lambda x: ''.join(reversed(x.from_date.split('/'))))
        return members

    @classmethod
    def search(cls, keyword):
        members = defaultdict(list)
        for info in cls._db_find({'$text': {'$search': keyword}}):
            members[info['position']].append(Member(info))
        return members

    @classmethod
    def get_comments(cls, uid):
        db = get_db()
        comments = db.comments.find_one({'uid': uid})
        if comments:
            return comments['comments']
        else:
            return []

    @classmethod
    def list_publications(cls):
        members_with_pub = cls._db_find({'publications': {'$exists': True}})
        publications = {}
        for member in members_with_pub:
            for item in member['publications']:
                unique_title = item['title'].lower()
                if unique_title not in publications:
                    publications[unique_title] = item
        return publications.values()

    @classmethod
    def new(cls, form=None):
        member = Member()
        try:
            member.uid = cls.get_next_uid()
            if form is None:
                member.create()
            else:
                member.update(form)
        except:
            return False
        else:
            return member

    @classmethod
    def delete(cls, uid):
        db = get_db()
        db.members.delete_one({'uid': uid})
        return True

    def __init__(self, info=None):
        profile = defaultdict(str)
        if info:
            profile.update(info)
        self.uid = profile['uid'] if profile['uid'] else 0
        self.en_name = profile['en_name']
        self.zh_name = profile['zh_name']
        self.state = profile['state'] if profile['state'] else 'Present'
        self.position = profile['position'] if profile['position'] else 'Others'
        self.sex = profile['sex'] if profile['sex'] else 'Male'
        self.birthdate = profile['birthdate']
        self.email = profile['email']
        self.supervisor = (profile['supervisor']
                           if profile['supervisor'] else 'None')
        self.from_date = profile['from_date']
        self.to_date = profile['to_date']
        self.bachelor = (profile['bachelor'] if profile['bachelor']
                         else {'school': '', 'major': '', 'rank': ''})
        self.master = (profile['master'] if profile['master']
                       else {'school': '', 'major': ''})
        self.doctor = (profile['doctor'] if profile['doctor']
                       else {'school': '', 'major': ''})
        self.awards = profile['awards'] if profile['awards'] else []
        self.publications = (profile['publications']
                             if profile['publications'] else [])
        self.google_scholar_page = profile['google_scholar_page']
        self.cv_url = profile['cv_url']
        self.homepage = profile['homepage']
        self.avatar_url = (profile['avatar_url'] if profile['avatar_url']
                           else '/static/img/avatar/default.png')

    def _db_insert(self, document):
        if not isinstance(document, Mapping):
            raise TypeError('document to be inserted must be a Mapping type')
        document['created_time'] = datetime.utcnow()
        document['updated_time'] = datetime.utcnow()
        db = get_db()
        db.members.insert_one(document)

    def _db_update(self, modification, target='one', upsert=False):
        if not isinstance(modification, dict):
            raise TypeError('modification must be a dict object')
        if '$set' not in modification:
            modification['$set'] = {}
        modification['$set']['updated_time'] = datetime.utcnow()
        db = get_db()
        if target == 'one':
            db.members.update_one({'uid': self.uid}, modification, upsert)
        elif target == 'many':
            db.members.update_many({'uid': self.uid}, modification, upsert)
        else:
            raise ValueError('update target must be either "one" or "many"')

    @classmethod
    def _db_find(cls, filter=None, target='many', **options):
        if filter is None:
            filter = {}
        if not isinstance(filter, dict):
            raise TypeError('filter must be a dict object')
        if 'uid' not in filter:
            filter['uid'] = {'$gte': 1000}
        db = get_db()
        if target == 'one':
            return db.members.find_one(filter, **options)
        elif target == 'many':
            return db.members.find(filter, **options)
        else:
            raise ValueError('find target must be either "one" or "many"')

    def create(self):
        self._db_insert(self.to_info())

    def to_info(self):
        member_info = {
            'uid': self.uid,
            'en_name': self.en_name,
            'zh_name': self.zh_name,
            'state': self.state,
            'position': self.position,
            'sex': self.sex,
            'birthdate': self.birthdate,
            'email': self.email,
            'supervisor': self.supervisor,
            'from_date': self.from_date,
            'to_date': self.to_date,
            'bachelor': self.bachelor,
            'master': self.master,
            'doctor': self.doctor,
            'awards': self.awards,
            'publications': self.publications,
            'google_scholar_page': self.google_scholar_page,
            'cv_url': self.cv_url,
            'homepage': self.homepage,
            'avatar_url': self.avatar_url,
        }
        return member_info

    def update(self, form):
        self.en_name = form['en_name']
        self.zh_name = form['zh_name']
        self.state = form['state']
        self.position = form['position']
        self.sex = form['sex']
        self.birthdate = form['birthdate']
        self.email = form['email']
        self.supervisor = form['supervisor']
        self.from_date = form['from_date']
        self.to_date = form['to_date']
        self.bachelor = {
            'school': form['bachelor_school'],
            'department': form['bachelor_department']
        }
        self.master = {
            'school': form['master_school'],
            'department': form['master_department']
        }
        self.doctor = {
            'school': form['phd_school'],
            'department': form['phd_department']
        }
        if not form['awards']:
            self.awards = []
        else:
            self.awards = form['awards'].split('\n')
        self.google_scholar_page = form['google_scholar_page']
        self.cv_url = form['cv_url']
        self.homepage = form['homepage']
        self._db_update({'$set': self.to_info()}, upsert=True)
        return True

    def change_avatar(self, img_file):
        avatar_url = '/static/img/avatar/{}.png'.format(self.uid)
        img_file.save('app' + avatar_url)
        self._db_update({'$set': {'avatar_url': avatar_url}})
        return avatar_url

    def add_publication(self, form):
        if 'bibtex' in form:
            bib_db = bibtexparser.loads(form['bibtex'])
            entries = bib_db.entries
        elif 'booktitle' in form or 'journal' in form:
            entries = {}
            for key in form:
                if form[key]:
                    entries[key] = form[key]
            entries['ID'] = (entries['author'].split(',')[0] + entries['year'] +
                             entries['title'].split(' ')[0]).lower()
            entries = [entries]
        self._db_update({'$push': {'publications': {'$each': entries}}})

    def del_publication(self, pub_id):
        self._db_update({'$pull': {'publications': {'ID': pub_id}}})

    def add_comment_to(self, uid, content):
        db = get_db()
        comment = {
            'uid': self.uid,
            'name': self.en_name,
            'avatar_url': self.avatar_url,
            'time': datetime.utcnow(),
            'content': content
        }
        db.comments.update_one(
            {'uid': uid}, {'$push': {'comments': comment}}, True)
        return comment
