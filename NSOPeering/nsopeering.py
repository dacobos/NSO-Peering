import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py


app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'nsopeering.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/devices', methods=['GET'])
def devices():
    try:
        db = get_db()
        entries = db.execute('select * from devices').fetchall()
        return render_template('devices.html', entries = entries)
    except sqlite3.Error as e:
        error = "No se pudo realizar la consulta: "+e.args[0]
        return render_template('devices.html', error = error)

@app.route('/createDevice', methods=['POST'])
def createDevice ():
    try:
        db = get_db()
        db.execute('insert into devices (device, ipAddress) values (?,?)',[request.form['device'],request.form['ipAddress']])
        db.commit()
        flash('Device successfully created')
        return redirect(url_for('devices'))
    except sqlite3.Error as e:
        error = "No se pudo crear el registro: "+e.args[0]
        return render_template('devices.html', error = error)

@app.route('/updateDevice', methods=['POST'])
def updateDevice():
    try:
        db = get_db()
        db.execute('update devices set ipAddress = (?) where device = (?)',[request.form['newipAddress'],request.form['updateDevice']])
        db.commit()
        flash('Device successfully updated')
        return redirect(url_for('devices'))
    except sqlite3.Error as e:
        error = "No se pudo actualizar el registro: "+e.args[0]
        return render_template('devices.html', error = error)

@app.route('/deleteDevice', methods=['POST'])
def deleteDevice():
    try:
        db = get_db()
        db.execute('delete from devices where device = (?)',[request.form['deleteDevice']])
        db.commit()
        flash('Device successfully deleted')
        return redirect(url_for('devices'))
    except sqlite3.Error as e:
        error = "No se pudo borrar el registro: "+e.args[0]
        return render_template('devices.html', error = error)





@app.route('/prefixset', methods=['GET'])
def prefixset():
    try:
        db = get_db()
        entries = db.execute('select * from prefixsets').fetchall()
        devs = db.execute('select * from devices').fetchall()
        return render_template('prefixset.html', entries = entries, devs = devs)
    except sqlite3.Error as e:
        error = "No se pudo realizar la consulta: "+e.args[0]
        return render_template('prefixset.html', error = error)

@app.route('/createPrefixSet', methods=['POST'])
def createPrefixSet ():
    try:
        db = get_db()
        db.execute('insert into prefixsets (prefixset, device) values (?,?)',[request.form['prefixset'],request.form['device']])
        db.commit()
        flash('Prefix Set successfully created')
        return redirect(url_for('prefixset'))
    except sqlite3.Error as e:
        error = "No se pudo crear el registro: "+e.args[0]
        return render_template('prefixset.html', error = error)

@app.route('/updatePrefixSet', methods=['POST'])
def updatePrefixSet():
    try:
        db = get_db()
        db.execute('update prefixsets set device = (?) where prefixset = (?)',[request.form['device'],request.form['updatePrefixSet']])
        db.commit()
        flash('Prefix Set successfully updated')
        return redirect(url_for('prefixset'))
    except sqlite3.Error as e:
        error = "No se pudo actualizar el registro: "+e.args[0]
        return render_template('prefixset.html', error = error)

@app.route('/deletePrefixSet', methods=['POST'])
def deletePrefixSet():
    try:
        db = get_db()
        db.execute('delete from prefixsets where prefixset = (?)',[request.form['deletePrefixSet']])
        db.commit()
        flash('Prefix Set successfully deleted')
        return redirect(url_for('prefixset'))
    except sqlite3.Error as e:
        error = "No se pudo borrar el registro: "+e.args[0]
        return render_template('prefixset.html', error = error)


@app.route('/routepolicy', methods=['GET'])
def routepolicy():
    try:
        db = get_db()
        entries = db.execute('select * from routepolicys').fetchall()
        pref = db.execute('select * from prefixsets').fetchall()
        return render_template('routepolicy.html', entries = entries, pref = pref)
    except sqlite3.Error as e:
        error = "No se pudo realizar la consulta: "+e.args[0]
        return render_template('routepolicy.html', error = error)


@app.route('/createRoutePolicy', methods=['POST'])
def createRoutePolicy ():
    try:
        db = get_db()
        db.execute('insert into routepolicys (routepolicy, prefixset) values (?,?)',[request.form['routepolicy'],request.form['prefixset']])
        db.commit()
        flash('Route policy successfully created')
        return redirect(url_for('routepolicy'))
    except sqlite3.Error as e:
        error = "No se pudo crear el registro: "+e.args[0]
        return render_template('routepolicy.html', error = error)


