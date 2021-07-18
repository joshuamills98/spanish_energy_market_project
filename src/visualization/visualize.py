def plot_forecast(model, data, periods,
                  ax,
                  historic_pred=True,
                  highlight_steps_ahead=None):

    future = model.make_future_dataframe(data,
                                         periods=periods,
                                         n_historic_predictions=historic_pred)
    forecast = model.predict(future)

    if highlight_steps_ahead is not None:
        model = model.highlight_nth_step_ahead_of_each_forecast(
            highlight_steps_ahead)
        model.plot_last_forecast(forecast, ylabel='Power MW', ax=ax)
    else:
        model.plot(forecast,
                   ylabel='Power Generation (MW)',
                   xlabel='Date',
                   ax=ax)
    return forecast