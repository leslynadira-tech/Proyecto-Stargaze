from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.observation import Observation

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para acceder a esta página.")
        return redirect('/') 
    
    observations = Observation.get_all(session['user_id'])
    return render_template('dashboard.html', observations=observations)

@app.route('/create_observation', methods=['POST'])
def create_observation():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para acceder a esta página.")
        return redirect('/')
    if not Observation.validate_observation(request.form):
        return redirect('/dashboard')
        
    data = {
        "name": request.form['name'],
        "location": request.form['location'],
        "date": request.form['date'],
        "description": request.form['description'],
        "user_id": session['user_id']
    }
    Observation.save(data)
    return redirect('/dashboard')

@app.route('/editar/<int:id>')
def edit_observation(id):
    if 'user_id' not in session:
        flash("Debes iniciar sesión para acceder a esta página.")
        return redirect('/')
    obs = Observation.get_by_id({"id": id})
    if not obs:
        flash("Observación no encontrada.")
        return redirect('/dashboard')
    # Bonus: Proteger edición por URL
    if obs.user_id != session['user_id']:
        flash("No tienes permiso para editar esta publicación.", "obs")
        return redirect('/dashboard')
        
    return render_template('edit.html', obs=obs)

@app.route('/update_observation/<int:id>', methods=['POST'])
def update_observation(id):
    if 'user_id' not in session:
        flash("Debes iniciar sesión para acceder a esta página.")
        return redirect('/')
        
    obs = Observation.get_by_id({"id": id})
    if not obs or obs.user_id != session['user_id']:
        flash("Observación no encontrada.")
        return redirect('/dashboard')
        
    if not Observation.validate_observation(request.form, is_edit=True, current_id=id):
        return redirect(f'/editar/{id}')
        
    data = {
        "id": id,
        "name": request.form['name'],
        "location": request.form['location'],
        "date": request.form['date'],
        "description": request.form['description']
    }
    Observation.update(data)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete_observation(id):
    if 'user_id' not in session:
        flash("Debes iniciar sesión para acceder a esta página.")
        return redirect('/')
    obs = Observation.get_by_id({"id": id})
    if obs and obs.user_id == session['user_id']:
        Observation.delete({"id": id})
    return redirect('/dashboard')

@app.route('/like/<int:id>')
def like_observation(id):
    if 'user_id' not in session:
        flash("Debes iniciar sesión para acceder a esta página.")
        return redirect('/')
    data = {
        "user_id": session['user_id'],
        "observation_id": id
    }
    Observation.add_like(data)
    return redirect('/dashboard')
