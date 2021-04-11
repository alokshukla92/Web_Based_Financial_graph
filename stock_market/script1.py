from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/plot/')
def plot():
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    start = datetime.datetime(2020, 7, 1)
    end = datetime.datetime(2020, 9, 30)

    df = data.DataReader(name = "GOOG", data_source = "yahoo", start = start, end = end)
    df

    def status(c, o):
        if c > o:
            value = "increase"
        elif c < o:
            value = "decrease"
        else:
            value = "equal"
        return value

    df["Status"] = [status(c, o) for c, o in zip(df.Close, df.Open)]

    df["Middle"] = (df.Open + df.Close)/2
    df["Height"] = abs(df.Close - df.Open)

    p = figure(x_axis_type = "datetime", width = 1000, height = 500, title = "CandleStick Chart")

    hours_12 = 12 * 60 * 60 * 1000 ## for milliseconds

    p.segment(df.index, df.High, df.index, df.Low, color = "black")


    p.rect(df.index[df.Status == "increase"], df.Middle[df.Status == "increase"],
           hours_12, df.Height[df.Status == "increase"],
           fill_color = "#00cc00", line_color = "black")

    p.rect(df.index[df.Status == "decrease"], df.Middle[df.Status == "decrease"],
           hours_12, df.Height[df.Status == "decrease"],
           fill_color = "#ff1a1a", line_color = "black")

    script1, div1 = components(p)
    cdn_js = CDN.js_files[0]
    return render_template("plot.html", script1 = script1, div1 = div1,
                           cdn_js = cdn_js)



@app.route('/about/')
def about():
    return render_template("about.html")
if __name__=="__main__":
    app.run(debug=True)
