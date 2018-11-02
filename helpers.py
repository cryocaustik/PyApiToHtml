import os
from datetime import datetime
from json import dumps


def exception_log_path():
    log_dir = './logs'
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    
    path = '{d]/error_{dt}.log'.format(
        d=log_dir,
        dt=datetime.now().strftime('%Y%m%d')
    )
    return path

def exception_handler(caller_name, exception, msg=None):
    log_dir = './logs'
    try:
        if not os.path.isdir(log_dir):
            os.mkdir(log_dir)
        log_path = '{d]/error_{dt}.log'.format(
            d=log_dir,
            dt=datetime.now().strftime('%Y%m%d')
        )
        err_msg = {
            'date': datetime.now().strftime('%Y%m%d_%H%M%S'),
            'caller': caller_name,
            'error_type': type(exception).__name__,
            'error_msg': exception.args,
            'additional_msg': str(msg) if msg else None,
        }
        with open(log_dir, 'a') as _f:
            _f.write(dumps(err_msg))
            _f.close()
        print(dumps(err_msg))
        
        usr_response = input('\n\nexit program? (Y/n)')
        if not usr_response.lower() == 'n':
            exit()
    except Exception as _err:
        err_msg = {
            'date': datetime.now().strftime('%Y%m%d_%H%M%S'),
            'caller': caller_name,
            'error_type': type(_err).__name__,
            'error_msg': _err.args,
            'additional_msg': 'error occurred when called by {c}'.format(c=caller_name),
        }
        if os.path.isdir(log_dir):
            log_path = '{d]/error_{dt}.log'.format(
                d=log_dir,
                dt=datetime.now().strftime('%Y%m%d')
            )
        else:
            log_path = '{d}/seattle_crime_errors_{dt}.log'.format(
                d=os.environ.get('temp'),
                dt=datetime.now().strftime('%Y%m%d')
            )
        with open(log_dir, 'a') as _f:
            _f.write(dumps(err_msg))
            _f.close()
        print(dumps(err_msg))
        print('errors logged to: {p]').format(p=log_path)
