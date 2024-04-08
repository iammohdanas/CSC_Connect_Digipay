var swiper = new Swiper(".mySwiper", {
    effect: "cards",
    grabCursor: true,
    navigation: {
        nextEl: ".swipe_next",
        prevEl: ".swipe_previous",
    },
    pagination: {
        el: ".swiper-page",
        clickable: true,
    },
});

document.querySelector('.r_transaction').addEventListener('click', function() {
    document.querySelector('.transaction_info').style.display = 'block';
    document.querySelector('.plot_chart').style.display = 'none';
});

document.querySelector('.s_analysis').addEventListener('click', function() {
    document.querySelector('.transaction_info').style.display = 'none';
    document.querySelector('.plot_chart').style.display = 'block';
    var ctx = document.getElementById('lineChart').getContext('2d');
    var lineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Sample Data',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
});

