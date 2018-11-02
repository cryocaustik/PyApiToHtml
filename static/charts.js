$.get('http://127.0.0.1:5000/api/bydate', data => {
        let chart1 = c3.generate({
            bindto: '#chart1',
            data: {
                json: data,
                keys: {
                    x: 'date',
                    value: ['cnt']
                },
                type: 'area-spline',
            },
            axis: {
                x: {
                    type: 'timeseries',
                    tick: {
                        format: '%Y-%m-%d'
                    }
                },
            }
        });

    })
    .fail(response => {
        console.log('error: ', response);
    })
    .always(() => {
        console.log('getData done!');
    });
