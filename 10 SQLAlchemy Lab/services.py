from models import User, Order
from main import Session

session = Session()


def create_user(session: Session, username: str, email: str) -> None:
    with session as session:
        user = User(username=username, email=email)
        session.add(user)
        session.commit()


def get_users(session: Session) -> None:
    with session as s:
        users = s.query(User).all()

        for user in users:
            print(user.username, user.email)


def update_email(session: Session, username: str, new_email: str) -> None:
    with session as s:
        user = s.query(User).filter_by(username=username).first()

        if user:
            user.email = new_email
            s.commit()
            print('User updated successfully.')
        else:
            print('User not found.')


def delete_user(session: Session, username: str) -> None:
    with session as s:
        user = s.query(User).filter_by(username=username).first()

        if user:
            s.delete(user)
            s.commit()
            print(f'{username} was deleted successfully.')
        else:
            print('User not found.')


def bulk_create_users(session: Session, users: list) -> None:
    users = [User(**u) for u in users]

    with session as s:
        s.add_all(users)
        s.commit()
        print('Users created.')


def bulk_delete_users(session: Session) -> None:
    try:
        session.begin()
        session.query(User).delete()
        session.commit()
        print('All users deleted.')
    except Exception as e:
        session.rollback()
        print('An error occurred:', str(e))
    finally:
        session.close()


def bulk_create_orders(session: Session, orders: list):
    with session as s:
        s.add_all(orders)
        s.commit()
        print('Orders added.')


def get_orders_info(session: Session):
    with session as s:
        orders = s.query(Order).order_by(Order.user_id.desc()).all()

        if not orders:
            print('No orders yet.')
        else:
            for order in orders:
                print(f'Order number {order.id}, Is completed: {order.is_completed}, Username: {order.user.username}')


users_data = [
    {'username': 'john_doe', 'email': 'john.doe @ example.com'},
    {'username': 'sarah_smith', 'email': 'sarah.smith@gmail.com'},
    {'username': 'mike_jones', 'email': 'mike.jones @ company.com'},
    {'username': 'emma_wilson', 'email': 'emma.wilson @ domain.net'},
    {'username': 'david_brown', 'email': 'david.brown @ email.org'},
]
