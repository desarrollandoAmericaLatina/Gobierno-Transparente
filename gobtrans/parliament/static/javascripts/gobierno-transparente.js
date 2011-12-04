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
      series: citations_data
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
      series: attendance_data
   });

   // Fancybox
   $("#portfolio a").fancybox({
     'speedIn' : 600,
     'speedOut' : 300, 
     'transitionIn' : 'elastic',
     'transitionOut' : 'elastic',
     'opacity' : true,
     'overlayShow' : false,
     'titlePosition' : 'inside'
   });
});
