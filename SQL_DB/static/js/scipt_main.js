let query;
let money;
let ordered = [];
let purchases = {'2000-02-02': 0}
const div_update = document.getElementById("update");
const div_items = document.getElementById("items_b");
const div_money = document.getElementById("money_spent");
const ctx = document.getElementById('char').getContext('2d');

let myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        datasets: [{
            label: 'Sales Over Two Years',
            data: [
                {x: '2023-01-01', y: 100},
                {x: '2023-06-01', y: 200},
                {x: '2024-01-01', y: 300},
                {x: '2024-06-01', y: 400},
                {x: '2025-01-01', y: 500}
            ],
            fill: true,
            color: 'rgb(45, 100, 245)',
            tension: 0.1
        }]
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
                    text: 'Date'
                },
                min: '2022-01-01',
                max: '2024-03-08'
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Number of items bought'
                },
                max: 4
            }
        }
    }
});


function update_div(contetnt) {
    let display ="";
    purchases = {}
    if (Object.keys(contetnt).length === 0){
        display = "This customer hasn't made any purchase";
    }
    else{
        for (row in contetnt){
            display += `
            <p>Order ID = ${contetnt[row].order_id}</p>
            <p>Product ID = ${contetnt[row].product_id}</p>
            <p>Quantity = ${contetnt[row].quantity}</p>
            <p>Order Date = ${contetnt[row].order_date}</p>
            <p>Status = ${contetnt[row].status}</p>
            <hr>
            `
            if (purchases[contetnt[row].order_date]) {
                purchases[contetnt[row].order_date] += contetnt[row].quantity;
            }
            else {
                purchases[contetnt[row].order_date] = contetnt[row].quantity;
            }
        } 
    }
    div_update.innerHTML = display;
}

function chart_data(dates_quant) {
    to_ret = []
    if (Object.keys(dates_quant).length === 0){
        to_ret = [{x: '2000-02-02', y: 0}]
    }
    else {
        ordered = Object.keys(dates_quant).sort()
        ordered.forEach(function(key){
            to_ret.push({x: key, y: dates_quant[key]})
        })
    }
    return to_ret;
}



function items_money(is_content){
    if (is_content.items === null){
        div_items.innerHTML = "0";
        div_money.innerHTML = "0.00$";
    }
    else {
        div_items.innerHTML = is_content.items;
        div_money.innerHTML = is_content.money + "$";
    }
    
}

function draw_chart() {
    if (myChart) {
        myChart.destroy();
    }
    myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            datasets: [{
                label: 'Quantity',
                data:
                chart_data(purchases)
                ,
                fill: true,
                color: 'rgb(45, 100, 245)',
                tension: 0.1
            }]
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
                        text: 'Date'
                    },
                    min: '2022-01-01',
                    max: '2024-03-08'
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of items bought'
                    },
                    max: 10
                }
            }
        }
    });
}


document.querySelectorAll(".SQL_query").forEach(button => {
    button.addEventListener("click", function() {
        const number = this.getAttribute("data-number");
        Promise.all([
            fetch(`http://127.0.0.1:8000/dashboard/data/orders_one${number}`).then(response => response.json()),
            fetch(`http://127.0.0.1:8000/dashboard/data/money${number}`).then(response => response.json())
        ])
        .then(([query_data, money_data]) => {
            query = query_data;
            update_div(query);

            money = money_data;
            items_money(money);

            draw_chart()
        })
        .catch(error => console.error("Fetch error:", error));
    })
});
