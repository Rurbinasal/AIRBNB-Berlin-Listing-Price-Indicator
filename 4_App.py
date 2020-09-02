import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
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
    'amsterdam': ['2020-03-14'], #, '2020-07-09'
    'barcelona': ['2020-03-16'],
    'berlin': ['2020-03-17'], #, '2020-06-13'
    'paris': ['2020-03-16']
}

# Define overall style of web app and maps
style = {'padding': '0.5em', 'maxWidth': '960px', 'margin': 'auto'}
px.defaults.template = "simple_white"  # 'ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff', 'ygridoff', 'gridon', 'none'
px.defaults.color_continuous_scale = ["#00A699", "#50D6B9", "#FF9A7F", "#FF5A5F"]  # ["#50D6B9", "#00A699", "#FF9A7F", "#FF5A5F"] #"burgyl"
px.defaults.color_discrete_sequence = ["#767676", "#00A699", "#FF5A5F", "#F9C70C", "#FC642D", "#484848"]
px.defaults.width = 900
px.defaults.height = 600

# Import data for Berlin 2020-03-17
dataset_loc = 'berlin'
dataset_date = '2020-03-17'
data = joblib.load(f"data/{dataset_loc}_{dataset_date}/APP_data_engineered.pkl")
model = joblib.load(f"data/{dataset_loc}_{dataset_date}/APP_best_model.pkl")
preprocessor = joblib.load(f"data/{dataset_loc}_{dataset_date}/APP_preprocessor.pkl")
X_test = joblib.load(f"data/{dataset_loc}_{dataset_date}/APP_X_test.pkl")
MAPE_median = joblib.load(f"data/{dataset_loc}_{dataset_date}/APP_MAPE_median.pkl")
zipcodes = joblib.load(f"data/{dataset_loc}_{dataset_date}/APP_zipcode.pkl")

# Import data for Amsterdam 2020-03-14
dataset_loc2 = 'amsterdam'
dataset_date2 = '2020-03-14'
data2 = joblib.load(f"data/{dataset_loc2}_{dataset_date2}/APP_data_engineered.pkl")
model2 = joblib.load(f"data/{dataset_loc2}_{dataset_date2}/APP_best_model.pkl")
preprocessor2 = joblib.load(f"data/{dataset_loc2}_{dataset_date2}/APP_preprocessor.pkl")
X_test2 = joblib.load(f"data/{dataset_loc2}_{dataset_date2}/APP_X_test.pkl")
MAPE_median2 = joblib.load(f"data/{dataset_loc2}_{dataset_date2}/APP_MAPE_median.pkl")
zipcodes2 = joblib.load(f"data/{dataset_loc2}_{dataset_date2}/APP_zipcode.pkl")

# Import data for Paris 2020-03-16
dataset_loc3 = 'paris'
dataset_date3 = '2020-03-16'
data3 = joblib.load(f"data/{dataset_loc3}_{dataset_date3}/APP_data_engineered.pkl")
model3 = joblib.load(f"data/{dataset_loc3}_{dataset_date3}/APP_best_model.pkl")
preprocessor3 = joblib.load(f"data/{dataset_loc3}_{dataset_date3}/APP_preprocessor.pkl")
X_test3 = joblib.load(f"data/{dataset_loc3}_{dataset_date3}/APP_X_test.pkl")
MAPE_median3 = joblib.load(f"data/{dataset_loc3}_{dataset_date3}/APP_MAPE_median.pkl")
zipcodes3 = joblib.load(f"data/{dataset_loc3}_{dataset_date3}/APP_zipcode.pkl")

# Import data for Barcelona 2020-03-16
dataset_loc4 = 'barcelona'
dataset_date4 = '2020-03-16'
data4 = joblib.load(f"data/{dataset_loc4}_{dataset_date4}/APP_data_engineered.pkl")
model4 = joblib.load(f"data/{dataset_loc4}_{dataset_date4}/APP_best_model.pkl")
preprocessor4 = joblib.load(f"data/{dataset_loc4}_{dataset_date4}/APP_preprocessor.pkl")
X_test4 = joblib.load(f"data/{dataset_loc4}_{dataset_date4}/APP_X_test.pkl")
MAPE_median4 = joblib.load(f"data/{dataset_loc4}_{dataset_date4}/APP_MAPE_median.pkl")
zipcodes4 = joblib.load(f"data/{dataset_loc4}_{dataset_date4}/APP_zipcode.pkl")

