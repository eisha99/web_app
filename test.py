# taken from
# https://stackoverflow.com/questions/20621321/how-to-write-tests-in-python-using-unittest
import os
from app import db
import app
import unittest
import tempfile
from app.db_models import User, Task
from werkzeug.exceptions import HTTPException
# mainly targets routing page

# the class on unit tests was after this assignment was supposed to be submitted, so I do not use coverage here for the sake of time
class KanbanTest(unittest.TestCase):


    def setUp(self):
        """Creates a new test client and initializes a new database"""
        # setup and teardown from documentation
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.testing = True
        self.app = app.app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        """Closes the test database"""
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    ##

    def test_home_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    ##

    def signup(self, username, password):
        """Send request to sign up page"""
        return self.app.post('/signup', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def test_signup_get(self):
        """Test sign up"""
        response = self.app.get('/signup', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_signup_post(self):
        """Test sign up"""
        response = self.signup('admin', '12345678')
        assert b' Kanban board ' in response.data
        user = db.session.query(User).filter(User.username=='admin').first()
        self.assertEqual(user.password, '12345678')
        

    def test_signup_post_duplicate(self):
        """Test if duplicated username is not excepted"""
        self.signup('admin1', '1234567')
        user = db.session.query(User).filter(User.username=='admin1').first()
        self.assertEqual(user.password, '1234567')
        response = self.signup('admin1', '123456')
        assert b'Please, choose a different username. This one is already taken' in response.data
    
    ##

    def login(self, username, password):
        """Send request to login page"""
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def test_login_get(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_login_page_noerror(self):
        self.signup('admin', '12345678')
        response = self.login('admin', '12345678')
        self.assertEqual(response.status_code, 200)

    def test_login_page_invalid_username(self):
        # invalid pass
        response = self.login('non_existant', '12345678')
        assert b'Invalid username!' in response.data

    def test_login_page_invalid_password(self):
        # invalid pass
        self.signup('admin', '12345678')
        response = self.login('admin', 'wrong')
        assert b'Incorrect password!' in response.data

    ##

    def test_logout(self):
        self.signup('admin', '12345678')
        self.login('admin', '12345678')
        response = self.app.get('/logout', follow_redirects=True)
        # redirects to welcome page
        assert b'Welcome to Canban Board!' in response.data
    ##

    def add(self, title):
        """
            Send request to add new task
        """
        return self.app.post('/add', data=dict(
            task=title
        ), follow_redirects=True)

    def test_form_add(self):
        """
            Test adding a task to the board. 
        """
        response = self.signup('admin', '1234567')
        self.assertEqual(response.status_code, 200)

        response = self.login('admin', '1234567')
        self.assertEqual(response.status_code, 200)

        self.add('test')
        task = db.session.query(Task).filter(Task.title=='test').first()
        self.assertEqual(task.title, 'test')
        assert task.status == 'to_do'

    ## 

    def change_status(self, id, status):
        """
            Send request to change status of task
        """
        print('/update/task/{}/{}'.format(str(id), str(status)))

        return self.app.get('/update/task/{}/{}'.format(str(id), str(status)), data=dict(
            id=id,
            status=status
        ), follow_redirects=True)

    def delete_task(self, id):
        """
            Send request to delete task
        """
        print('/delete/task/{}'.format(str(id)))

        return self.app.get('/delete/task/{}'.format(str(id)), data=dict(
            id=id
        ), follow_redirects=True)

    def test_change_status(self):

        """
            Test the change of status (and deletion) of a task
        """

        response = self.signup('admin', '12345678')
        assert b' Kanban board ' in response.data
        self.login('admin', '12345678')
        
        self.add('test')
        task = db.session.query(Task).filter(Task.title=='test').first()
        self.assertEqual(task.title, 'test')
        assert task.status == 'to_do'
        
        self.change_status(task.id, 'doing')
        task = db.session.query(Task).filter(Task.title=='test').first()
        print(task, task.status)
        assert task.status =='doing'
        
        self.change_status(task.id, 'done')
        task = db.session.query(Task).filter(Task.title=='test').first()
        assert task.status == 'done'
        
        self.change_status(task.id, 'to_do')
        task = db.session.query(Task).filter(Task.title=='test').first()
        assert task.status == 'to_do'
        
        self.delete_task(task.id)
        task = db.session.query(Task).filter(Task.id==task.id).first()
        assert task is None

    def test_loginin_user_exceptions(self):
        """ 
            test exceptions in change_status function from routing.py (non logged in user)
        """
        # logged in
        response = self.add('test')
        assert b'401' in response.data
        response = self.change_status(1, 'doing')       
        assert b'401' in response.data
        response = self.delete_task(1)        
        assert b'401' in response.data

    def test_validate_task(self):
        """
            Test status code when trying to move or delete non-existent task
        """
        # signed up and logged in 
        response = self.signup('admin', '12345678')
        assert b' Kanban board ' in response.data
        
        response = self.change_status(0, 'doing')        
        assert b'404' in response.data
        response = self.delete_task(0)        
        assert b'404' in response.data


if __name__ == '__main__':
    unittest.main()