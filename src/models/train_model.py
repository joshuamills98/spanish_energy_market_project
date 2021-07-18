from neural_prophet.neuralprophet import NeuralProphet


def create_time_series(df, energy_source):
    time_series = df\
                .reset_index()\
                .rename(columns={'time': 'ds',
                                 energy_source: 'y'})[['ds', 'y']]
    time_series['ds'] = time_series['ds']\
        .apply(lambda x: x.strftime('%Y-%m-%d'))
    return time_series


def run_experiment(e, ax, title, k=3, fold_pct=0.2, plot=False):
    df = e.df
    df = create_time_series(df, e.column_name)
    print(" ---- running exp: {} (len: {}) ----"
          .format(title, len(df)))
    folds = NeuralProphet(**e.model_config)\
        .crossvalidation_split_df(df,
                                  freq='D',
                                  k=k,
                                  fold_pct=fold_pct,
                                  fold_overlap_pct=0.0)
    train, val = [], []
    for df_train, df_val in folds:
        m = NeuralProphet(**e.model_config)
        metrics_train = m.fit(df_train, freq='D', plot_live_loss=False)
        metrics_val = m.test(df_val)
        train.append(metrics_train["MAE"].values[-1])
        val.append(metrics_val["MAE"].values[-1])
    if plot:
        future = m.make_future_dataframe(df_train,
                                         periods=len(df_val),
                                         n_historic_predictions=len(df_train))
        forecast = m.predict(future)
        m.plot(forecast, ax=ax)
    print("train MAE:", train)
    print("val MAE:", val)
    print("train MAE (avg):", sum(train)/len(train))
    print("val MAE (avg):", sum(val)/len(val))
