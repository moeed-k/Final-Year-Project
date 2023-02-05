var ctx = document.getElementById("myChart1").getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Authenticity', 'Confidence', 'Persuasion', 'Reliability'],
      datasets: [{
        label: 'Score',
        data: [50, 40, 80, 20 ],
        borderWidth: 1,
        backgroundColor: [
          'rgba(168, 98, 189, 0.566)'
          
        ],
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });


  var ctx = document.getElementById("myChart2").getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['', ' ', ' ', ' ','', ' ', ' ', ' '],
      datasets: [
        {
          label: 'Pitch 1',
          data: [19,27,32,36,50,67,99,88],
          // borderColor: Utils.CHART_COLORS.red,
          // backgroundColor: Utils.transparentize(Utils.CHART_COLORS.red, 0.5),
          yAxisID: 'y',
        },
        {
          label: 'Pitch 2',
          data: [59,57,82,16,40,60,70,55],
          // borderColor: Utils.CHART_COLORS.blue,
          // backgroundColor: Utils.transparentize(Utils.CHART_COLORS.blue, 0.5),
          yAxisID: 'y1',
        },
        {
          label: 'Pitch 3',
          data: [25,45,70,60,40,58,75,50],
          // borderColor: Utils.CHART_COLORS.blue,
          // backgroundColor: Utils.transparentize(Utils.CHART_COLORS.blue, 0.5),
          yAxisID: 'y1',
        }
      ]
    },
    options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
  });
  


  var ctx = document.getElementById("myChart3").getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['January', 'Febuary', 'March', 'April','May', 'June', 'July', 'August'],
      datasets: [{
        label: 'Number Of Tests',
        data: [5, 4, 8, 1 ,10, 11, 2, 4],
        borderWidth: 1,
        backgroundColor: [
          'rgba(168, 98, 189, 0.566)'
          
        ]
      }]
    },
    options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
  });
  