zipcode_options = {
    'berlin': zipcodes,
    'amsterdam': zipcodes2,
    'paris': zipcodes3,
    'barcelona': zipcodes4
}

app.layout = html.Div([
    html.Div(className='background', children=[
        html.Img(className='background-img', id='background_img', src=app.get_asset_url('amsterdam_background.png')
                 )]),
    html.Div(
        className='container', children=[
            html.Header(
                html.Div(className='os-header',
                         style={'background-image': 'url(assets/app_icon.png)', 'background-repeat': 'no-repeat',
                                'background-position': 'left', 'background-size': 'contain'},
                         children=[html.Div([dcc.Markdown('# Airbnb Pricing Indicator')], style={'padding-left': '130px'})])
#                html.Div(className='os-header', children=[
#                    html.Div([html.Img(src=app.get_asset_url('app_icon.png'), style={'maxHeight': '100px', 'maxWidth': '100px'})], style={'display': 'inline-block', 'height': '40px'}),
#                    html.Div([dcc.Markdown('# Airbnb Pricing Indicator')], style={'display': 'inline-block', 'maxHeight': '100px', 'maxWidth': '840px', 'margin': 'auto'})
            ),
            html.Main(
            dcc.Tabs(className = 'os-tab-container', children=[
                dcc.Tab(id='tab-intro', label='Description', className = 'os-tab', children=[
                    html.Div([
                        html.Img(src=app.get_asset_url('navigator.png'), style={'width': '100%', 'opacity': 0.3}),
                        html.Div([
                            dcc.Markdown("""
                            ### About Airbnb
                            **Airbnb is the leading online platform for vacation rentals for travelers** - primarily homestays - 
                            as an alternative to traditional hotel or hostel stays. While they do not own or host themselves,
                            they instead act as an intermediary broker.
                            
                            ### Pricing indicator background                    
                            Platforms like Airbnb make it incredibly easy to rent out a place, but it is **not so trivial
                            to figure out how much one could or should actually charge for a listing**. Airbnb does not publicly 
                            publish booking data as this presents one of its core assets. Users instead need to have an 
                            account, create a listing and then receive a pricing indication as part of the listing creation process.
                            Hence it is difficult for individuals to estimate a good listing price upfront.
                            
                            ### Pricing indicator concept                    
                            This project aims at **providing a tool giving a non-binding and assumption-based upfront 
                            indication for listing pricing**, taking into account 24 features the user can enter
                            via the "pricing prediction" tab. Additionally, listings can be explored on an
                            interactive map via the "map" tab. Initially, the focus was on Berlin, but by now several
                            other major European cities have been added.
                            
                            ### About me
                            **I am a Data Scientist and passionate traveller, aiming for a long and exciting future in 
                            the field of data**. This specific project was created as the final capstone during my 
                            three-month Data Scientist Bootcamp at neuefische GmbH in Hamburg. The project is not in
                             any way affiliated with Airbnb and has been carried out with data retrieved at 
                              [Inside Airbnb](http://insideairbnb.com/get-the-data.html). Please feel free 
                            to get in touch or contact me with regard to this tool or other topics.  
                            
                            Github project repo: https://github.com/Rurbinasal/AIRBNB-Berlin-Listing-Price-Indicator  
                            https://linkedin.com/in/mauriciomalzer  
                            https://github.com/Rurbinasal  
                              
                            **Special thanks go to [Jim King](https://github.com/JimKing100)**, whose great [blog post](https://jimking100.github.io/2019-12-08-Post-7/)
                            was key to building a first mock-up of this web application in no time.  
                            """),
                        ], className='content'),
                    ])
                ]),
                dcc.Tab(id='tab-predict', label='Pricing Indicator', className = 'os-tab', children=[
                        html.Div(className='content', children=[
                        # Selection of dataset
                        html.Div([
                            dcc.Markdown('### Please first select a city (analysis currently based on March 2020 to avoid COVID impact):'),
                            dcc.Dropdown(
                                id='city',
                                options=[{'label': city.capitalize(), 'value': city} for city in data_options.keys()],
                                value='amsterdam'
                            ),
                        ]),

                        dcc.Markdown('### Use the controls below to enter the specifics of your listing:'),

                    # Zipcode:
                        html.Div([
                            dcc.Markdown('#### Zipcode:'),
                            dcc.Dropdown(
                                id='zipcode',
                                value='zip_other'
                            ),
                        ]),
                    # Property type:
                        html.Div([
                            dcc.Markdown('#### Property type:'),
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
                        ]),
                    # Room type:
                        html.Div([
                            dcc.Markdown('#### Room type:'),
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
                        ]),
                    # Accommodates:
                        html.Div([
                            dcc.Markdown('#### Accommodates:'),
                            dcc.Slider(
                                id='accommodates',
                                min=1,
                                max=10,
                                step=1,
                                value=2,
                                marks={n: str(n) for n in range(1, 11, 1)}
                            ),
                        ]),

                        html.Div([
                            dcc.Markdown('#### Bedrooms:'),
                            dcc.Slider(
                                id='bedrooms',
                                min=0.5,
                                max=7,
                                step=0.5,
                                value=1,
                                marks={n: str(n) for n in [0.5, 1, 2, 3, 4, 5, 6, 7]}
                            ),
                        ]),

                        html.Div([
                            dcc.Markdown('#### Beds:'),
                            dcc.Slider(
                                id='beds',
                                min=0.5,
                                max=7,
                                step=0.5,
                                value=1,
                                marks={n: str(n) for n in [0.5, 1, 2, 3, 4, 5, 6, 7]}
                            ),
                        ]),

                        html.Div([
                            dcc.Markdown('#### Bathrooms:'),
                            dcc.Slider(
                                id='bathrooms_log',
                                min=0.5,
                                max=7,
                                step=0.5,
                                value=1,
                                marks={n: str(n) for n in [0.5, 1, 2, 3, 4, 5, 6, 7]}
                            ),
                        ]),

                        html.Div([
                            dcc.Markdown('#### Minimum nights:'),
                            dcc.Input(
                                id='minimum_nights_sqrt',
                                placeholder="Enter a number...",
                                type='number',
                                value=1
                            )
                        ]),
                    # Maximum nights
                        html.Div([
                            dcc.Markdown('#### Maximum nights:'),
                            dcc.Input(
                                id='maximum_nights',
                                placeholder="Enter a number...",
                                type='number',
                                value=1125
                            )
                        ]),
                    # Cancellation policy:
                        html.Div([
                            dcc.Markdown('#### Cancellation policy:'),
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
                        ]),
                    # Instant bookable:
                        html.Div([
                            dcc.Markdown('#### Will you make your listing available for instant booking?:'),
                            daq.BooleanSwitch(
                                id='instant_bookable',
                                on=False,
                                color="#00A699",
                                style={'width': '8%', 'padding-right': '92%'}
                            ),
                        ]),

                        html.Div([
                            dcc.Markdown('#### Do you already have active listings on Airbnb apart from the one in question?:'),
                            dcc.Slider(
                                id='calc_host_lst_count_sqrt_log',
                                min=0,
                                max=7,
                                step=1,
                                value=0,
                                marks={n: str(n) for n in [0, 1, 2, 3, 4, 5, 6, 7]}
                            ),
                        ]),

                        html.Div([
                            dcc.Markdown('#### If so, are you already a superhost?:'),
                            daq.BooleanSwitch(
                                id='host_is_superhost',
                                on=False,
                                color="#00A699",
                                style={'width': '8%', 'padding-right':'92%'}
                            ),
                        ]),

                        html.Div([
                            dcc.Markdown('#### Will you offer a weekly or monthly discount?:'),
                            dcc.Slider(
                                id='wk_mth_discount',
                                min=0,
                                max=0.5,
                                step=0.05,
                                value=0,
                                marks={n: str(int(n*100))+"%" for n in [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]}
                            ),
                        ]),

                        html.Div([
                            dcc.Markdown('#### Show price for # of guests included:'),
                            dcc.Slider(
                                id='guests_included_calc',
                                min=1,
                                max=9,
                                step=1,
                                value=2,
                                marks={n: str(n) for n in range(1, 9, 1)}
                            ),
                        ]),

                        html.Div([
                            dcc.Markdown('#### How much occupancy are you targeting? (please consider local laws):'),
                            dcc.Slider(
                                id='occupancy_rate',
                                min=0,
                                max=1,
                                step=0.05,
                                value=0.3,
                                marks={n: str(int(n*100))+"%" for n in [0,  0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]}
                            ),
                        ]),

                        dcc.Markdown('### Optional: Select amenities that you provide (defaults are given)'),

                        html.Div([
                            dcc.Markdown('#### Essentials:'),
                            daq.BooleanSwitch(
                                id='am_essentials',
                                on=True,
                                color="#00A699",
                                style={'width': '8%', 'padding-right':'92%'}
                            ),
                        ]),

                        html.Div([
                            dcc.Markdown('#### Balcony:'),
                            daq.BooleanSwitch(
                                id='am_balcony',
                                on=False,
                                color="#00A699",
                                style={'width': '8%', 'padding-right':'92%'}
                            ),
                        ]),

                        html.Div([
                            dcc.Markdown('#### Breakfast:'),
                            daq.BooleanSwitch(
                                id='am_breakfast',
                                on=False,
                                color="#00A699",
                                style={'width': '8%', 'padding-right':'92%'}
                            ),
                        ]),

                        html.Div([
                            dcc.Markdown('#### Child Friendly:'),
                            daq.BooleanSwitch(
                                id='am_child_friendly',
                                on=False,
                                color="#00A699",
                                style={'width': '8%', 'padding-right': '92%'}
                            ),
                        ]),

                        html.Div([
                            dcc.Markdown('#### Elevator:'),
                            daq.BooleanSwitch(
                                id='am_elevator',
                                on=False,
                                color="#00A699",
                                style={'width': '8%', 'padding-right':'92%'}
                            ),
                        ]),

                        html.Div([
                            dcc.Markdown('#### Pets allowed:'),
                            daq.BooleanSwitch(
                                id='am_pets_allowed',
                                on=False,
                                color="#00A699",
                                style={'width': '8%', 'padding-right':'92%'}
                            ),
                        ]),

                        html.Div([
                            dcc.Markdown('#### Private entrance:'),
                            daq.BooleanSwitch(
                                id='am_private_entrance',
                                on=False,
                                color="#00A699",
                                style={'width': '8%', 'padding-right':'92%'}
                            ),
                        ]),

                        html.Div([
                            dcc.Markdown('#### Smoking allowed:'),
                            daq.BooleanSwitch(
                                id='am_smoking_allowed',
                                on=False,
                                color="#00A699",
                                style={'width': '8%', 'padding-right':'92%'}
                            ),
                        ]),

                        html.Div([
                            dcc.Markdown('#### TV:'),
                            daq.BooleanSwitch(
                                id='am_tv',
                                on=False,
                                color="#00A699",
                                style={'width': '8%', 'padding-right':'92%'}
                            ),
                        ]),

                        html.Div(className = 'os-footer', children=[
                            dcc.Markdown('### PRICING INDICATION:'),
                            html.Div(id='listing_price'),
                            html.Div(id='price_range'),
                            html.Div(id='yearly_earnings')]),
                    ])
                ]),
                dcc.Tab(id='tab-map', label='Map of all Listings', className = 'os-tab', children=[
                    html.Div(className='content', style={'margin-bottom': 10, 'padding-bottom': 15}, children=[
                        html.Div([
                            html.Div(id='total_listings')
                        ]),

                        html.Div([
                            dcc.Graph(className='graph', id='map_fig')
                        ]),

                        html.Div([
                            html.Div([
                                dcc.Markdown('### Enter listing # to generate URL (if listing still exists): '),
                                dcc.Link(href='listing_url', id='listing_url', target='_blank')]),
                            dcc.Input(
                                id='listing_no',
                                placeholder="Enter a number...",
                                type='number',
                                value=40610629
                            )
                        ]),
                    ]),
                ]),
            ]),
        ),
    ]),
])


