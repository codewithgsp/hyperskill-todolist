from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DeclarativeMeta = declarative_base()


class Task(DeclarativeMeta):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return '{id}. {task}'.format(id=self.id, task=self.task)


class ToDoList(Task):

    def define_engine(self, name):
        return create_engine('sqlite:///' + name + '?check_same_thread=False')

    def create_data_base(self, engine):
        DeclarativeMeta.metadata.create_all(engine)

    def create_session(self, engine):
        Session = sessionmaker(bind=engine)
        return Session()

    def query_all(self, session, table):
        return session.query(table).all()

    def query_add_row(self, session, new_row):
        session.add(new_row)
        session.commit()

    def display_action(self):
        return input("1) Today's tasks\n2) Add task\n0) Exit")


if __name__ == '__main__':
    todo = ToDoList()
    engine = todo.define_engine('todo.db')
    todo.create_data_base(engine)
    session = todo.create_session(engine)
    action = ''
    while action != '0':
        action = todo.display_action()
        if action == '1':
            print('Today:')
            rows = todo.query_all(session=session, table=Task)
            if not rows:
                print('Nothing to do!')
            else:
                for row in rows:
                    print(row)
        elif action == '2':
            task_input = input('Enter task')
            new_row = Task(task=task_input)
            todo.query_add_row(session=session, new_row=new_row)
            print('The task has been added!')
    else:
        print('Bye!')
