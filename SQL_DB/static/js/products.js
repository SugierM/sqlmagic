const ctx1 = document.getElementById('chart_1').getContext('2d');
const ctx2 = document.getElementById('chart_2').getContext('2d');
const ctxall = document.getElementById('chart_all').getContext('2d');
let id1, id2, id_all;
let kid1, kid2, kid_all;
let temp = 0;
Promise.all([
    fetch('http://127.0.0.1:8000/dashboard/data/sales1').then(response => response.json()),
    fetch('http://127.0.0.1:8000/dashboard/data/sales2').then(response => response.json()),
    fetch('http://127.0.0.1:8000/dashboard/data/quant1').then(response => response.json()),
    fetch('http://127.0.0.1:8000/dashboard/data/quant2').then(response => response.json()),
]).then(([first, second, third, fourth])=> {
    id1 = parse_data(first);
    id2 = parse_data(second);
    kid1 = parse_data(third);
    kid2 = parse_data(fourth);
    id_all = add_ids(id1, id2);
    kid_all = add_ids(kid1, kid2);
    draw_chart(ctx1, kid2, kid1, 'Units sold', 130);
    draw_chart(ctx2, id2, id1, 'Sell value $', 50000);
    draw_chart(ctxall, id_all, id_all, 'Products together', 75000)
}).catch(error => console.error("Fetch error:", error));

function parse_data(data) {
    v = Object.keys(data[0])[0]
    k = Object.keys(data[0])[1]
    to_ret = Array();
        for(row in data){
            to_ret.push({x: data[row][k], y: data[row][v]})
        }
    return to_ret;
}
// p_id1 has all dates needed
function add_ids(one, two){
    to_ret = Array();
    for (row in one){
        temp = Number(one[row].y) + Number(two[row].y);
        to_ret.push({x: one[row].x, y: temp});
    }
    return to_ret;
}


function draw_chart(ctx, draw_data, draw_data2, prompt1, max, fillament, fillament2) {
    new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Prodcut 2',
                data: draw_data,
                fill: true,
                borderColor: fillament,
                tension: 0.4
            },
            {
                label: 'Product 1',
                data: draw_data2,
                fill: true,
                borderColor: fillament2,
                tension: 0.4
            },
        ]
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        tooltipFormat: 'DD T',
                        unit: 'year'
                    },
                    title: {
                        display: true,
                        text: prompt1
                    },
                    min: '2022-03-01',
                    max: '2024-03-11'
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: false,
                        text: 'Income each month $'
                    },
                    max : max,
                }
            }
        }
    });
}
