const ctx = document.getElementById('myChart').getContext('2d');

// Chart data
const data = {
    labels: ['Red', 'Blue', 'Yellow'],
    datasets: [{
        label: 'My First Dataset',
        data: [300, 50, 100],
        backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 205, 86)'
        ],
        hoverOffset: 4
    }]
};

// Configuration options
const options = {
    responsive: true,
    maintainAspectRatio: false
};

// Create the chart
const myChart = new Chart(ctx, {
    type: 'doughnut',
    data: data,
    options: options
});