@app.callback(
    [Output('zipcode', 'options'),
     Output('background_img', 'src'),
     Output('zipcode', 'value')],
    [Input('city', 'value')])
def set_date_options(selected_city):
    return [{'label': zipcode[4:], 'value': zipcode} for zipcode in zipcode_options[selected_city]],\
           app.get_asset_url(f'{selected_city.lower()}_background.png'),\
           'zip_other'


@app.callback(
#    Output('prediction-content', 'children'),
    [Output('listing_price', 'children'),
    Output('price_range', 'children'),
    Output('yearly_earnings', 'children')],
    [Input('accommodates', 'value'),
     Input('am_balcony', 'on'),
     Input('am_breakfast', 'on'),
     Input('am_child_friendly', 'on'),
     Input('am_elevator', 'on'),
     Input('am_essentials', 'on'),
     Input('am_pets_allowed', 'on'),
     Input('am_private_entrance', 'on'),
     Input('am_smoking_allowed', 'on'),
     Input('am_tv', 'on'),
     Input('bathrooms_log', 'value'),
     Input('bedrooms', 'value'),
     Input('beds', 'value'),
     Input('calc_host_lst_count_sqrt_log', 'value'),
     Input('cancellation_policy', 'value'),
     Input('guests_included_calc', 'value'),
     Input('host_is_superhost', 'on'),
     Input('instant_bookable', 'on'),
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
        df[col].replace([True, False], [1, 0], inplace=True)
#        df[col] = df[col][0]

    if city == 'berlin':
        x_test_prep = preprocessor.transform(df)
        y_pred = model.predict(x_test_prep)
        y_pred_interval = tuple(
            [(round(curr.convert(math.exp(el - el * MAPE_median), 'USD', 'EUR', date=date(2020, 3, 17))),
              round(curr.convert(math.exp(el + el * MAPE_median), 'USD', 'EUR', date=date(2020, 3, 17)))) for el in
             y_pred])
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

    elif city == 'barcelona':
        x_test_prep = preprocessor4.transform(df)
        y_pred = model4.predict(x_test_prep)
        y_pred_interval = tuple(
            [(round(curr.convert(math.exp(el - el * MAPE_median4), 'USD', 'EUR', date=date(2020, 3, 16))),
              round(curr.convert(math.exp(el + el * MAPE_median4), 'USD', 'EUR', date=date(2020, 3, 16)))) for el in
             y_pred])
        y_pred_exp = [round(curr.convert(math.exp(el), 'USD', 'EUR', date=date(2020, 3, 16))) for el in y_pred]

    listing_price = f'Recommended listing price: €{y_pred_exp[0]}'
    price_range = f'Sensible range: €{y_pred_interval[0][0]}-€{y_pred_interval[0][1]}'
    yearly_earnings = f'Potential yearly earnings: €{round(y_pred_exp[0] * 365 * occupancy_rate)} (at occupancy of {int(occupancy_rate * 100)}%, not considering fees and taxes)'

    return listing_price, price_range, yearly_earnings


@app.callback(
    Output('listing_url', 'href'),
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
        city_date=dataset_date
        zoom=9
    elif city == "amsterdam":
        map_input=data2
        city_date=dataset_date2
        zoom=10
    elif city == "paris":
        map_input=data3
        city_date=dataset_date3
        zoom=11
    elif city == "barcelona":
        map_input=data4
        city_date=dataset_date4
        zoom=11
    data.price = [round(curr.convert(math.exp(el), 'USD', 'EUR', date=date(2020, 3, 17))) for el in data.price_log]
    map_fig = px.scatter_mapbox(
        map_input,
        lat="latitude",
        lon="longitude",
        color="price",
        size="accommodates",
        size_max=15,
#        width="100%",
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
    total_listings = len(map_input.price_log)
    return map_fig, dcc.Markdown(f'### {total_listings} listings in {city.capitalize()} on {city_date}:')


if __name__ == '__main__':
    app.run_server(debug=True)


# OPEN TOPICS:
# - Make for-loop for importing data/models to make it scalable
# - Potentially keep only one date per city (a) makes more sense, b) causes less potential issues)
# - Remove edge/margin in web app (left and top)
