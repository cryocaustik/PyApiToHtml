import os
from datetime import datetime
import requests 
from helpers import exception_handler
import json


class SeattlePDApi:
    """Seattle Police Department API Crime Data Explorer

    [Data API Reference](https://data.seattle.gov/Public-Safety/Crime-Data/4fs7-3vj5)
    """

    def __init__(self):
        self.api_url = 'https://data.seattle.gov/resource/xurz-654a.json'
        self.export_dir = './exports'

    def pull_data(self):
        try:
            response = requests.get(self.api_url)
            if response.status_code != 200:
                response.raise_for_status

            results = response.json()
            if not results:
                raise ValueError('response contained no json results')
            
            return results
        except requests.ConnectionError as _err:
            request_response = [response.status_code, response.text]
            exception_handler('pull_data', _err, msg=request_response)
        except Exception as _err:
            exception_handler('pull_data', _err)

    def export_raw_json(self, export_path=None):
        if not export_path:
            export_path = os.path.join(self.export_dir, 'raw_json_{}.json'.format(datetime.now().strftime('%Y%m%d')))
        
        data = self.pull_data()
        with open(export_path, 'w') as _f:
            json.dump(data, _f)
            _f.close()
        print('exported to: {}'.format(export_path))
        return export_path

    def get_crimes_by_date(self):
        try:
            data = self.pull_data()
            results = {}
            for rcd in data:
                time = rcd.get('occ_time')
                while len(time) < 4:
                    time = '0' + time
                
                dt = datetime.strptime(rcd.get('occ_datetime'), '%Y-%m-%dT%H:%M:%S.%f').date()
                time = datetime.strptime(time, '%H%M').time()
                dt_time = datetime.combine(dt, time)
                dt_time_str = datetime.combine(dt, time).strftime('%Y-%m-%d')
                if dt_time_str not in results:
                    results[dt_time_str] = {
                        'datetime': dt_time,
                        'date': dt_time_str,
                        'crimes': [],
                        'cnt': 0
                    }
                results[dt_time_str]['cnt'] += 1
                if rcd.get('crime_description') not in results[dt_time_str]['crimes']:
                    results[dt_time_str]['crimes'].append(rcd.get('crime_description'))
            results = [results[k] for k in results]
            results.sort(key=lambda k: k['date'])
            return results
        except Exception as _err:
            exception_handler('get_crimes_by_date', _err)


if __name__ == '__main__':
    s = SeattlePDApi()
    print(str(s.get_crimes_by_date()))

