/*
 Gobierno Transparente
*/
var citations;
var attendance;

$(document).ready(function() {
  // Citations
  citations = new Highcharts.Chart({
      chart: {
         renderTo: 'citations',
         defaultSeriesType: 'column'
      },
      credits: {
          enabled: false
      },
      title: false,
      xAxis: {
         categories: ['Partido Blanco', 'Partido Colorado', 'Frente Amplio', 'Partido Independiente']
      },
      yAxis: {
         min: 0,
         title: {
            text: 'Citaciones'
         },
         stackLabels: {
            enabled: true,
            style: {
               fontWeight: 'bold',
               color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
            }
         }
      },
      tooltip: {
         formatter: function() {
            return '<b>'+ this.x +'</b><br/>'+
                this.series.name +': '+ this.y +'<br/>'+
                'Total: '+ this.point.stackTotal;
         }
      },
      plotOptions: {
         column: {
            stacking: 'normal',
            dataLabels: {
               enabled: true,
               color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
            }
         }
      },
      colors: [
        '#89A54E', 
        '#AA4643' 
      ],
      series: [{
         name: 'Asistencias',
         data: [5, 3, 4, 7],
         backgroundColor: 'green'
      }, {
         name: 'Inasistencias',
         data: [3, 4, 4, 2]
      }]
   });

   // Attendance
   attendance = new Highcharts.Chart({
      chart: {
         renderTo: 'attendance',
         defaultSeriesType: 'line'
      },
      credits: {
          enabled: false
      },
      title: false,
      xAxis: {
         categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

      },
      yAxis: {
         title: {
            text: 'Asistencia'
         },
         plotLines: [{
            value: 0,
            width: 1,
            color: '#808080'
         }]
      },
      tooltip: {
         formatter: function() {
                   return '<b>'+ this.series.name +'</b><br/>'+
               this.x +': '+ this.y +'Â°C';
         }
      },
      series: [{
         name: 'Tokyo',
         data: [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
      }, {
         name: 'New York',
         data: [-0.2, 0.8, 5.7, 11.3, 17.0, 22.0, 24.8, 24.1, 20.1, 14.1, 8.6, 2.5]
      }, {
         name: 'Berlin',
         data: [-0.9, 0.6, 3.5, 8.4, 13.5, 17.0, 18.6, 17.9, 14.3, 9.0, 3.9, 1.0]
      }, {
         name: 'London',
         data: [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
      }]
   }); 
});
