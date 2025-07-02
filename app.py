from flask import Flask,jsonify,request
from models import User,Plan,Subscription,db
from flask_login import logout_user,login_required,LoginManager,login_user
from dateutil import parser
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///subscription.db'
app.config['SECRET_KEY'] = ''
db.init_app(app)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/register',methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({'message':'Please fill in all forms'}),404

        user = User(email=email,password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message':'You have successfully registered! please try to login now'}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500


@app.route('/login',methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({'message':'Please fill in all forms'}),404

        user = User.query.filter_by(email=email,password=password).first()
        if user.password == password:
            login_user(user)
            return jsonify({'message':'You have successfully login'}),200
        return jsonify({'message':'Error logging in.. Please try again.'}),404
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@app.route('/logout',methods=['GET'])
def logout():
    try:
        logout_user()
        return jsonify({'message':'You have successfully logged out'})
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@app.route('/plan',methods=['POST'])
@login_required
def plan():
    try:
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        billing_cycle = data.get('billing_cycle')
        api_call_limit = data.get('api_call_limit')
        storage_limit_mb = data.get('storage_limit_mb')
        if not name or not price or not billing_cycle or not api_call_limit or not storage_limit_mb:
            return jsonify({'message':'please fill in all forms'}),404

        plan = Plan(name=name,price=price,billing_cycle=billing_cycle,api_call_limit=api_call_limit,storage_limit_mb=storage_limit_mb)
        db.session.add(plan)
        db.session.commit()
        return jsonify({'message':'your plan has been bought'}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@app.route('/buy_plan/<int:plan_id>',methods=['POST'])
@login_required
def buy_plan(plan_id):
    try:
        plan = Plan.query.get_or_404(plan_id)

        if plan.is_available:
            amount = int(input('How much plan do you want? '))
            if amount:
                db.session.commit()
                return jsonify({'message':'Your plan has been booked'}),200
            else:
                return jsonify({'message':'Input a plan'}),404
        else:
            return jsonify({'message':'No id with this plan.. Please try again'}),404
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@app.route('/get_plan',methods=['GET'])
@login_required
def get_plan():
    try:
        plan_all = Plan.query.all()

        plans = [
            {
                'name':plan.name,
                'price':plan.price,
                'is_available':plan.is_available,
                'billing_cycle':plan.billing_cycle,
                'api_call_limit':plan.api_call_limit,
                'storage_limit_mb':plan.storage_limit_mb
            }
            for plan in plan_all
        ]
        return jsonify({'plan':plans}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@app.route('/single_plan/<int:plan_id>',methods=['GET'])
@login_required
def single_plan(plan_id):
    try:
        plan = Plan.query.get_or_404(plan_id)

        plans_data = {
            'name': plan.name,
            'price':plan.price,
            'is_available':plan.is_available,
            'billing_cycle':plan.billing_cycle,
            'api_call_limit':plan.api_call_limit,
            'storage_limit_mb':plan.storage_limit_mb
        }
        return jsonify({'plan':plans_data}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500


@app.route('/delete_plan/<int:plan_id>',methods=['DELETE'])
@login_required
def delete_plan(plan_id):
    try:
        plan = Plan.query.get_or_404(plan_id)
        db.session.delete(plan)
        db.session.commit()
        return jsonify({'message':'You have successfully deleted your plan'}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500


@app.route('/subscription',methods=['POST'])
@login_required
def subscription():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        plan_id = data.get('plan_id')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        is_active = data.get('is_active')
        if not user_id or not plan_id:
            return jsonify({'message':'Please user_id and plan_id are required'})

        parsed_start_date = parser.parse(start_date) if start_date else datetime.utcnow()
        parsed_end_date = parser.parse(end_date) if end_date else None

        new_subscription = Subscription(
            user_id=user_id,
            plan_id=plan_id,
            start_date=parsed_start_date,
            end_date=parsed_end_date,
            is_active=is_active
        )

        db.session.add(new_subscription)
        db.session.commit()
        return jsonify({'message':'Subscription has been created'}),201
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500


@app.route('/get_subscription',methods =['GET'])
@login_required
def get_subscription():
    try:
        subscriptions = Subscription.query.all()
        subscription_list = [
            {
                'user_id':subscription.user_id,
                'plan_id':subscription.plan_id,
                'start_date':subscription.start_date,
                'end_date':subscription.end_date,
                'is_active':subscription.is_active
            }
            for subscription in subscriptions
        ]
        return jsonify({'subscription':subscription_list}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500


@app.route('/single_subscription/<int:subscription_id>',methods=['GET'])
@login_required
def single_subscription(subscription_id):
    try:
        subscription = Subscription.query.get_or_404(subscription_id)
        subscription_list = {
            'user_id':subscription.user_id,
            'plan_id':subscription.plan_id,
            'start_date':subscription.start_date,
            'end_date':subscription.end_date,
            'is_active':subscription.is_active
        }
        return jsonify({'message':'This is the subscription plan','data':subscription_list}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@app.route('/delete_subscription/<int:subscription_id>',methods = ['DELETE'])
@login_required
def delete_subscription(subscription_id):
    try:
        subscription = Subscription.query.get_or_404(subscription_id)
        db.session.delete(subscription)
        db.session.commit()
        return jsonify({'message':'Your subscription has been deleted'}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500





if __name__ =='__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
