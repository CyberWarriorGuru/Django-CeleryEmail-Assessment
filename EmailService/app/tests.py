from django.test import TestCase, Client
from .models import Lead, User, Campaign, ConnectedEmail
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .serializers import CampaignSerializer
from .utils import send_email, read_emails
from django.core import mail
# Create your tests here.
class LeadTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.lead = Lead.objects.create(name='Harsh', email='harsh@gmail.com', company='Harsh Inc', website="https://harsh.com")

    def test_get_all_leads(self):
        response = self.client.get('/api/leads/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_lead(self):
        response = self.client.get('/api/leads/{}/'.format(self.lead.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_lead(self):
        data = {'name': 'Jhon', 'email': 'Jhon@outlook.com', 'company': 'Jhon Inc', 'website': 'https://jhon.com'}
        response = self.client.post('/api/leads/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_lead(self):
        data = {'name': 'Jhon', 'email': 'Jhon_lead@outlook.com', 'company': 'Jhon Inc', 'website': 'https://jhon.com'}
        response = self.client.put('/api/leads/{}/'.format(self.lead.id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lead(self):
        response = self.client.delete('/api/leads/{}/'.format(self.lead.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class CampaignTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

        # Create a connected email
        self.connected_email = ConnectedEmail.objects.create(
            user=self.user,
            provider='Gmail',
            email='test@gmail.com',
            password='testpass'
        )

        # Create some leads
        self.lead1 = Lead.objects.create(
            name='John Smith',
            email='john@example.com',
            company='Acme Inc.',
            website='https://www.acme.com'
        )
        self.lead2 = Lead.objects.create(
            name='Jane Doe',
            email='jane@example.com',
            company='Widgets Inc.',
            website='https://www.widgets.com'
        )

        # Create a campaign
        self.campaign = Campaign.objects.create(
            connected_email=self.connected_email,
            message='Test message',
            scheduled_time='2023-04-20 12:00:00'
        )
        self.campaign.leads.set([self.lead1, self.lead2])

    def test_campaign_list_create(self):
        # Ensure we can create a new campaign
        url = '/api/campaigns/'
        data = {
            'connected_email': self.connected_email.id,
            'leads': [self.lead1.id, self.lead2.id],
            'message': 'New campaign message',
            'scheduled_time': '2023-04-22 12:00:00'
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Campaign.objects.count(), 2)

        # Ensure we can list all campaigns
        response = self.client.get(url, format='json')
        campaigns = Campaign.objects.all()
        serializer = CampaignSerializer(campaigns, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_campaign_retrieve_update_destroy(self):
        # Ensure we can retrieve a campaign by id
        url = f'/api/campaigns/{self.campaign.id}/'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        serializer = CampaignSerializer(self.campaign)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure we can update a campaign by id
        data = {
            'connected_email': self.connected_email.id,
            'leads': [self.lead1.id],
            'message': 'Updated campaign message',
            'scheduled_time': '2023-04-23 12:00:00'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Updated campaign message')

        # Ensure we can delete a campaign by id
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Ensure the campaign was deleted
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EmailTestCase(TestCase):
    def setUp(self):
        self.email = ConnectedEmail.objects.create(
            email='example@gmail.com',
            password='password',
            smtp_host='smtp.gmail.com',
            smtp_port=587,
            imap_host='imap.gmail.com',
            imap_port=993,
        )

    def test_send_email(self):
        # Send an email
        subject = 'Test email'
        body = 'This is a test email'
        from_email = 'example@gmail.com'
        to_emails = ['recipient1@example.com', 'recipient2@example.com']
        send_email(subject, body, from_email, to_emails)

        # Assert that the email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, subject)
        self.assertEqual(mail.outbox[0].body, body)
        self.assertEqual(mail.outbox[0].from_email, from_email)
        self.assertEqual(mail.outbox[0].to, to_emails)

    def test_read_emails(self):
        # Read all emails in the inbox
        emails = read_emails()

        # Assert that at least one email was found
        self.assertGreater(len(emails), 0)

        # Assert that the first email has a subject and a body
        first_email = emails[0]
        self.assertTrue(first_email['Subject'])
        self.assertTrue(first_email.get_payload())