from service.db.models.subscription import Subscription, session
from datetime import datetime

from service.utils.logging import log_function_errors, logger

@log_function_errors(logger)
def create_subscription(request):
    if not isinstance(request, dict):
        raise ValueError("Request must be a dict")

    extract_date = lambda dt_str: datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%SZ').date().strftime('%Y-%m-%d')
    new_subscription = Subscription(
        user_id=request.get('user_id'),
        product_id=request.get('product_id'),
        start_date=extract_date(request.get('start_date')),
        end_date=extract_date(request.get('end_date')),
        status=request.get('status')
    )

    session.add(new_subscription)
    session.commit()

    return new_subscription

@log_function_errors(logger)
def modify_subscription(request):
    existing_subscription = session.query(Subscription).filter_by(
        subscription_id=request.subscription_id).first()
    if existing_subscription:
        existing_subscription.user_id = request.user_id
        existing_subscription.product_id = request.product_id
        existing_subscription.start_date = request.start_date
        existing_subscription.end_date = request.end_date
        existing_subscription.status = request.status
        session.commit()
        return existing_subscription
    else:
        return None

@log_function_errors(logger)
def delete_subscription(request):
    existing_subscription = session.query(Subscription).filter_by(
        subscription_id=request.subscription_id).first()
    if existing_subscription:
        session.delete(existing_subscription)
        session.commit()
        return existing_subscription
    else:
        return None

@log_function_errors(logger)
def get_subscription_details(request):
  if not isinstance(request, dict):
    raise TypeError("Request must be a dict")

  filters = {}
  if 'user_id' in request and request['user_id']:
    filters['user_id'] = request['user_id']

  if 'product_id' in request and request['product_id']:  
    filters['product_id'] = request['product_id']

  if 'start_date' in request and 'end_date' in request:
    start_date = datetime.fromisoformat(request['start_date'])
    end_date = datetime.fromisoformat(request['end_date']) 

    # # Add time comparision filters
    # if request['start_date'] and request['end_date']:
    #   filters['start_date'] = (Subscription.start_date >= start_date) & (
    #       Subscription.start_date <= end_date) & (
    #           Subscription.end_date >= end_date)

  try:
    result = session.query(Subscription).filter_by(**filters).filter(
       (Subscription.start_date >= start_date) & (
          Subscription.start_date <= end_date) & (
              Subscription.end_date <= end_date )).all()
    
    return result
  except Exception as e:
    print("Error fetching subscription: ", e)
    return None


@log_function_errors(logger)
def get_active_subscriptions(start_date, end_date):
    # Retrieve active subscriptions within a specified date range
    return session.query(Subscription).filter(
        (Subscription.start_date <= end_date) & (Subscription.end_date >= start_date) &
        (Subscription.status == 'active')
    ).all()
