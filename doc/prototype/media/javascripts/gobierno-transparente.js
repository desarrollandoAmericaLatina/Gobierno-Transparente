/*
 Gobierno Transparente
*/
var citations;
var attendance;

$(document).ready(function() {
  // Citations
  options =  {
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
   }
  citations = new Highcharts.Chart(options);

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
         name: 'faltca',
         data: [8, 22, 10, 10, 48, 50, 38, 72, 2, 456, 4]
      }, {
         name: 'citaciones',
         data: [62, 557, 1267, 1044, 1987, 1721, 1696, 1882, 914, 2317, 463]
      }, {
         name: 'pasajes',
         data: [0, 0, 14, 12, 8, 0, 40, 32, 14, 48, 4]
      }, {
         name: 'licencias',
         data: [4, 42, 126, 150, 285, 253, 342, 354, 164, 349, 75]
      }, {
         name: 'asist',
         data: [46, 525, 1251, 1022, 1923, 1645, 1644, 1782, 908, 1843, 459]
      }]
   });

   // Personalized Graphs
   //

   $.each(['best1', 'best2', 'best3', 'worst1', 'worst2', 'worst3'], function(index, value) {
      options.chart.renderTo = value + "_chart";
      alert(options.chart.renderTo);
      // options.series = $.ajax(...)
      parameterized = new Highcharts.Chart(options);
   });

   // Fancybox
   $("a.lightbox").fancybox({
     'speedIn' : 600,
     'speedOut' : 300, 
     'transitionIn' : 'elastic',
     'transitionOut' : 'elastic',
     'opacity' : true,
     'overlayShow' : false,
     'titlePosition' : 'inside'
   });
});
