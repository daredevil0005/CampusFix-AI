import os
import tempfile
import unittest
from werkzeug.security import generate_password_hash

import app as campus


class CampusFixTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        campus.DB_PATH = os.path.join(self.tmp.name, 'test.sqlite')
        campus.init_db()
        campus.app.config.update(TESTING=True, SECRET_KEY='test-secret')
        self.client = campus.app.test_client()

    def tearDown(self): self.tmp.cleanup()

    def token(self):
        response = self.client.get('/')
        with self.client.session_transaction() as sess: return sess['csrf']

    def test_priority_rules(self):
        self.assertEqual(campus.priority_for('Smoke in the hallway')[0], 'Urgent')
        self.assertEqual(campus.priority_for('Water leaking by library')[0], 'High')
        self.assertEqual(campus.priority_for('Broken bench')[0], 'Normal')

    def test_validation_and_manual_ticket_creation(self):
        token=self.token()
        bad=self.client.post('/report',data={'csrf_token':token,'complaint':'short','location':'Library'})
        self.assertEqual(bad.status_code,302)
        good=self.client.post('/report',data={'csrf_token':token,'complaint':'Water leaking near the library washroom.','location':'Library, ground floor','category':'Plumbing'})
        self.assertEqual(good.status_code,200)
        self.assertIn(b'CF-',good.data)
        self.assertIn(b'High',good.data)
        with campus.db() as con: self.assertEqual(con.execute('SELECT COUNT(*) FROM tickets').fetchone()[0],1)

    def test_tracking_does_not_show_assignee(self):
        with campus.db() as con:
            con.execute('INSERT INTO tickets VALUES (?,?,?,?,?,?,?,?,?,?)',('CF-ABC12345','Sink issue','Sink is clogged','Hall A','Plumbing','Normal','Routine','Submitted','Private Staff','2026-10-23'))
        response=self.client.get('/ticket/CF-ABC12345')
        self.assertEqual(response.status_code,200)
        self.assertNotIn(b'Private Staff',response.data)

    def test_admin_protection_and_validated_update(self):
        self.assertEqual(self.client.get('/admin').status_code,401)
        with campus.app.app_context(): pass
        os.environ['ADMIN_PASSWORD_HASH']=generate_password_hash('strong-test-password')
        token=self.token()
        self.client.post('/admin/login',data={'csrf_token':token,'password':'strong-test-password'})
        with campus.db() as con:
            con.execute('INSERT INTO tickets VALUES (?,?,?,?,?,?,?,?,?,?)',('CF-ABC12345','Sink issue','Sink is clogged','Hall A','Plumbing','Normal','Routine','Submitted','','2026-10-23'))
        csrf=self.token()
        res=self.client.post('/admin/ticket/CF-ABC12345',data={'csrf_token':csrf,'status':'Resolved','assignee':'Facilities'})
        self.assertEqual(res.status_code,302)
        with campus.db() as con: self.assertEqual(con.execute('SELECT status FROM tickets').fetchone()[0],'Resolved')
        invalid=self.client.post('/admin/ticket/CF-ABC12345',data={'csrf_token':csrf,'status':'Magic','assignee':''})
        self.assertEqual(invalid.status_code,400)
        os.environ.pop('ADMIN_PASSWORD_HASH',None)


if __name__ == '__main__': unittest.main()