@app.route('/updateRoutePolicy', methods=['POST'])
def updateRoutePolicy():
    try:
        db = get_db()
        db.execute('update routepolicys set prefixset = (?) where routepolicy = (?)',[request.form['prefixset'],request.form['updateRoutePolicy']])
        db.commit()
        flash('Route policy successfully updated')
        return redirect(url_for('routepolicy'))
    except sqlite3.Error as e:
        error = "No se pudo actualizar el registro: "+e.args[0]
        return render_template('routepolicy.html', error = error)

@app.route('/deleteRoutePolicy', methods=['POST'])
def deleteRoutePolicy():
    try:
        db = get_db()
        db.execute('delete from routepolicys where routepolicy = (?)',[request.form['deleteRoutePolicy']])
        db.commit()
        flash('Prefix Set successfully deleted')
        return redirect(url_for('routepolicy'))
    except sqlite3.Error as e:
        error = "No se pudo borrar el registro: "+e.args[0]
        return render_template('routepolicy.html', error = error)

@app.route('/prefix', methods=['GET'])
def prefix():
    try:
        db = get_db()
        entries = db.execute('select prefixes.prefId, prefixsets.device, prefixsets.prefixset, prefixes.prefix, prefixes.mask from prefixsets inner join prefixes on prefixsets.prefsetId = prefixes.prefsetId;').fetchall()
        pref = db.execute('select * from prefixsets').fetchall()
        return render_template('prefix.html', entries = entries, pref=pref)
    except sqlite3.Error as e:
        error = "No se pudo realizar la consulta: "+e.args[0]
        return render_template('routepolicy.html', error = error)

@app.route('/movePrefix', methods=['POST'])
def movePrefix():
    try:
        db = get_db()
        if request.form['param'] == 'Device':
            entries = db.execute('select prefixes.prefId, prefixsets.device, prefixsets.prefixset, prefixes.prefix, prefixes.mask from prefixsets inner join prefixes on prefixsets.prefsetId = prefixes.prefsetId where prefixsets.device = (?);',[request.form['paramValue']]).fetchall()
            pref = db.execute('select * from prefixsets').fetchall()
            return render_template('prefix.html', entries = entries, pref=pref)
        elif request.form['param'] == 'PrefixSet':
            entries = db.execute('select prefixes.prefId, prefixsets.device, prefixsets.prefixset, prefixes.prefix, prefixes.mask from prefixsets inner join prefixes on prefixsets.prefsetId = prefixes.prefsetId where prefixsets.prefixset = (?);',[request.form['paramValue']]).fetchall()
            pref = db.execute('select * from prefixsets').fetchall()
            return render_template('prefix.html', entries = entries, pref=pref)
        elif request.form['param'] == 'None':
            entries = db.execute('select prefixes.prefId, prefixsets.device, prefixsets.prefixset, prefixes.prefix, prefixes.mask from prefixsets inner join prefixes on prefixsets.prefsetId = prefixes.prefsetId;').fetchall()
            pref = db.execute('select * from prefixsets').fetchall()
            return render_template('prefix.html', entries = entries, pref=pref)
        else:
            entries = db.execute('select * from prefixes').fetchall()
            for row in entries:
                if request.form[str(row[0])] == 'True':
                    db.execute('update prefixes set prefsetId = (?) where prefId = (?)',[request.form['prefsetId'],str(row[0])])
                    db.commit()
            flash('Prefix successfully moved')
            return redirect(url_for('prefix'))
    except sqlite3.Error as e:
        error = "No se pudo actualizar el registro: "+e.args[0]
        return render_template('prefix.html', error = error)


@app.route('/moveDevice', methods=['POST'])
def moveDevice():
    try:
        db = get_db()
        entries = db.execute('select * from prefixes').fetchall()
        for row in entries:
            if request.form[str(row[0])] == 'True':
                db.execute('update prefixes set device = (?), prefixset = (?) where id = (?)',[request.form['device'],request.form['prefixset'],str(row[0])])
                db.commit()
        flash('Prefix successfully moved')
        return redirect(url_for('prefix'))
    except sqlite3.Error as e:
        error = "No se pudo actualizar el registro: "+e.args[0]
        return render_template('prefix.html', error = error)
