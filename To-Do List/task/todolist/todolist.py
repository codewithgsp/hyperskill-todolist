from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# constants
NUM_OF_DAYS_IN_WEEK = 7
NUM_TO_DAY_MAPPING = {0: 'Monday',
                      1: 'Tuesday',
                      2: 'Wednesday',
                      3: 'Thursday',
                      4: 'Friday',
                      5: 'Saturday',
                      6: 'Sunday'}

DeclarativeMeta = declarative_base()


class Task(DeclarativeMeta):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return '{id}. {task}'.format(id=self.id, task=self.task)

    def __str__(self):
        return '{id}. {task}. {deadline}'.format(id=self.id,
                                                 task=self.task,
                                                 deadline=self.deadline.strftime('%d %b'))


class ToDoList(Task):

    def define_engine(self, name):
        return create_engine('sqlite:///' + name + '?check_same_thread=False')

    def create_data_base(self, engine_):
        DeclarativeMeta.metadata.create_all(engine_)

    def create_session(self, engine_):
        Session = sessionmaker(bind=engine_)
        return Session()

    def query_all(self, session_, table):
        return session_.query(table).all()

    def query_filter(self, session_, table, date):
        return session_.query(table).filter(table.deadline == date).all()

    def query_filter_missed(self, session_, table, date):
        return session_.query(table).filter(table.deadline < date).order_by(table.deadline)

    def query_all_ordered(self, session_, table):
        return session_.query(table).order_by(table.deadline)

    def query_add_row(self, session_, new_row_):
        session_.add(new_row_)
        session_.commit()

    def query_delete_selected(self, session_, row_):
        session_.delete(row_)
        session_.commit()

    def display_action(self):
        return input("\n1) Today's tasks"
                     "\n2) Week's tasks"
                     "\n3) All tasks"
                     "\n4) Missed tasks"
                     "\n5) Add task"
                     "\n6) Delete task"
                     "\n0) Exit\n")

    def display_day_and_month(self, date):
        return date.strftime('%d %b')

    def display_today_date(self):
        return datetime.today()

    def convert_to_datetype(self, string):
        return datetime.strptime(string, '%Y-%m-%d')


if __name__ == '__main__':
    todo = ToDoList()
    engine = todo.define_engine('todo.db')
    todo.create_data_base(engine)
    session = todo.create_session(engine)
    action = ''
    while action != '0':
        action = todo.display_action()
        if action == '1':
            today = todo.display_today_date()
            print('Today {}:'.format(todo.display_day_and_month(today)))
            rows = todo.query_filter(session_=session, table=Task, date=today)
            if not rows:
                print('Nothing to do!')
            else:
                for row in rows:
                    print(repr(row))
        elif action == '2':
            for day in range(NUM_OF_DAYS_IN_WEEK):
                new_date = todo.display_today_date().date() + timedelta(days=day)
                print(NUM_TO_DAY_MAPPING.get(new_date.weekday()), new_date.day, new_date.strftime('%b') + ':')
                rows = todo.query_filter(session_=session, table=Task, date=new_date)
                if not rows:
                    print('Nothing to do!')
                else:
                    count = 0
                    for row in rows:
                        count += 1
                        print('{}. {}'.format(count, row.task))
                print()
        elif action == '3':
            print('All tasks:')
            rows = todo.query_all(session_=session, table=Task)
            if not rows:
                print('Nothing to do!')
            else:
                for row in rows:
                    print(row)
        elif action == '4':
            print('Missed tasks:')
            rows = todo.query_filter_missed(session_=session, table=Task, date=todo.display_today_date().date())
            if not rows:
                print('Nothing is missed!')
            else:
                count = 0
                for row in rows:
                    count += 1
                    print('{}. {}. {} {}.'.format(count, row.task, row.deadline.day, row.deadline.strftime('%b')))
        elif action == '5':
            task_input = input('Enter task')
            deadline_input = input('Enter deadline')
            deadline_date_type = todo.convert_to_datetype(deadline_input)
            new_row = Task(task=task_input, deadline=deadline_date_type)
            todo.query_add_row(session_=session, new_row_=new_row)
            print('The task has been added!')
        elif action == '6':
            rows = todo.query_all_ordered(session_=session, table=Task)
            if not rows:
                print('Nothing to delete')
            else:
                print('Chose the number of the task you want to delete:')
                count = 0
                for row in rows:
                    count += 1
                    print('{}. {}. {} {}.'.format(count, row.task, row.deadline.day, row.deadline.strftime('%b')))
                chose_input = input()
                todo.query_delete_selected(session_=session, row_=rows[int(chose_input) - 1])
                print('The task has been deleted!')
    else:
        print('\nBye!')
