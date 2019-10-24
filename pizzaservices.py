import sqlite3


class PizzaServices:

    def __init__(self):
        self.connection = sqlite3.connect("pizza-190807A.sqlite")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def do_query(self, query, parameters=None):
        crs = self.connection.cursor()
        if parameters:
            crs.execute(query, parameters)
        else:
            crs.execute(query)
        return crs.fetchall()

    def customers(self):
        return self.do_query("select * from customer")

    def crusts(self):
        return self.do_query("select * from crust")

    def invoices(self):
        return self.do_query("select * from invoice")

    def pizzas(self):
        return self.do_query("select * from crust")

    def pizzaToppings(self):
        return self.do_query("select * from pizzaTopping")

    def sauces(self):
        return self.do_query("select * from sauce")

    def customer_invoices(self, cust):
        return self.do_query("select * from invoice where customerId = " + str(cust))

    def invoice_pizzas(self, inv):
        return self.do_query("select * from pizza where invoiceId = " + str(inv))

    def pizza_pizzaToppings(self, piz):
        return self.do_query("select * from pizzaTopping where pizzaId = " + str(piz))

    def pizzatoppings_pizza(self, piz):
        return self.do_query("select * from topping join pizzaTopping pT on topping.toppingId = pT.toppingId where pizzaId = " + str(piz))

    def invoices_for_customer(self, customer_id):
        """
        :param customer_id:  Primary key value identifying a customer
        :return: A list of rows from the invoice table for invoices for that customer
        """
        cmd = "select * from invoice where customerId = ?"
        return self.do_query(cmd, [customer_id])

    def pizzas_for_invoice(self, invoice_id):
        """
        :param invoice_id: Primary key value identifying an invoice
        :return: A list of rows from the pizza table for pizzas on that invoice
        """
        cmd = "select * from pizza where invoiceId = ?"
        return self.do_query(cmd, [invoice_id])

    def crust_for_id(self, crust_id):
        """
        :param crust_id: Primary key value identifying a crust
        :return: The row of data for that crust id.
                None if the crust id is invalid
        """
        lst = self.do_query(
            "select * from crust where crustId = ?",
            [crust_id])
        if len(lst) != 1:
            return None
        else:
            return lst[0]

    def sauce_for_id(self, sauce_id):
        """
        :param sauce_id: Primary key value identifying a sauce
        :return:  The row of data for that sauce id
            None if the sauce id is invalid
        """
        lst = self.do_query(
            "select * from sauce where sauceId = ?",
            [sauce_id])
        if len(lst) != 1:
            return None
        else:
            return lst[0]

    def toppings_for_pizza(self, pizza_id):
        """
        :param pizza_id:  Primary key value identifying a pizza
        :return: A list of rows from the topping table for toppings that appear on that pizza
        """
        cmd = """
            select topping.*
            from topping, pizzaTopping
            where pizzaTopping.toppingId = topping.toppingId and pizzaTopping.pizzaId = ?
        """
        return self.do_query(cmd, [pizza_id])