import plotly.graph_objects as go
import pandas as pd
import statsmodels.api as sm



def create_figure(title):

    fig = go.Figure().update_layout(template ="plotly_white", title = title, title_x = 0.5, title_y = 0.95, title_font_weight = 600)
    fig.update_layout(width = 800, height = 500)

    return fig


def create_coefficient_dataframe(res):

    df = pd.DataFrame(index = list(res.params.to_dict().keys())[1:])

    df["coef"] = res.params
    df["ci_low"], df["ci high"] = res.conf_int()[0], res.conf_int()[1]

    df["err_left"], df["err_right"] = df["coef"] - df["ci_low"], df["ci high"] - df["coef"]
    df["pval"] = res.pvalues

    return df



def touch_up_figure(fig):

    fig.update_layout(margin=dict(t=50, b=120, l=200, r=60))
    fig.update_layout(margin = dict(autoexpand = False))
    fig.update_layout(paper_bgcolor = "#FFFFFF")
    fig.update_layout(plot_bgcolor = "#FFFFFF")
    fig.update_layout(font_family = "Garamond", font_weight = 1000, font_size = 19)
    fig.update_yaxes(tickfont = dict(size = 15, weight = 600))
    fig.update_xaxes(title_font = dict(size = 17), title_text = "Coefficient")
    fig.update_layout(legend2 = dict(orientation = "h", y = -0.2, x = 0.375, font_color = "#9C2225"))
    fig.update_layout(title_font = dict(size = 20))



def plot_coefficient_dataframe(df, fig):
    
    for index, row in df.iterrows():

        if row["pval"] < 0.05:
            color = "#9C2225"

        else:
            color = "#012F68"


        fig.add_trace(
            go.Scatter(
                x=[row["coef"]], 
                y=[index.split("(")[0][:-1]],
                mode = "markers",
                error_x = dict(
                    type="data",
                    symmetric = False,
                    array = [row["err_left"]],
                    arrayminus = [row["err_right"]],
                    width = 6,
                    thickness = 3),
                showlegend = False,
                line = dict(
                    width = 10, 
                    color = color),
                name = index.split("(")[0][:-1],
                legend = "legend1"))


    fig.add_trace(
        go.Scatter(
            x=[None], 
            y = [None],
            mode = "markers",
            name = "Significant",
            marker = dict(color = "#9C2225"),
            legend = "legend2",
            showlegend=True,
        )
    )
        

    fig.add_vline(
        x=0,
        line = dict(width = 3, dash = "dash"),
        opacity = 0.5,
        annotation_text = "Null",
        annotation_position = "top",
        annotation_font = dict(size = 15)
    )


    fig.update_yaxes(autorange = "reversed")


    touch_up_figure(fig)
   


def main():

    results = sm.load("regressions/regression_results.pickle")
    coefficient_df = create_coefficient_dataframe(results)
    
    fig = create_figure("")
    plot_coefficient_dataframe(coefficient_df, fig)

    fig.show(renderer="browser")

main()