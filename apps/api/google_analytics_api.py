import datetime
from django.conf import settings
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest

class GoogleAnalyticsAPI:

    def __init__(self):
        self.client = BetaAnalyticsDataClient()
        self.property_id = settings.GOOGLE_PROPERTY_ID

    def initiate_client(self):
        return self.client

    def _get_activeXDayUsers(self, days=7, metric_name='active7DayUsers'):
        today = datetime.date.today()
        dateXDaysAgo = (today - datetime.timedelta(days=days)).strftime('%Y-%m-%I')
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            metrics=[Metric(name=metric_name)],
            date_ranges=[DateRange(start_date=f'{days}daysAgo',
                                   end_date="today")]
        )
        res = self.client.run_report(request)
        if not res.rows:
            return 0
        return res.rows[0].metric_values[0].value

    def get_active7DayUsers(self):
        return self._get_activeXDayUsers()

    def get_active28DayUsers(self):
        return self._get_activeXDayUsers(days=28, metric_name="active28DayUsers")

    def get_activeUsers(self, startDays=365):
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            metrics=[Metric(name='activeUsers')],
            date_ranges=[DateRange(start_date=f"{startDays}daysAgo",
                                   end_date="today")]
        )
        res = self.client.run_report(request)
        if not res.rows:
            return 0
        return res.rows[0].metric_values[0].value

    def get_engagedSessions(self, startDays=365):
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            metrics=[Metric(name='engagedSessions')],
            date_ranges=[DateRange(start_date=f"{startDays}daysAgo",
                                   end_date="today")]
        )
        res = self.client.run_report(request)
        if not res.rows:
            return 0
        return res.rows[0].metric_values[0].value


    def get_engagementRate(self, startDays=365):
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            metrics=[Metric(name='engagementRate')],
            date_ranges=[DateRange(start_date=f"{startDays}daysAgo", 
                                   end_date="today")]
        )
        res = self.client.run_report(request)
        if not res.rows:
            return 0
        rate = res.rows[0].metric_values[0].value
        return round(float(rate), 3)


    def get_sessions(self, startDays=365):
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            metrics=[Metric(name='sessions')],
            date_ranges=[DateRange(start_date=f"{startDays}daysAgo",
                                   end_date="today")]
        )
        res = self.client.run_report(request)
        if not res.rows:
            return 0
        return res.rows[0].metric_values[0].value
