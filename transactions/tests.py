from django.test import TestCase, Client
from django.contrib.auth.models import User
from transactions.models import Transaction, Budget
from transactions.forms import TransactionForm, BudgetForm
from django.urls import reverse
from django.core.exceptions import ValidationError  # Import added for clarity

class TransactionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.transaction = Transaction.objects.create(
            user=self.user,
            title='Test Income',
            amount=1000.00,
            transaction_type='Income',
            category='Salary',
            date='2025-02-01',
            payment_method='bank_transfer'
        )

    def test_transaction_creation(self):
        self.assertEqual(self.transaction.title, 'Test Income')
        self.assertEqual(self.transaction.amount, 1000.00)
        self.assertEqual(self.transaction.transaction_type, 'Income')
        self.assertTrue(self.transaction.user == self.user)

    def test_transaction_validation(self):
        with self.assertRaises(ValidationError):  # Updated to ValidationError
            Transaction.objects.create(
                user=self.user,
                title='Invalid Amount',
                amount=-100.00,  # Should raise validation error
                transaction_type='Expense',
                category='Test',
                date='2025-02-01',
                payment_method='cash'
            )

class BudgetModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.budget = Budget.objects.create(
            user=self.user,
            category='Food',
            amount=500.00,
            start_date='2025-02-01',
            end_date='2025-02-28'
        )

    def test_budget_creation(self):
        self.assertEqual(self.budget.category, 'Food')
        self.assertEqual(self.budget.amount, 500.00)
        self.assertTrue(self.budget.user == self.user)

    def test_budget_validation(self):
        with self.assertRaises(ValidationError):  # Updated to ValidationError
            Budget.objects.create(
                user=self.user,
                category='Invalid Amount',
                amount=-50.00,  # Should raise validation error
                start_date='2025-02-01',
                end_date='2025-02-28'
            )

class TransactionFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_valid_transaction_form(self):
        form_data = {
            'title': 'Test Income',
            'amount': 1000.00,
            'transaction_type': 'Income',
            'category': 'Salary',
            'date': '2025-02-01',
            'payment_method': 'bank_transfer'
        }
        form = TransactionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_transaction_form(self):
        form_data = {
            'title': '',
            'amount': -100.00,  # Invalid amount
            'transaction_type': 'Income',
            'category': 'Salary',
            'date': '2025-02-01',
            'payment_method': 'bank_transfer'
        }
        form = TransactionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('amount', form.errors)

class BudgetFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_valid_budget_form(self):
        form_data = {
            'category': 'Food',
            'amount': 500.00,
            'start_date': '2025-02-01',
            'end_date': '2025-02-28'
        }
        form = BudgetForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_budget_form(self):
        form_data = {
            'category': '',
            'amount': -50.00,  # Invalid amount
            'start_date': '2025-02-01',
            'end_date': '2025-02-28'
        }
        form = BudgetForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)
        self.assertIn('amount', form.errors)

class TransactionViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.admin = User.objects.create_superuser(username='nay_s', password='adminpass123', email='nay_s@example.com')
        self.transaction = Transaction.objects.create(
            user=self.user,
            title='Test Income',
            amount=1000.00,
            transaction_type='Income',
            category='Salary',
            date='2025-02-01',
            payment_method='bank_transfer'
        )

    def test_transaction_list_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('transaction_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transactions/transaction_list.html')
        self.assertContains(response, 'Test Income')

    def test_transaction_list_unauthenticated(self):
        response = self.client.get(reverse('transaction_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, '/accounts/login/?next=/transactions/')

    def test_add_transaction_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('add_transaction'), {
            'title': 'New Expense',
            'amount': 200.00,
            'transaction_type': 'Expense',
            'category': 'Food',
            'date': '2025-02-02',
            'payment_method': 'cash'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to transaction_list
        self.assertTrue(Transaction.objects.filter(title='New Expense').exists())

    def test_edit_transaction_owner(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('edit_transaction', kwargs={'transaction_id': self.transaction.id}), {
            'title': 'Updated Income',
            'amount': 1200.00,
            'transaction_type': 'Income',
            'category': 'Salary',
            'date': '2025-02-01',
            'payment_method': 'bank_transfer'
        })
        self.assertEqual(response.status_code, 302)
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.title, 'Updated Income')

    def test_edit_transaction_non_owner(self):
        other_user = User.objects.create_user(username='otheruser', password='testpass123')  # Regular user
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.post(reverse('edit_transaction', kwargs={'transaction_id': self.transaction.id}), {
            'title': 'Unauthorized Edit',
            'amount': 1500.00,
            'transaction_type': 'Income',
            'category': 'Salary',
            'date': '2025-02-01',
            'payment_method': 'bank_transfer'
        })
        self.assertEqual(response.status_code, 403)  # Expect Permission Denied
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.title, 'Test Income')  # Unchanged

    def test_edit_transaction_superuser(self):
        self.client.login(username='nay_s', password='adminpass123')
        response = self.client.post(reverse('edit_transaction', kwargs={'transaction_id': self.transaction.id}), {
            'title': 'Admin Edit',
            'amount': 1500.00,
            'transaction_type': 'Income',
            'category': 'Salary',
            'date': '2025-02-01',
            'payment_method': 'bank_transfer'
        })
        self.assertEqual(response.status_code, 302)  # Superuser succeeds
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.title, 'Admin Edit')

    def test_delete_transaction_owner(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('delete_transaction', kwargs={'transaction_id': self.transaction.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Transaction.objects.filter(id=self.transaction.id).exists())

    def test_delete_transaction_non_owner(self):
        other_user = User.objects.create_user(username='otheruser', password='testpass123')
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.post(reverse('delete_transaction', kwargs={'transaction_id': self.transaction.id}))
        self.assertEqual(response.status_code, 403)  # Expect Permission Denied
        self.assertTrue(Transaction.objects.filter(id=self.transaction.id).exists())  # Not deleted

    def test_delete_transaction_superuser(self):
        self.client.login(username='nay_s', password='adminpass123')
        response = self.client.post(reverse('delete_transaction', kwargs={'transaction_id': self.transaction.id}))
        self.assertEqual(response.status_code, 302)  # Superuser succeeds
        self.assertFalse(Transaction.objects.filter(id=self.transaction.id).exists())

class BudgetViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.admin = User.objects.create_superuser(username='nay_s', password='adminpass123', email='nay_s@example.com')
        self.budget = Budget.objects.create(
            user=self.user,
            category='Food',
            amount=500.00,
            start_date='2025-02-01',
            end_date='2025-02-28'
        )

    def test_budget_list_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('budget_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transactions/budget_list.html')
        self.assertContains(response, 'Food')

    def test_budget_list_unauthenticated(self):
        response = self.client.get(reverse('budget_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, '/accounts/login/?next=/transactions/budgets/')

    def test_add_budget_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('add_budget'), {
            'category': 'Rent',
            'amount': 1000.00,
            'start_date': '2025-03-01',
            'end_date': '2025-03-31'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to budget_list
        self.assertTrue(Budget.objects.filter(category='Rent').exists())

    def test_edit_budget_owner(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('edit_budget', kwargs={'budget_id': self.budget.id}), {
            'category': 'Updated Food',
            'amount': 600.00,
            'start_date': '2025-02-01',
            'end_date': '2025-02-28'
        })
        self.assertEqual(response.status_code, 302)
        self.budget.refresh_from_db()
        self.assertEqual(self.budget.category, 'Updated Food')

    def test_edit_budget_non_owner(self):
        other_user = User.objects.create_user(username='otheruser', password='testpass123')
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.post(reverse('edit_budget', kwargs={'budget_id': self.budget.id}), {
            'category': 'Unauthorized Food',
            'amount': 700.00,
            'start_date': '2025-02-01',
            'end_date': '2025-02-28'
        })
        self.assertEqual(response.status_code, 403)  # Expect Permission Denied
        self.budget.refresh_from_db()
        self.assertEqual(self.budget.category, 'Food')  # Unchanged

    def test_edit_budget_superuser(self):
        self.client.login(username='nay_s', password='adminpass123')
        response = self.client.post(reverse('edit_budget', kwargs={'budget_id': self.budget.id}), {
            'category': 'Admin Food',
            'amount': 700.00,
            'start_date': '2025-02-01',
            'end_date': '2025-02-28'
        })
        self.assertEqual(response.status_code, 302)  # Superuser succeeds
        self.budget.refresh_from_db()
        self.assertEqual(self.budget.category, 'Admin Food')

    def test_delete_budget_owner(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('delete_budget', kwargs={'budget_id': self.budget.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Budget.objects.filter(id=self.budget.id).exists())

    def test_delete_budget_non_owner(self):
        other_user = User.objects.create_user(username='otheruser', password='testpass123')
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.post(reverse('delete_budget', kwargs={'budget_id': self.budget.id}))
        self.assertEqual(response.status_code, 403)  # Expect Permission Denied
        self.assertTrue(Budget.objects.filter(id=self.budget.id).exists())  # Not deleted

    def test_delete_budget_superuser(self):
        self.client.login(username='nay_s', password='adminpass123')
        response = self.client.post(reverse('delete_budget', kwargs={'budget_id': self.budget.id}))
        self.assertEqual(response.status_code, 302)  # Superuser succeeds
        self.assertFalse(Budget.objects.filter(id=self.budget.id).exists())