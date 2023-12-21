from service.db.models.subscription import Subscription, session

from datetime import datetime


class SubscriptionService:
    @staticmethod
    def create_subscription(request):
        if not isinstance(request, dict):
            raise ValueError("Request must be a dict")

        new_subscription = Subscription(
            user_id=request.get('user_id'),
            product_id=request.get('product_id'),
            start_date=request.get('start_date'),
            end_date=request.get('end_date'),
            status=request.get('status')
        )

        session.add(new_subscription)
        session.commit()

        return new_subscription

    @staticmethod
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

    @staticmethod
    def delete_subscription(request):
        existing_subscription = session.query(Subscription).filter_by(
            subscription_id=request.subscription_id).first()
        if existing_subscription:
            session.delete(existing_subscription)
            session.commit()
            return existing_subscription
        else:
            return None

    @staticmethod
    def get_subscription_details(request):
        # Allow fetching subscriptions based on user_id, product_id, and a time window
        filters = {}
        if request.user_id:
            filters['user_id'] = request.user_id
        if request.product_id:
            filters['product_id'] = request.product_id
        if request.start_date and request.end_date:
            filters['start_date'] = (Subscription.start_date >= request.start_date) & (
                Subscription.start_date <= request.end_date)

        return session.query(Subscription).filter_by(**filters).first()

    @staticmethod
    def get_active_subscriptions(start_date, end_date):
        # Retrieve active subscriptions within a specified date range
        return session.query(Subscription).filter(
            (Subscription.start_date <= end_date) & (Subscription.end_date >= start_date) &
            (Subscription.status == 'active')
        ).all()
