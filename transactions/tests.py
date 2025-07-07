from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from transactions.models import Budget, Transaction


class TransactionViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.other_user = User.objects.create_user(username="otheruser", password="testpass123")
        self.admin = User.objects.create_superuser(username="nay_s", password="adminpass123", email="nay_s@example.com")
        self.transaction = Transaction.objects.create(
            user=self.user,
            title="Test Income",
            amount=1000.00,
            transaction_type="Income",
            category="Salary",
            date="2025-02-01",
            payment_method="bank_transfer",
        )

    def test_transaction_list_authenticated(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("transaction_list"))
        self.assertEqual(response.status_code, 200)

    def test_transaction_list_unauthenticated(self):
        response = self.client.get(reverse("transaction_list"))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_add_transaction(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("add_transaction"),
            {
                "title": "New Transaction",
                "amount": 500.00,
                "transaction_type": "Expense",
                "category": "Food",
                "date": "2025-02-02",
                "payment_method": "cash",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Transaction.objects.filter(title="New Transaction").exists())

    def test_edit_transaction_owner(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("edit_transaction", kwargs={"transaction_id": self.transaction.id}),
            {
                "title": "Updated Title",
                "amount": 1200.00,
                "transaction_type": "Income",
                "category": "Bonus",
                "date": "2025-02-05",
                "payment_method": "bank_transfer",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.title, "Updated Title")

    def test_edit_transaction_non_owner(self):
        self.client.login(username="otheruser", password="testpass123")
        response = self.client.post(
            reverse("edit_transaction", kwargs={"transaction_id": self.transaction.id}),
            {
                "title": "Unauthorized Edit",
                "amount": 1500.00,
                "transaction_type": "Income",
                "category": "Salary",
                "date": "2025-02-01",
                "payment_method": "bank_transfer",
            },
        )
        self.assertEqual(response.status_code, 403)
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.title, "Test Income")

    def test_delete_transaction_owner(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(reverse("delete_transaction", kwargs={"transaction_id": self.transaction.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Transaction.objects.filter(id=self.transaction.id).exists())

    def test_delete_transaction_non_owner(self):
        self.client.login(username="otheruser", password="testpass123")
        response = self.client.post(reverse("delete_transaction", kwargs={"transaction_id": self.transaction.id}))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Transaction.objects.filter(id=self.transaction.id).exists())


class BudgetViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.other_user = User.objects.create_user(username="otheruser", password="testpass123")
        self.admin = User.objects.create_superuser(username="nay_s", password="adminpass123", email="nay_s@example.com")
        self.budget = Budget.objects.create(
            user=self.user,
            category="Food",
            amount=500.00,
            start_date="2025-02-01",
            end_date="2025-02-28",
        )

    def test_add_budget(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("add_budget"),
            {
                "category": "Transport",
                "amount": 300.00,
                "start_date": "2025-02-01",
                "end_date": "2025-02-28",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Budget.objects.filter(category="Transport").exists())

    def test_edit_budget_owner(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("edit_budget", kwargs={"budget_id": self.budget.id}),
            {
                "category": "Updated Category",
                "amount": 700.00,
                "start_date": "2025-02-01",
                "end_date": "2025-02-28",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.budget.refresh_from_db()
        self.assertEqual(self.budget.category, "Updated Category")

    def test_edit_budget_non_owner(self):
        self.client.login(username="otheruser", password="testpass123")
        response = self.client.post(
            reverse("edit_budget", kwargs={"budget_id": self.budget.id}),
            {
                "category": "Unauthorized Edit",
                "amount": 800.00,
                "start_date": "2025-02-01",
                "end_date": "2025-02-28",
            },
        )
        self.assertEqual(response.status_code, 403)
        self.budget.refresh_from_db()
        self.assertEqual(self.budget.category, "Food")

    def test_delete_budget_owner(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(reverse("delete_budget", kwargs={"budget_id": self.budget.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Budget.objects.filter(id=self.budget.id).exists())

    def test_delete_budget_non_owner(self):
        self.client.login(username="otheruser", password="testpass123")
        response = self.client.post(reverse("delete_budget", kwargs={"budget_id": self.budget.id}))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Budget.objects.filter(id=self.budget.id).exists())
