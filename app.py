from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add_expense():

    if request.method == "POST":

        expense_id = request.form["expense_id"]
        expense_date = request.form["expense_date"]
        category = request.form["category"]
        description = request.form["description"]
        amount = request.form["amount"]

        file = open("expenses.txt", "a")
        file.write(expense_id + "," + expense_date + "," + category + "," + description + "," + amount + "\n")
        file.close()

        message = "Expense Added Successfully"

        return render_template("add_expense.html", message=message)

    return render_template("add_expense.html")

@app.route("/view")
def view_expense():

    expenses = []

    file = open("expenses.txt", "r")

    for line in file:

        expense_id, expense_date, category, description, amount = line.strip().split(",")

        expenses.append(
            {
                "expense_id": expense_id,
                "expense_date": expense_date,
                "category": category,
                "description": description,
                "amount": amount
            }
        )

    file.close()

    return render_template("view_expense.html", expenses=expenses)

@app.route("/search", methods=["GET", "POST"])
def search_expense():

    expenses = []

    if request.method == "POST":

        search = request.form["search"]
        value = request.form["value"].strip().lower()

        file = open("expenses.txt", "r")

        for line in file:

            expense_id, expense_date, category, description, amount = line.strip().split(",")

            if search == "id":

                if expense_id == value:

                    expenses.append(
                        {
                            "expense_id": expense_id,
                            "expense_date": expense_date,
                            "category": category,
                            "description": description,
                            "amount": amount
                        }
                    )

            elif search == "date":

                if expense_date.lower() == value:

                    expenses.append(
                        {
                            "expense_id": expense_id,
                            "expense_date": expense_date,
                            "category": category,
                            "description": description,
                            "amount": amount
                        }
                    )

            elif search == "category":

                if category.lower() == value:

                    expenses.append(
                        {
                            "expense_id": expense_id,
                            "expense_date": expense_date,
                            "category": category,
                            "description": description,
                            "amount": amount
                        }
                    )

        file.close()

    return render_template("search_expense.html", expenses=expenses)

@app.route("/modify", methods=["GET", "POST"])
def modify_expense():

    message = ""

    if request.method == "POST":

        expense_id = request.form["expense_id"].strip()
        expense_date = request.form["expense_date"].strip()
        category = request.form["category"].strip()
        description = request.form["description"].strip()
        amount = request.form["amount"].strip()

        file = open("expenses.txt", "r")

        expenses = []

        found = False

        for line in file:

            current_id, current_date, current_category, current_description, current_amount = line.strip().split(",")

            if current_id == expense_id:

                found = True

                expenses.append(
                    expense_id + "," +
                    expense_date + "," +
                    category + "," +
                    description + "," +
                    amount + "\n"
                )

            else:

                expenses.append(line)

        file.close()

        file = open("expenses.txt", "w")

        for expense in expenses:
            file.write(expense)

        file.close()

        if found:
            message = "Expense Modified Successfully"
        else:
            message = "Expense Not Found"

    return render_template("modify_expense.html", message=message)

@app.route("/delete", methods=["GET", "POST"])
def delete_expense():

    message = ""

    if request.method == "POST":

        expense_id = request.form["expense_id"].strip()

        file = open("expenses.txt", "r")

        expenses = []

        found = False

        for line in file:

            current_id, expense_date, category, description, amount = line.strip().split(",")

            if current_id == expense_id:

                found = True
                continue

            else:

                expenses.append(line)

        file.close()

        file = open("expenses.txt", "w")

        for expense in expenses:

            file.write(expense)

        file.close()

        if found:

            message = "Expense Deleted Successfully"

        else:

            message = "Expense Not Found"

    return render_template("delete_expense.html", message=message)

@app.route("/total")
def total_expense():

    total = 0

    file = open("expenses.txt", "r")

    for line in file:

        expense_id, expense_date, category, description, amount = line.strip().split(",")

        total = total + float(amount)

    file.close()

    return render_template("total_expense.html", total=total)


if __name__ == "__main__":
    app.run(debug=True)
    