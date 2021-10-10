/* globals Chart:false, feather:false */

(function () {
  'use strict'

  feather.replace({ 'aria-hidden': 'true' })
  
  // Graphs
  var ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [
        label_1,
        label_2,
        label_3,
        label_4,
        label_5,
        label_6,
        label_7,
        label_8,
        label_9,
        label_10,
        label_11,
        label_12
      ],
      datasets: [{
        data: [
          data_1,
          data_2,
          data_3,
          data_4,
          data_5,
          data_6,
          data_7,
          data_8,
          data_9,
          data_10,
          data_11,
          data_12
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: false
      }
    }
  })
})()
