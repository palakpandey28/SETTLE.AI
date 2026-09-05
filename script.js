function createChart() {
    const ctx = $('chart').getContext('2d');
    const volume = [45200, 52100, 48900, 61200, 55900, 38200, 42600];
    const atRisk = [2100, 3200, 1400, 4800, 1900, 2600, 1500];
    const grad = ctx.createLinearGradient(0, 0, 0, 320);
    grad.addColorStop(0, 'rgba(99, 102, 241, .18)');
    grad.addColorStop(1, 'rgba(99, 102, 241, 0)');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'Settled volume',
                data: volume,
                borderColor: '#6366f1',
                backgroundColor: grad,
                borderWidth: 2,
                tension: .4,
                fill: true,
                pointRadius: 0,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: '#6366f1'
            }, {
                label: 'Amount at risk',
                data: atRisk,
                borderColor: '#f43f5e',
                backgroundColor: 'transparent',
                borderWidth: 1.5,
                borderDash: [6, 6],
                tension: .4,
                fill: false,
                pointRadius: 0,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: '#f43f5e'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#ffffff',
                    borderColor: '#e6eaf1',
                    borderWidth: 1,
                    titleColor: '#101828',
                    bodyColor: '#5b6b83',
                    padding: 12,
                    cornerRadius: 10,
                    displayColors: true,
                    callbacks: {
                        label: c => ' ' + c.dataset.label + ': ' + inr(c.parsed.y)
                    }
                }
            },
            scales: {
                x: { grid: { display: false }, ticks: { color: '#8b98ac', font: { size: 11 } } },
                y: {
                    grid: { color: 'rgba(15, 23, 42, .07)' },
                    border: { display: false },
                    ticks: {
                        color: '#8b98ac', font: { size: 11 },
                        callback: v => v >= 1000 ? '₹' + (v / 1000) + 'k' : '₹' + v
                    }
                }
            }
        }
    });
}