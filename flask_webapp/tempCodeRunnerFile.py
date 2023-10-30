    def tearDown(self):
        with app.app_context():
            db.session.query(Role_Listing).filter(Role_Listing.listing_id == 0).delete()
            db.session.query(Staff).filter(Staff.staff_id == 171029).delete()
            db.session.query(Staff).filter(Staff.staff_id == 171014).delete()
            db.session.query(Role).filter(Role.role_name == "Finance Manager").delete()


            db.session.commit()