
@app.route('/all_listings_staff', methods=["GET", "POST"])
@login_required(allowed_roles=[1,2])
def all_listings_staff():
    Staff_ID = session.get('Staff_ID')
    Role = session.get('Role')