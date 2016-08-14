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
            'email': form['email'],
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
            'cv_url': form['cv_url'],
            'homepage': form['homepage']
        }
        return member_info

    @classmethod
    def list_supervisors(cls):
        supervisors = []
        db = get_db()
        for info in db.members.find({'uid': {'$gte': 1000}, 'position': 'Professor'}):
            supervisors.append(Member(info))
        supervisors.sort(
            key=lambda x: ''.join(reversed(x.from_date.split('/'))))
        return supervisors

    def __init__(self, info=None):
        self.uid = info['uid'] if info else 0
        self.en_name = info['en_name'] if info else ''
        self.zh_name = info['zh_name'] if info else ''
        self.position = info['position'] if info else None
        self.sex = info['sex'] if info else None
        self.birthdate = info['birthdate'] if info else None
        self.email = info['email'] if info else ''
        self.supervisor = info['supervisor'] if info else ''
        self.from_date = info['from_date'] if info else ''
        self.to_date = info['to_date'] if info else ''
        self.bachelor = info['bachelor'] if info else {'school': '', 'major': ''}
        self.master = info['master'] if info else {'school': '', 'major': ''}
        self.doctor = info['doctor'] if info else {'school': '', 'major': ''}
        self.awards = info['awards'] if info else []
        self.publications = info['publications'] if info else []
        self.google_scholar_page = info['google_scholar_page'] if info else ''
        self.cv_url = info['cv_url'] if info else ''
        self.homepage = info['homepage'] if info else ''
        self.avatar_url = info['avatar_url'] if info else '/static/img/avatar/default.png'

    def to_info(self):
        member_info = {
            'en_name': self.en_name,
            'zh_name': self.zh_name,
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
            'google_scholar_page': self.google_scholar_page,
            'cv_url': self.cv_url,
            'homepage': self.homepage,
            'avatar_url': self.avatar_url
        }
        return member_info

    def update(self, form):
        member_info = self.form2info(form)
        db = get_db()
        db.members.update_one({'uid': self.uid}, {'$set': member_info})
        return True

    def change_avatar(self, img_file):
        avatar_url = '/static/img/avatar/{}.png'.format(self.uid)
        img_file.save('app' + avatar_url)
        db = get_db()
        db.members.update_one({'uid': self.uid}, {'$set': {'avatar_url': avatar_url}})
        return avatar_url

    def add_publication(self, form):
        db = get_db()
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
        db.members.update_one(
            {'uid': self.uid},
            {'$push': {'publications': {'$each': entries}}}
        )

    def del_publication(self, pub_id):
        db = get_db()
        db.members.update_one(
            {'uid': self.uid},
            {'$pull': {'publications': {'ID': pub_id}}}
        )
