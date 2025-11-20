from app import create_app, db
from app.models import Activity

app = create_app()

with app.app_context():
    db.create_all()
    if not Activity.query.first():
        Hiking = Activity(
            name= 'Hiking Killington',
            size='small',
            distance_from_origin=5.2,
            cost=0.0,
            category='hiking'
        )
        db.session.add(Hiking)
        db.session.commit()
        print('Created activity')
    else:
        print('Activities already exist')
