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
        label: '단독주택',
        data: [ //단독주택
          data1[labels[0]],
          data1[labels[1]],
          data1[labels[2]],
          data1[labels[3]],
          data1[labels[4]],
          data1[labels[5]],
          data1[labels[6]],
          data1[labels[7]],
          data1[labels[8]],
          data1[labels[9]],
          data1[labels[10]],
          data1[labels[11]]
        ],
        
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 3,
        pointBackgroundColor: '#007bff'
      },
      {
        label: '아파트',
        data: [ //아파트
          data2[labels[0]],
          data2[labels[1]],
          data2[labels[2]],
          data2[labels[3]],
          data2[labels[4]],
          data2[labels[5]],
          data2[labels[6]],
          data2[labels[7]],
          data2[labels[8]],
          data2[labels[9]],
          data2[labels[10]],
          data2[labels[11]],
          data2[labels[12]],
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#dc3545',
        borderWidth: 3,
        pointBackgroundColor: '#dc3545'
      },
      {
        label: '연립주택',
        data: [ //연립주택
          data3[labels[0]],
          data3[labels[1]],
          data3[labels[2]],
          data3[labels[3]],
          data3[labels[4]],
          data3[labels[5]],
          data3[labels[6]],
          data3[labels[7]],
          data3[labels[8]],
          data3[labels[9]],
          data3[labels[10]],
          data3[labels[11]],
          data3[labels[12]],
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#20c997',
        borderWidth: 3,
        pointBackgroundColor: '#20c997'
      },
      {
        label: '오피스텔',
        data: [ //오피스텔
          data4[labels[0]],
          data4[labels[1]],
          data4[labels[2]],
          data4[labels[3]],
          data4[labels[4]],
          data4[labels[5]],
          data4[labels[6]],
          data4[labels[7]],
          data4[labels[8]],
          data4[labels[9]],
          data4[labels[10]],
          data4[labels[11]],
          data4[labels[12]],
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#6610f2',
        borderWidth: 3,
        pointBackgroundColor: '#6610f2'
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
        display: true
      }
    }
  })
})()
