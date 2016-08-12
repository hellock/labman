from datetime import datetime

import bibtexparser

from app.db import get_db


class Member(object):

    @classmethod
    def get_member_by_uid(cls, uid):
        db = get_db()
        info = db.members.find_one({'uid': uid})
        return Member(info)

    @classmethod
    def form2info(cls, form):
        awards = form['awards'].split('\n')
        if not awards:
            awards = []
        member_info = {
            'updated_time': datetime.utcnow(),
            'en_name': form['en_name'],
            'zh_name': form['zh_name'],
            'position': form['position'],
            'sex': form['sex'],
            'birthdate': form['birthdate'],
            'supervisor': form['supervisor'],
            'from_date': form['from_date'],
            'to_date': form['to_date'],
            'bachelor': {
                'school': form['bachelor_school'],
                'department': form['bachelor_department']
            },
            'master': {
                'school': form['master_school'],
                'department': form['master_department']
            },
            'doctor': {
                'school': form['phd_school'],
                'department': form['phd_department']
            },
            'awards': awards,
            'google_scholar_page': form['google_scholar_page'],
        }
        return member_info

    def __init__(self, info=None):
        self.uid = info['uid'] if info else 0
        self.en_name = info['en_name'] if info else ''
        self.zh_name = info['zh_name'] if info else ''
        self.position = info['position'] if info else None
        self.sex = info['sex'] if info else None
        self.from_date = info['from_date'] if info else None
        self.to_date = info['to_date'] if info else None
        self.supervisor = info['supervisor'] if info else ''
        self.bachelor = info['bachelor'] if info else {'school': '', 'major': ''}
        self.master = info['master'] if info else {'school': '', 'major': ''}
        self.doctor = info['doctor'] if info else {'school': '', 'major': ''}
        self.awards = info['awards'] if info else []
        self.publications = info['publications'] if info else []
        self.google_scholar_page = info['google_scholar_page'] if info else ''
        self.avatar_url = info['avatar_url'] if info else '/static/img/avatar/default.png'

    def update(self, form):
        member_info = self.form2info(form)
        db = get_db()
        db.members.update_one({'uid': self.uid}, {'$set': member_info})
        return True

    def add_publication(self, bibtex):
        bib_db = bibtexparser.loads(bibtex)
        db = get_db()
        db.members.update_one(
            {'uid': self.uid},
            {'$push': {'publications': {'$each': bib_db.entries}}}
        )

    def del_publication(self, pub_id):
        db = get_db()
        db.members.update_one(
            {'uid': self.uid},
            {'$pull': {'publications': {'ID': pub_id}}}
        )
