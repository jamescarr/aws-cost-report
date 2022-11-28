import click 
import boto3
import datetime
import pprint

__version__ = '0.1.0'


class ReportOutput(object):
    def __init__(self):
        pass

    def start(self):
        pass

    def add(self, result_by_time):
        pass

    def end(self):
        pass


# Use https://xlsxwriter.readthedocs.io/
class XlsxOutput(ReportOutput):
    pass

# https://developers.google.com/sheets/api/quickstart/python
class GoogleSheetsOutput(ReportOutput):
    pass

class TSVReportOutput(ReportOutput):
    def __init__(self):
        session = boto3.session.Session()
        self.org = session.client('organizations', 'us-east-1')
        self.linked_account_mapping = {}


    def start(self):
        print('\t'.join(['TimePeriod', 'Service', 'Amount']))

    def get_account_name(self, id):
        if id not in self.linked_account_mapping.keys():
            try:
                account = self.org.describe_account(AccountId=id)
                self.linked_account_mapping[id] = account['Account']['Name']
            except:
                return ''
        return self.linked_account_mapping[id]

    def add(self, result_by_time):
        current_account = None
        
        for group in result_by_time['Groups']:
            (account, service) = group['Keys']
            if current_account != account:
                current_account = account
                print('')
                print(account, '\t', self.get_account_name(account))

            amount = group['Metrics']['UnblendedCost']['Amount']
            unit = group['Metrics']['UnblendedCost']['Unit']
            print(result_by_time['TimePeriod']['Start'], '\t', 
                  service, '\t', 
                  amount)



@click.command()
@click.option('--days',         default=30,      help="Number of days to report")
@click.option('--start',        default=None,    help="Start date to report, in YYYY-MM-DD format")
@click.option('--end',          default=None,    help="End date to report, in YYYY-MM-DD format")
@click.option('--grainularity', default='DAILY', help='One of HOURLY, DAILY, MONTHLY')
def report(days, start, end, grainularity):
    now = datetime.datetime.utcnow()
    _start = start or (now - datetime.timedelta(days=days)).strftime('%Y-%m-%d')
    _end = end or now.strftime('%Y-%m-%d')
    output = TSVReportOutput()
    output.start()

    for result_by_time in get_cost_explorer_data(_start, _end, grainularity):
        output.add(result_by_time)

    output.end()

def get_cost_explorer_data(start, end, grainularity, **kwargs):
    # create a session for cost explorer. 
    session = boto3.session.Session()
    cd = session.client('ce', 'us-east-1')
    org = session.client('organizations', 'us-east-1')

    token = None
    while True:
        if token:
            kwargs = {'NextPageToken': token}
        else:
            kwargs = {}
        data = cd.get_cost_and_usage(TimePeriod={'Start': start, 'End':  end}, 
                                     Granularity=grainularity,
                                     Metrics=['UnblendedCost'], 
                                     GroupBy=[
                                         {'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'}, 
                                         {'Type': 'DIMENSION', 'Key': 'SERVICE'}], 
                                     **kwargs)
        
        for result in data['ResultsByTime']:

            yield result

        token = data.get('NextPageToken')
        if not token:
            break
    


if __name__ == '__main__':
    report()
