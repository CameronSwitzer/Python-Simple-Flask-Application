from flask import Flask, render_template
from pizzaservices import PizzaServices

app = Flask(__name__)


@app.route('/')
def first_page():
    return render_template("front_page.html")


@app.route('/part1')
def part_1():
    with PizzaServices() as ps:
        customers = ps.customers()
        return render_template("part1.html", customers=customers)


@app.route('/part2')
def part_2():
    with PizzaServices() as ps:
        toppings = ps.do_query(
            "select distinct name, price, count(pT.toppingId), (price * count(pT.toppingId)) total "
            "from topping join pizzaTopping pT on topping.toppingId = pT.toppingId "
            "group by pT.toppingId order by total desc")
        return render_template("part2.html", toppings=toppings)


@app.route('/part3')
def part_3():
    data_table = []
    with PizzaServices() as ps:
        customers = ps.customers()
        for customer in customers:
            customer_total = 0
            invoices = ps.invoices_for_customer(customer[0])
            for invoice in invoices:
                pizzas = ps.pizzas_for_invoice(invoice[0])
                for pizza in pizzas:
                    crust = ps.crust_for_id(pizza[1])
                    sauce = ps.sauce_for_id(pizza[2])
                    toppings = ps.toppings_for_pizza(pizza[0])
                    toppings_cost = sum([tp[2] for tp in toppings])
                    total = crust[2] + sauce[2] + toppings_cost
                    discounted_total = (1 - pizza[3]) * total
                    customer_total += discounted_total
            data_table.append((customer[1], customer[2], customer_total))
    sorted_data = sorted(data_table, key=lambda x: x[2])
    sorted_data.reverse()
    data = []
    for i in range(5):
        data.append(sorted_data[i])
    return render_template("part3.html", data=data)


if __name__ == '__main__':
    app.run()
