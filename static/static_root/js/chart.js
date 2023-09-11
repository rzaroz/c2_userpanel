var ctx = document.getElementById('meuGrafico').getContext('2d');
var chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'],
        datasets: [{
                label: 'نمودار درآمد شما',
                data: [5, 10, 45, 7, 20, 30, 45, 38, 35, 75, 50, 20],
                borderWidth: 2,
                backgroundColor: '#b071f6',
            },
        ]
    },
    options: {
        title: {
            display: true,
            fontSize: 40,
        }
    }
});