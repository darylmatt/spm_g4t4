from functools import wraps
from flask import g, redirect, url_for, session

def login_required(allowed_roles=None):
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            if 'Staff_ID' not in session:
                return redirect(url_for('login'))
            
            if allowed_roles is None:
                return func(*args, **kwargs)
            
            user_role = session.get('Role')
            if user_role in allowed_roles:
 
                return func(*args, **kwargs)
            else:
                return redirect(url_for('unauthorised'))
        return wrapped_function
    return decorator


