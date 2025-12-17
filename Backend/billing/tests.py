from django.test import TestCase
from infrastructure.models import Tenant
from .models import Plan, Subscription

class BillingModelTests(TestCase):
    def test_create_plan_and_subscription(self):
        tenant = Tenant.objects.create(name="Billing Tenant")
        plan = Plan.objects.create(name="Pro", limit_funnels=10)

        subscription = Subscription.objects.create(tenant=tenant, plan=plan)

        self.assertEqual(tenant.subscription, subscription)
        self.assertEqual(subscription.plan.name, "Pro")
        self.assertEqual(subscription.plan.limit_funnels, 10)
