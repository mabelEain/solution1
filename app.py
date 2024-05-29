from flask import Flask, render_template, request
import csv

app = Flask(__name__)
referral_dict = {}
referral_emails = []


# read csv data into dict
def get_csv_data():
    try:
        with open('client.csv', mode='r') as file:
            data = csv.reader(file)
            rows = list(data)

            for row in rows[1:]:
                if row[1] == '':
                    row[1] = 'null'
                referral_dict[row[0]] = row[1]
    except FileNotFoundError as e:
        print("Exception occurred: {}".format(e))


get_csv_data()


# route to check referral email via user input 
@app.route("/", methods=["GET", "POST"])
def index():
    global referral_emails
    print(request.method)
    error = None
    try:
        if request.method == "POST":
            email = request.form["email"]
            # print(email)
            referral_emails = get_referral_email(email)
            if len(referral_emails) == 0:
                error = "Email Not Found"
    except Exception as e:
        print("Exception occurred: {}".format(e))
    return render_template("index.html", emails=referral_emails, error= error)


# check referral emails and return
def get_referral_email(email):
    related_values = []
    if email != '' and email in referral_dict:
        values = [key for key in referral_dict if referral_dict[key] == email]
        # print(values)
        related_values.append(email)
        for key, value in referral_dict.items():
            if value in values:
                related_values.append(key)
            elif key in values:
                related_values.append(key)

        print(related_values)
    else:
        return []
    return related_values


if __name__ == "__main__":
    app.run(debug=True, port=5001)
