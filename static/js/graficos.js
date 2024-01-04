Highcharts.chart('grafico-hinchas', {
  chart: {
    plotBackgroundColor: null,
    plotBorderWidth: null,
    plotShadow: false,
    type: 'pie'
  },
  title: {
    text: 'Gráfico de hinchas por deporte',
    align: 'left'
  },
  tooltip: {
    pointFormat: '{series.name}: <b>{point.y}</b>'
  },
  accessibility: {
    point: {
      valueSuffix: '%'
    }
  },
  plotOptions: {
    pie: {
      allowPointSelect: true,
      cursor: 'pointer',
      dataLabels: {
        enabled: true,
        format: '<b>{point.name}</b>: {point.y}'
      }
    }
  },
  series: [{
    name: 'Hinchas',
    colorByPoint: true,
    data: []
  }]
});

Highcharts.chart('grafico-artesanos', {
  chart: {
    plotBackgroundColor: null,
    plotBorderWidth: null,
    plotShadow: false,
    type: 'pie'
  },
  title: {
    text: 'Gráfico de artesanos por tipo',
    align: 'left'
  },
  tooltip: {
    pointFormat: '{series.name}: <b>{point.y}</b>'
  },
  accessibility: {
    point: {
      valueSuffix: '%'
    }
  },
  plotOptions: {
    pie: {
      allowPointSelect: true,
      cursor: 'pointer',
      dataLabels: {
        enabled: true,
        format: '<b>{point.name}</b>: {point.y}'
      }
    }
  },
  series: [{
    name: 'Artesanos',
    colorByPoint: true,
    data: []
  }]
});

fetch("http://127.0.0.1:5000/get-hinchas-tipo")
  .then((response) => response.json())
  .then((hinchasData) => {
    let hinchas = [];
    for (let hincha of hinchasData) {
      hinchas.push({
        name: capitalize(hincha["tipo_hincha"]), y: hincha["total"]
      });
    }
    let chart = Highcharts.charts.find(
      (chart) => chart && chart.renderTo.id === "grafico-hinchas"
    );
    chart.update({
      series: [
        {
          data: hinchas,
        },
      ],
    });
  })
  .catch((error) => console.error("Error:", error));


fetch("http://127.0.0.1:5000/get-artesanos-tipo")
  .then((response) => response.json())
  .then((artesanosData) => {
    let artesanos = [];
    for (let artesano of artesanosData) {
      artesanos.push({
        name: capitalize(artesano["tipo_artesano"]), y: artesano["total"]
      });
    }
    const chart = Highcharts.charts.find(
      (chart) => chart && chart.renderTo.id === "grafico-artesanos"
    );

    chart.update({
      series: [
        {
          data: artesanos,
        },
      ],
    });
  })
  .catch((error) => console.error("Error:", error));

function capitalize(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}