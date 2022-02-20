from flask import Flask, render_template, request

app = Flask(__name__)

# Creating simple Routes 
@app.route('/test')
def test():
    return "Home Page"

@app.route('/test/about/')
def about_test():
    return "About Page"


# Routes to Render Something
@app.route('/')
def home():
    return render_template("home.html")


@app.route('/dato', methods=['POST'])
def dato():
    nombreUser= datos()
    return nombreUser












#----------------------------------------------------


#----------------------------------------------------
def datos():
    warnings.filterwarnings("ignore") # specify to ignore warning messages
    print('----------------------------------------------------')
    data = pd.read_csv('./sample_data/train.csv', engine='python', skipfooter=3)
    data = data.groupby(data.family)
    data = data.get_group("GROCERY I")
    data = data.groupby(data.store_nbr)
    data = data.get_group(1)
    data['date']=pd.to_datetime(data['date'], format='%Y-%m-%d')
    data = data.groupby(data['date'].dt.strftime('%Y-%m')).sum().reset_index()
    data = pd.DataFrame(data, columns = ['date','sales'])
    data['date']=pd.to_datetime(data['date'], format='%Y-%m-%d')
    data.set_index(['date'], inplace=True)
    data = data[:-1]
    ass = data.iloc[-1:]
    data = pd.concat([data, ass])

    q = d = range(0, 1)
    p = range(0, 3)
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

    train_data = data['2013-01-01':'2016-12-01']
    test_data = data['2017-01-01':'2017-02-01']
    
    AIC = []
    SARIMAX_model = []
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(train_data,
                                                order=param,
                                                seasonal_order=param_seasonal,
                                                enforce_stationarity=False,
                                                enforce_invertibility=False)

                results = mod.fit()

                print('SARIMAX{}x{} - AIC:{}'.format(param, param_seasonal, results.aic), end='\r')
                AIC.append(results.aic)
                SARIMAX_model.append([param, param_seasonal])
            except:
                continue
            
    mod = sm.tsa.statespace.SARIMAX(train_data,
                                    order=SARIMAX_model[AIC.index(min(AIC))][0],
                                    seasonal_order=SARIMAX_model[AIC.index(min(AIC))][1],
                                    enforce_stationarity=False,
                                    enforce_invertibility=False)
    results = mod.fit()

    pred0 = results.get_prediction(start='2015-01-01', dynamic=False) #un anio antes del train data 
    pred0_ci = pred0.conf_int()
    pred1 = results.get_prediction(start='2015-01-01', dynamic=True) #un anio antes del train data 
    pred1_ci = pred1.conf_int()
    pred2 = results.get_forecast('2018-12-01') #anios no conocidos 
    pred2_ci = pred2.conf_int()
    prediction = pred2.predicted_mean['2017-01-01':'2017-02-01'].values
    truth = list(itertools.chain.from_iterable(test_data.values))
    MAPE = np.mean(np.abs((truth - prediction) / truth)) * 100
    #print('El error porcentual absoluto medio para el pronóstico del año 2017 mes de Enero es {:.2f}%'.format(MAPE))
    #print(truth)
    #print(prediction)

    return 'El error porcentual absoluto medio para el pronóstico del año 2017 mes de Enero es {:.2f}%'.format(MAPE)


if __name__ == '__main__':
    app.run(debug=True)