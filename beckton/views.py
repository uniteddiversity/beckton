from flask import request, redirect, render_template, url_for, session, flash
from mongoengine import NotUniqueError
import gocardless_pro
import uuid
from beckton import app
import forms
import models
import tasks

@app.route("/", methods=['GET', 'POST'])
def condition():

    commitment_count = models.Commitment.objects.count()
    commitment_percent = int(float(commitment_count) / float(app.config['BECKTON_TARGET']) * 100)
    form = forms.Commitment()
    duplicate = False

    #If target met, display a different page
    if commitment_percent >= 100:
        return render_template('target_met.html')

    if request.method == 'GET':
        #clear session
        session['gocardless_session_token'] = str(uuid.uuid4())
        session.pop('commitment', None)

    if request.method == 'POST' and form.validate():
        session['commitment'] = {'name': form.data['name'], 'mobile_number': form.data['mobile_number'], 'rate': int(form.data['rate'])}

        #check if exists
        if not models.Commitment.objects(mobile_number=session['commitment']['mobile_number']):
            return redirect(url_for('direct_debit'))
        else:
            flash('Someone has already signed up with that phone number', 'error')

    return render_template('condition.html', commitment_count=commitment_count, commitment_percent=commitment_percent, form=form, duplicate=duplicate)

@app.route("/direct-debit", methods=['GET', 'POST'])
def direct_debit():

    if not session.get('commitment', False):
        return redirect(url_for('condition'))

    if request.method == 'POST':
        client = gocardless_pro.Client(access_token=app.config['GOCARDLESS_ACCESS_TOKEN'], environment=app.config['GOCARDLESS_ENVIRONMENT'])
        flow = client.redirect_flows.create(params={'scheme':'bacs','session_token': session['gocardless_session_token'], 'description': 'No payments will be taken unless the target is reached', 'success_redirect_url': url_for('direct_debit_callback', _external=True)})
        return redirect(flow.redirect_url)
    return render_template('direct-debit.html')

@app.route("/direct-debit-callback", methods=['GET', 'POST'])
def direct_debit_callback():

    if not session.get('commitment', False):
        return redirect(url_for('condition'))

    try:
        #save the commitment (double check not a duplicate)
        commitment = models.Commitment()
        commitment.name = session['commitment']['name']
        commitment.mobile_number = session['commitment']['mobile_number']
        commitment.rate = session['commitment']['rate']
        commitment = commitment.save()

        #complete the direct debit mandate
        client = gocardless_pro.Client(access_token=app.config['GOCARDLESS_ACCESS_TOKEN'], environment=app.config['GOCARDLESS_ENVIRONMENT'])
        redirect_flow_id = request.args.get('redirect_flow_id')
        redirect_flow = client.redirect_flows.complete(redirect_flow_id, params={'session_token': session['gocardless_session_token']})

        #save the mandate
        commitment.gocardless_mandate_id = redirect_flow.links.mandate
        commitment.save()

    except NotUniqueError:
        flash('Someone has already signed up with that phone number', 'error')
        return redirect(url_for('condition'))
    except gocardless_pro.errors.GoCardlessProError:
        flash('Sorry, something went wrong, the direct debit mandate has not been created', 'error')
        commitment.delete()
        return redirect(url_for('condition'))
        

    #clear session
    session.pop('gocardless_session_token', None)
    session.pop('commitment', None)

    #off to the final page
    return redirect(url_for('committed'))

@app.route("/committed")
def committed():

    commitment_count = models.Commitment.objects.count()
    commitment_percent = int(float(commitment_count) / float(app.config['BECKTON_TARGET']) * 100)
    return render_template('committed.html', commitment_count=commitment_count, commitment_percent=commitment_percent)

