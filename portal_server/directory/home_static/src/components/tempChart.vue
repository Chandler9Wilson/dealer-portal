<template>
<canvas id="myChart" width="400" height="400"></canvas>
</template>

<script>
import Chart from 'chart.js'

export default {
  name: 'tempChart',
  props: [
    't1',
    't2'
  ],
  mounted() {
    this.createChart()
  },
  methods: {
    createChart() {
      var self = this
      var ctx = document.getElementById('myChart')

      var tempComparisonChart = new Chart(ctx, {
        type: 'line',
        data: {
          datasets: [{
            label: 'Intake',
            data: self.t1,
            borderColor: "#3e95cd"
          }, {
            label: 'Vent',
            data: self.t2,
            borderColor: "#8e5ea2"
          }]
        },
        options: {
          scales: {
            xAxes: [{
              type: 'time',
              time: {
                unit: 'day',
                unitStepSize: 1,
                displayFormats: {
                  'day': 'MMM DD'
                }
              }
            }]
          }
        }
        //responsive: true
      })
    }
  }
}
</script>