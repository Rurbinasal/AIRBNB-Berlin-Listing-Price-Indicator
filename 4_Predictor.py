import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import joblib
import math
from currency_converter import CurrencyConverter
from datetime import date

external_stylesheets = ['https://codepen.io/rurbinasal/pen/QWNdogQ.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
server = app.server

# Import and definition of variables
curr = CurrencyConverter()
data_options = {
    'amsterdam': ['2020-03-14', '2020-06-15'],
    'berlin': ['2020-03-17'],
    'paris': ['2020-03-16']
}

# Define overall style of web app and maps
style = {'padding': '1.5em', 'maxWidth': '960px', 'margin': 'auto'}
px.defaults.template = "simple_white"  # 'ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff', 'ygridoff', 'gridon', 'none'
px.defaults.color_continuous_scale = ["#00A699", "#50D6B9", "#FF9A7F", "#FF5A5F"]  # ["#50D6B9", "#00A699", "#FF9A7F", "#FF5A5F"] #"burgyl"
px.defaults.color_discrete_sequence = ["#767676", "#00A699", "#FF5A5F", "#F9C70C", "#FC642D", "#484848"]
px.defaults.width = 900
px.defaults.height = 600

# Import data for Berlin 2020-03-17
dataset_loc = 'berlin'
dataset_date = '2020-03-17'
data = joblib.load(f"../data/{dataset_loc}_{dataset_date}/APP_data_engineered.pkl")
model = joblib.load(f"../data/{dataset_loc}_{dataset_date}/APP_best_model.pkl")
preprocessor = joblib.load(f"../data/{dataset_loc}_{dataset_date}/APP_preprocessor.pkl")
X_test = joblib.load(f"../data/{dataset_loc}_{dataset_date}/APP_X_test.pkl")
MAPE_median = joblib.load(f"../data/{dataset_loc}_{dataset_date}/APP_MAPE_median.pkl")
zipcodes = joblib.load(f"../data/{dataset_loc}_{dataset_date}/APP_zipcode.pkl")

# Import data for Amsterdam 2020-03-14
dataset_loc2 = 'amsterdam'
dataset_date2 = '2020-03-14'
data2 = joblib.load(f"../data/{dataset_loc2}_{dataset_date2}/APP_data_engineered.pkl")
model2 = joblib.load(f"../data/{dataset_loc2}_{dataset_date2}/APP_best_model.pkl")
preprocessor2 = joblib.load(f"../data/{dataset_loc2}_{dataset_date2}/APP_preprocessor.pkl")
X_test2 = joblib.load(f"../data/{dataset_loc2}_{dataset_date2}/APP_X_test.pkl")
MAPE_median2 = joblib.load(f"../data/{dataset_loc2}_{dataset_date2}/APP_MAPE_median.pkl")
zipcodes2 = joblib.load(f"../data/{dataset_loc2}_{dataset_date2}/APP_zipcode.pkl")

# Import data for Paris 2020-03-16
dataset_loc3 = 'paris'
dataset_date3 = '2020-03-16'
data3 = joblib.load(f"../data/{dataset_loc3}_{dataset_date3}/APP_data_engineered.pkl")
model3 = joblib.load(f"../data/{dataset_loc3}_{dataset_date3}/APP_best_model.pkl")
preprocessor3 = joblib.load(f"../data/{dataset_loc3}_{dataset_date3}/APP_preprocessor.pkl")
X_test3 = joblib.load(f"../data/{dataset_loc3}_{dataset_date3}/APP_X_test.pkl")
MAPE_median3 = joblib.load(f"../data/{dataset_loc3}_{dataset_date3}/APP_MAPE_median.pkl")
zipcodes3 = joblib.load(f"../data/{dataset_loc3}_{dataset_date3}/APP_zipcode.pkl")

zipcode_options = {
    'berlin': zipcodes,
    'amsterdam': zipcodes2,
    'paris': zipcodes3
}

app.layout = html.Div([
    dcc.Markdown('# Airbnb Pricing Indicator'),
    dcc.Tabs(id='tabs', value='tab-intro', children=[
        dcc.Tab(id='tab-intro', label='Description', children=[
            html.Div([
                html.Img(src=app.get_asset_url('berlin_image.png'), height=540, width=960),

                dcc.Markdown("""
        Airbnb is the leading online platform for vacation rentals for travelers - primarily homestays - 
        as an alternative to traditional hotel or hostel stays. While they do not own or host themselves,
        they instead act as an intermediary broker.

        Airbnb does not publicly publish booking data as this presents one of its core assets.
        Users instead receive a pricing indication as part of the listing creation process.
        Hence it is difficult for individuals to estimate a good listing price before account creation.

        This project aims at providing a tool giving a non-binding and assumption-based upfront 
        indication for listing pricing in Berlin, taking into account 24 features the user can enter
        via the "pricing prediction" tab. Additionally, listings in Berlin can be explored on an
        interactive map via the "map" tab.
    """),
            ])
        ]),
        dcc.Tab(id='tab-predict', label='Pricing Indicator',
                children=[
            html.Div([
                # Selection of dataset (default = Berlin, 2020-03-17)
                html.Div([
                    dcc.Markdown('###### Please first select city and date (due to COVID impact, for now the latest option is March 2020):'),
                    dcc.Dropdown(
                        id='city',
                        options=[{'label': city.upper(), 'value': city} for city in data_options.keys()],
                        value='amsterdam'
                    ),
                    dcc.Dropdown(
                        id='date'
                    ),
                ], style=style),

                dcc.Markdown("""
                    Use the controls below to enter the specifics of your listing.
                """),

            # Zipcode:
                html.Div([
                    dcc.Markdown('###### Zipcode:'),
                    dcc.Dropdown(
                        id='zipcode'
                    ),
                ], style=style),
            # Property type:
                html.Div([
                    dcc.Markdown('###### Property type:'),
                    dcc.Dropdown(
                        id='property_type',
                        options=[
                            {'label': "Apartment", 'value': "Apartment"},
                            {'label': "House", 'value': "House"},
                            {'label': "Boutique hotel", 'value': "Boutique hotel"},
                            {'label': "Secondary unit", 'value': "Secondary unit"},
                            {'label': "Bed and breakfast", 'value': "Bed and breakfast"},
                            {'label': "Unique space", 'value': "Unique space"},
                        ],
                        value="Apartment"
                    ),
                ], style=style),
            # Room type:
                html.Div([
                    dcc.Markdown('###### Room type:'),
                    dcc.Dropdown(
                        id='room_type',
                        options=[
                            {'label': "Entire home/apt", 'value': "Entire home/apt"},
                            {'label': "Private room", 'value': "Private room"},
                            {'label': "Shared room", 'value': "Shared room"},
                            {'label': "Hotel room", 'value': "Hotel room"}
                        ],
                        value="Entire home/apt"
                    ),
                ], style=style),
            # Accommodates:
                html.Div([
                    dcc.Markdown('###### Accommodates:'),
                    dcc.Slider(
                        id='accommodates',
                        min=1,
                        max=10,
                        step=1,
                        value=2,
                        marks={n: str(n) for n in range(1, 11, 1)}
                    ),
                ], style=style),

                html.Div([
                    dcc.Markdown('###### Bedrooms:'),
                    dcc.Slider(
                        id='bedrooms',
                        min=0.5,
                        max=7,
                        step=0.5,
                        value=1,
                        marks={n: str(n) for n in [0.5, 1, 2, 3, 4, 5, 6, 7]}
                    ),
                ], style=style),

                html.Div([
                    dcc.Markdown('###### Beds:'),
                    dcc.Slider(
                        id='beds',
                        min=0.5,
                        max=7,
                        step=0.5,
                        value=1,
                        marks={n: str(n) for n in [0.5, 1, 2, 3, 4, 5, 6, 7]}
                    ),
                ], style=style),

                html.Div([
                    dcc.Markdown('###### Bathrooms:'),
                    dcc.Slider(
                        id='bathrooms_log',
                        min=0.5,
                        max=7,
                        step=0.5,
                        value=1,
                        marks={n: str(n) for n in [0.5, 1, 2, 3, 4, 5, 6, 7]}
                    ),
                ], style=style),

                html.Div([
                    dcc.Markdown('###### Minimum nights:'),
                    dcc.Input(
                        id='minimum_nights_sqrt',
                        placeholder="Enter a number...",
                        type='number',
                        value=1
                    )
                ], style=style),
            # Maximum nights
                html.Div([
                    dcc.Markdown('###### Maximum nights:'),
                    dcc.Input(
                        id='maximum_nights',
                        placeholder="Enter a number...",
                        type='number',
                        value=1125
                    )
                ], style=style),
            # Cancellation policy:
                html.Div([
                    dcc.Markdown('###### Cancellation policy:'),
                    dcc.Dropdown(
                        id='cancellation_policy',
                        options=[
                            {'label': "flexible", 'value': "flexible"},
                            {'label': "moderate", 'value': "moderate"},
                            {'label': "strict", 'value': "strict"},
                            {'label': "super strict", 'value': "super_strict"}
                        ],
                        value="flexible"
                    ),
                ], style=style),
            # Instant bookable:
                html.Div([
                    dcc.Markdown('###### Will you make your listing available for instant booking?:'),
                    dcc.RadioItems(
                        id='instant_bookable',
                        options=[
                            {'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0},
                        ],
                        value=0
                    ),
                ], style=style),

                html.Div([
                    dcc.Markdown('###### Do you already have active listings on Airbnb apart from the one in question?:'),
                    dcc.Slider(
                        id='calc_host_lst_count_sqrt_log',
                        min=0,
                        max=7,
                        step=1,
                        value=0,
                        marks={n: str(n) for n in [0, 1, 2, 3, 4, 5, 6, 7]}
                    ),
                ], style=style),

                html.Div([
                    dcc.Markdown('###### If so, are you already a superhost?:'),
                    dcc.RadioItems(
                        id='host_is_superhost',
                        options=[
                            {'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0},
                        ],
                        value=0
                    ),
                ], style=style),

                html.Div([
                    dcc.Markdown('###### Will you offer a weekly or monthly discount?:'),
                    dcc.Slider(
                        id='wk_mth_discount',
                        min=0,
                        max=0.5,
                        step=0.05,
                        value=0,
                        marks={n: str(int(n*100))+"%" for n in [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]}
                    ),
                ], style=style),

                html.Div([
                    dcc.Markdown('###### Show price for # of guests included:'),
                    dcc.Slider(
                        id='guests_included_calc',
                        min=1,
                        max=9,
                        step=1,
                        value=2,
                        marks={n: str(n) for n in range(1, 9, 1)}
                    ),
                ], style=style),

                html.Div([
                    dcc.Markdown('###### How much occupancy are you targeting? (please consider local laws):'),
                    dcc.Slider(
                        id='occupancy_rate',
                        min=0,
                        max=1,
                        step=0.05,
                        value=0.3,
                        marks={n: str(int(n*100))+"%" for n in [0,  0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]}
                    ),
                ], style=style),

                dcc.Markdown("""
                Optional: Select amenities that you provide (defaults are given)
            """),

                html.Div([
                    dcc.Markdown('###### Essentials:'),
                    dcc.RadioItems(
                        id='am_essentials',
                        options=[
                            {'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0},
                        ],
                        value=1
                    ),
                ], style=style),

                html.Div([
                    dcc.Markdown('###### Balcony:'),
                    dcc.RadioItems(
                        id='am_balcony',
                        options=[
                            {'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0},
                        ],
                        value=0
                    ),
                ], style=style),

                html.Div([
                    dcc.Markdown('###### Breakfast:'),
                    dcc.RadioItems(
                        id='am_breakfast',
                        options=[
                            {'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0},
                        ],
                        value=0
                    ),
                ], style=style),

                html.Div([
                    dcc.Markdown('###### Child Friendly:'),
                    dcc.RadioItems(
                        id='am_child_friendly',
                        options=[
                            {'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0},
                        ],
                        value=0
                    ),
                ], style=style),

                html.Div([
                    dcc.Markdown('###### Elevator:'),
                    dcc.RadioItems(
                        id='am_elevator',
                        options=[
                            {'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0},
                        ],
                        value=0
                    ),
                ], style=style),

                html.Div([
                    dcc.Markdown('###### Pets allowed:'),
                    dcc.RadioItems(
                        id='am_pets_allowed',
                        options=[
                            {'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0},
                        ],
                        value=0
                    ),
                ], style=style),

                html.Div([
                    dcc.Markdown('###### Private entrance:'),
                    dcc.RadioItems(
                        id='am_private_entrance',
                        options=[
                            {'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0},
                        ],
                        value=0
                    ),
                ], style=style),

                html.Div([
                    dcc.Markdown('###### Smoking allowed:'),
                    dcc.RadioItems(
                        id='am_smoking_allowed',
                        options=[
                            {'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0},
                        ],
                        value=0
                    ),
                ], style=style),

                html.Div([
                    dcc.Markdown('###### TV:'),
                    dcc.RadioItems(
                        id='am_tv',
                        options=[
                            {'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0},
                        ],
                        value=0
                    ),
                ], style=style),

                html.Div([
                    html.Div(id='listing_price'),
                    html.Div(id='price_range'),
                    html.Div(id='yearly_earnings')],
                    style={'fontWeight': 'bold', 'position': 'sticky', 'bottom': 0, 'border': "2px solid #FF5A5F",
                                                         'background-color': "#FFEAEB", 'z-index': 1, 'margin': 30,   # alt. green:"#00A699", red: "#FF5A5F"
                                                         'padding': 15, 'color': "#000000"}),

            ])#, style = {'padding': '1.5em', 'maxWidth': '960px', 'margin': 'auto',
#                             'background-image': html.Div(id='background_img'), 'background-repeat': 'no-repeat',
#                             'background-position': 'right top',
#                             'background-size': '150px 100px'}
        ]),
        dcc.Tab(id='tab-map', label='Map of all Listings', children=[
            html.Div([
#         html.Div([
#             dcc.Markdown('###### Please first select city and date (due to COVID impact, for now the latest option is March 2020):'),
#             dcc.Dropdown(
#                 id='city',
#                 options=[{'label': city.upper(), 'value': city} for city in data_options.keys()],
#                 value='berlin'
#             ),
#             dcc.Dropdown(
#                 id='date'
#             ),
#         ], style=style),

                html.Div([
                    html.Div(id='total_listings')
                ], style=style),

                html.Div([
                    dcc.Graph(id='map_fig')
                ]),

                html.Div([
                    dcc.Markdown('###### Enter listing # to generate URL to listing (if still existing):'),
                    dcc.Input(
                        id='listing_no',
                        placeholder="Enter a number...",
                        type='number',
                        value=40610629
                    )
                ], style=style),

                html.Div(id='listing_url', style={'fontWeight': 'bold'})
            ])
        ]),
    ]),
], style=style)

#@app.callback(Output('tabs-content', 'children'),
#              [Input('tabs', 'value')])
#def render_content(tab):
#    if tab == 'tab-intro': return intro.layout
#    elif tab == 'tab-predict': return predict.layout
#    elif tab == 'tab-map': return map.layout

@app.callback(
    [Output('date', 'options'),
    Output('zipcode', 'options')],
    [Input('city', 'value')])
def set_date_options(selected_city):
    return [{'label': date[:-3], 'value': date} for date in data_options[selected_city]], [{'label': zipcode[4:], 'value': zipcode} for zipcode in zipcode_options[selected_city]]


#@app.callback(
#    Output('background_img', 'value'),
#    [Input('city', 'value')])
#def set_background(selected_city):
#    if selected_city == "berlin":
#        return 'url("/assets/berlin_image.png")'
#    elif selected_city == "amsterdam":
#        return 'url("/assets/amsterdam_image.png")'


@app.callback(
    [Output('date', 'value'),
    Output('zipcode', 'value')],
    [Input('date', 'options'),
     Input('zipcode', 'options')])
def set_cities_value(available_dates, available_zipcodes):
    return available_dates[0]['value'], available_zipcodes[-1]['value']


@app.callback(
#    Output('prediction-content', 'children'),
    [Output('listing_price', 'children'),
    Output('price_range', 'children'),
    Output('yearly_earnings', 'children')],
    [Input('accommodates', 'value'),
     Input('am_balcony', 'value'),
     Input('am_breakfast', 'value'),
     Input('am_child_friendly', 'value'),
     Input('am_elevator', 'value'),
     Input('am_essentials', 'value'),
     Input('am_pets_allowed', 'value'),
     Input('am_private_entrance', 'value'),
     Input('am_smoking_allowed', 'value'),
     Input('am_tv', 'value'),
     Input('bathrooms_log', 'value'),
     Input('bedrooms', 'value'),
     Input('beds', 'value'),
     Input('calc_host_lst_count_sqrt_log', 'value'),
     Input('cancellation_policy', 'value'),
     Input('guests_included_calc', 'value'),
     Input('host_is_superhost', 'value'),
     Input('instant_bookable', 'value'),
     Input('maximum_nights', 'value'),
     Input('minimum_nights_sqrt', 'value'),
     Input('property_type', 'value'),
     Input('room_type', 'value'),
     Input('wk_mth_discount', 'value'),
     Input('zipcode', 'value'),
     Input('occupancy_rate', 'value'),
     Input('city', 'value')])

def predict(accommodates, am_balcony, am_breakfast, am_child_friendly, am_elevator, am_essentials, am_pets_allowed,
            am_private_entrance, am_smoking_allowed, am_tv, bathrooms_log, bedrooms, beds, calc_host_lst_count_sqrt_log,
            cancellation_policy, guests_included_calc, host_is_superhost, instant_bookable, maximum_nights,
            minimum_nights_sqrt, property_type, room_type, wk_mth_discount, zipcode, occupancy_rate, city):

    df = pd.DataFrame(
        columns=X_test.columns,
        data=[[accommodates, am_balcony, am_breakfast, am_child_friendly, am_elevator, am_essentials, am_pets_allowed,
            am_private_entrance, am_smoking_allowed, am_tv, bathrooms_log, bedrooms, calc_host_lst_count_sqrt_log,
            cancellation_policy, guests_included_calc, host_is_superhost, instant_bookable, maximum_nights,
            minimum_nights_sqrt, property_type, room_type, wk_mth_discount, zipcode]]
    )
    df.accommodates_per_bed = accommodates/beds
    df.bathrooms_log = math.log(int(bathrooms_log))
    df.calc_host_lst_count_sqrt_log = math.log(math.sqrt(calc_host_lst_count_sqrt_log+1))
    df.minimum_nights_sqrt = math.sqrt(minimum_nights_sqrt)
    for col in ["am_balcony", "am_breakfast", "am_child_friendly", "am_elevator", "am_essentials",
                "am_pets_allowed", "am_private_entrance", "am_smoking_allowed", "am_tv",
                "host_is_superhost", "instant_bookable"]:
        df[col] = df[col][0]

    if city == 'berlin':
        x_test_prep = preprocessor.transform(df)
        y_pred = model.predict(x_test_prep)
        y_pred_interval = tuple([(round(curr.convert(math.exp(el-el*MAPE_median), 'USD', 'EUR', date=date(2020, 3, 17))),
                                  round(curr.convert(math.exp(el+el*MAPE_median), 'USD', 'EUR', date=date(2020, 3, 17)))) for el in y_pred])
        y_pred_exp = [round(curr.convert(math.exp(el), 'USD', 'EUR', date=date(2020, 3, 17))) for el in y_pred]

    elif city == 'amsterdam':
        x_test_prep = preprocessor2.transform(df)
        y_pred = model2.predict(x_test_prep)
        y_pred_interval = tuple(
            [(round(curr.convert(math.exp(el - el * MAPE_median2), 'USD', 'EUR', date=date(2020, 3, 13))),
              round(curr.convert(math.exp(el + el * MAPE_median2), 'USD', 'EUR', date=date(2020, 3, 13)))) for el in
             y_pred])
        y_pred_exp = [round(curr.convert(math.exp(el), 'USD', 'EUR', date=date(2020, 3, 13))) for el in y_pred]

    elif city == 'paris':
        x_test_prep = preprocessor3.transform(df)
        y_pred = model3.predict(x_test_prep)
        y_pred_interval = tuple(
            [(round(curr.convert(math.exp(el - el * MAPE_median3), 'USD', 'EUR', date=date(2020, 3, 16))),
              round(curr.convert(math.exp(el + el * MAPE_median3), 'USD', 'EUR', date=date(2020, 3, 16)))) for el in
             y_pred])
        y_pred_exp = [round(curr.convert(math.exp(el), 'USD', 'EUR', date=date(2020, 3, 16))) for el in y_pred]

    listing_price = f'Recommended listing price: €{y_pred_exp[0]}'
    price_range = f'Sensible range: €{y_pred_interval[0][0]}-€{y_pred_interval[0][1]}'
    yearly_earnings = f'Potential yearly earnings: €{round(y_pred_exp[0] * 365 * occupancy_rate)} (at occupancy of {int(occupancy_rate * 100)}%, not considering fees)'

    return listing_price, price_range, yearly_earnings


@app.callback(
    Output('listing_url', 'children'),
    [Input('listing_no', 'value')])

def generate_url(listing_no):
    url = f'https://www.airbnb.com/rooms/{listing_no}'
    return url


@app.callback(
    [Output('map_fig', 'figure'),
     Output('total_listings', 'children')],
    [Input('city', 'value')])

def generate_map(city):
# Define map content and layout
    if city == "berlin":
        map_input=data
        zoom=9
    if city == "amsterdam":
        map_input=data2
        zoom=10
    if city == "paris":
        map_input=data3
        zoom=11
    data.price = [round(curr.convert(math.exp(el), 'USD', 'EUR', date=date(2020, 3, 17))) for el in data.price_log]
    map_fig = px.scatter_mapbox(
        map_input,
        lat="latitude",
        lon="longitude",
        color="price",
        size="accommodates",
        size_max=15,
        hover_name="listing_no",
        hover_data={
            "latitude": False,
            "longitude": False,
            "bedrooms": True,
            "price": True,
            "room_type": True,
            "neighbourhood_cleansed": False,
            "occupancy_rate": True,
            "occupancy_rate": ":.2f"
        },
        range_color=[10,200],
        zoom=zoom,
        opacity=0.8,
        mapbox_style="carto-positron")
    total_listings = len(data.price_log)
    return map_fig, dcc.Markdown(f'{total_listings} listings in {city.capitalize()} on {dataset_date}:')


if __name__ == '__main__':
    app.run_server(debug=True)