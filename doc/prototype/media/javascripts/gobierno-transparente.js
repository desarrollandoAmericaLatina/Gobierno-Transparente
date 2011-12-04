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
      title: {
         text: 'Stacked column chart'
      },
      xAxis: {
         categories: ['Apples', 'Oranges', 'Pears', 'Grapes', 'Bananas']
      },
      yAxis: {
         min: 0,
         title: {
            text: 'Total fruit consumption'
         },
         stackLabels: {
            enabled: true,
            style: {
               fontWeight: 'bold',
               color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
            }
         }
      },
      legend: {
         align: 'right',
         x: -100,
         verticalAlign: 'top',
         y: 20,
         floating: true,
         backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColorSolid) || 'white',
         borderColor: '#CCC',
         borderWidth: 1,
         shadow: false
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
       series: [{
         name: 'John',
         data: [5, 3, 4, 7, 2]
      }, {
         name: 'Jane',
         data: [2, 2, 3, 2, 1]
      }, {
         name: 'Joe',
         data: [3, 4, 4, 2, 5]
      }]
   });

   // Attendance
   attendance = new Highcharts.Chart({
      chart: {
         renderTo: 'attendance',
         defaultSeriesType: 'line',
         marginRight: 130,
         marginBottom: 25
      },
      title: {
         text: 'Monthly Average Temperature',
         x: -20 //center
      },
      subtitle: {
         text: 'Source: WorldClimate.com',
         x: -20
      },
      xAxis: {
         categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
      },
      yAxis: {
         title: {
            text: 'Temperature (Â°C)'
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
      legend: {
         layout: 'vertical',
         align: 'right',
         verticalAlign: 'top',
         x: -10,
         y: 100,
         borderWidth: 0
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
