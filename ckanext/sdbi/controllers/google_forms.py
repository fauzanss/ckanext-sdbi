from flask import Blueprint, render_template, request, abort
import ckan.model as model
import logging
import ckan.authz as authz
import ckan.lib.base as base

# Create Flask Blueprint
google_forms_blueprint = Blueprint('google_forms', __name__)

# Debug logging for blueprint creation
log = logging.getLogger(__name__)
log.info("Google Forms blueprint created")

def _check_admin():
    """Check if current user is admin"""
    c = base.c
    if not authz.is_sysadmin(c.user):
        abort(403, description='Access denied. Admin privileges required.')

@google_forms_blueprint.route('/google-forms')
def index():
    """Halaman utama Google Forms"""
    _check_admin()
    try:
        # Get all forms from database
        forms = _get_all_forms()
        return render_template('google_forms/index.html', forms=forms)
    except Exception as e:
        log.error(f"Google Forms index error: {str(e)}")
        abort(500, description='Internal server error')

@google_forms_blueprint.route('/google-forms/create', methods=['GET', 'POST'])
def create():
    """Halaman create Google Form"""
    _check_admin()
    if request.method == 'POST':
        return _save_form()
    return render_template('google_forms/create.html')

@google_forms_blueprint.route('/google-forms/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    """Halaman edit Google Form"""
    _check_admin()
    if request.method == 'POST':
        return _update_form(id)
    
    form = _get_form_by_id(id)
    if not form:
        abort(404, description='Form not found')
    
    return render_template('google_forms/edit.html', form=form)

@google_forms_blueprint.route('/google-forms/view/<id>')
def view(id):
    """Halaman view Google Form"""
    _check_admin()
    form = _get_form_by_id(id)
    if not form:
        abort(404, description='Form not found')
    
    return render_template('google_forms/view.html', form=form)

@google_forms_blueprint.route('/google-forms/delete/<id>', methods=['DELETE'])
def delete(id):
    """Delete Google Form"""
    _check_admin()
    try:
        form = _get_form_by_id(id)
        if not form:
            return {'error': 'Form not found'}, 404
        
        # Delete from database
        from sqlalchemy import text
        model.Session.execute(text("""
            DELETE FROM google_forms WHERE id = :id
        """), {'id': id})
        model.Session.commit()
        
        return {'success': True, 'message': 'Form deleted'}
        
    except Exception as e:
        log.error(f"Delete form error: {str(e)}")
        return {'error': str(e)}, 500

@google_forms_blueprint.route('/api/google-forms/exit-intent')
def get_exit_intent_forms():
    """Get Google Forms with exit intent enabled"""
    try:
        from sqlalchemy import text
        result = model.Session.execute(text("""
            SELECT id, title, description, form_url, category, status, exit_intent, created_at
            FROM google_forms 
            WHERE exit_intent = true AND status = 'active'
            ORDER BY created_at DESC
        """))
        
        forms = []
        for row in result:
            forms.append({
                'id': str(row[0]),
                'title': row[1],
                'description': row[2],
                'form_url': row[3],
                'category': row[4],
                'status': row[5],
                'exit_intent': row[6],
                'created_at': str(row[7])
            })
        
        return {'success': True, 'forms': forms}
        
    except Exception as e:
        log.error(f"Get exit intent forms error: {str(e)}")
        return {'success': False, 'error': str(e)}, 500

def _save_form():
    """Save new Google Form to database"""
    try:
        title = request.form.get('title', '')
        description = request.form.get('description', '')
        form_url = request.form.get('form_url', '')
        category = request.form.get('category', 'general')
        status = request.form.get('status', 'active')
        exit_intent = request.form.get('exit_intent') == 'on'
        
        if not title or not form_url:
            abort(400, description='Title and Form URL are required')
        
        # Insert into database
        from sqlalchemy import text
        from datetime import datetime
        result = model.Session.execute(text("""
            INSERT INTO google_forms (title, description, form_url, category, status, exit_intent, created_at)
            VALUES (:title, :description, :form_url, :category, :status, :exit_intent, :created_at)
            RETURNING id
        """), {
            'title': title,
            'description': description,
            'form_url': form_url,
            'category': category,
            'status': status,
            'exit_intent': exit_intent,
            'created_at': datetime.utcnow()
        })
        
        form_id = result.fetchone()[0]
        model.Session.commit()
        
        # Redirect to form view
        from flask import redirect, url_for
        return redirect(f'/google-forms/view/{form_id}')
        
    except Exception as e:
        log.error(f"Save form error: {str(e)}")
        abort(500, description='Internal server error')

def _update_form(id):
    """Update existing Google Form"""
    try:
        title = request.form.get('title', '')
        description = request.form.get('description', '')
        form_url = request.form.get('form_url', '')
        category = request.form.get('category', 'general')
        status = request.form.get('status', 'active')
        exit_intent = request.form.get('exit_intent') == 'on'
        
        if not title or not form_url:
            abort(400, description='Title and Form URL are required')
        
        # Update database
        from sqlalchemy import text
        model.Session.execute(text("""
            UPDATE google_forms 
            SET title = :title, description = :description, form_url = :form_url, 
                category = :category, status = :status, exit_intent = :exit_intent
            WHERE id = :id
        """), {
            'id': id,
            'title': title,
            'description': description,
            'form_url': form_url,
            'category': category,
            'status': status,
            'exit_intent': exit_intent
        })
        
        model.Session.commit()
        
        # Redirect to form view
        from flask import redirect
        return redirect(f'/google-forms/view/{id}')
        
    except Exception as e:
        log.error(f"Update form error: {str(e)}")
        abort(500, description='Internal server error')

def _get_all_forms():
    """Get all Google Forms from database"""
    try:
        from sqlalchemy import text
        result = model.Session.execute(text("""
            SELECT id, title, description, form_url, category, status, exit_intent, created_at
            FROM google_forms 
            ORDER BY created_at DESC
        """))
        
        forms = []
        for row in result:
            forms.append({
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'form_url': row[3],
                'category': row[4],
                'status': row[5],
                'exit_intent': row[6],
                'created_at': row[7]
            })
        
        return forms
        
    except Exception as e:
        log.error(f"Get forms error: {str(e)}")
        return []

def _get_form_by_id(id):
    """Get Google Form by ID"""
    try:
        from sqlalchemy import text
        result = model.Session.execute(text("""
            SELECT id, title, description, form_url, category, status, exit_intent, created_at
            FROM google_forms 
            WHERE id = :id
        """), {'id': id})
        
        row = result.fetchone()
        if row:
            return {
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'form_url': row[3],
                'category': row[4],
                'status': row[5],
                'exit_intent': row[6],
                'created_at': row[7]
            }
        
        return None
        
    except Exception as e:
        log.error(f"Get form by ID error: {str(e)}")
        return None 