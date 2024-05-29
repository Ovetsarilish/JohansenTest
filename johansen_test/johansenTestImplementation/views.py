import numpy as np
import pandas as pd
import yfinance as yf
from statsmodels.tsa.vector_ar.vecm import coint_johansen
import pandas_datareader as pdr
from django.http import HttpResponse
from django.template import loader

def fun_met(request):
    stock_list = ['JPM', 'BAC', 'WFC', 'C', 'GS', 'MS', 'USB', 'PNC', 'TFC']
    start_date = '2010-01-01'
    end_date = '2022-10-16'
    data = yf.download(stock_list, start=start_date, end=end_date)['Adj Close']

  # Perform the Johansen Cointegration Test with a specified number of zero
    specified_number = 0  # Testing for zero cointegrating relationships
    coint_test_result = coint_johansen(data, specified_number, 1)

  # Extract the trace statistics and eigen statistics
    trace_stats = coint_test_result.lr1
    eigen_stats = coint_test_result.lr2
    crit_val = coint_test_result.cvt
  # Print the test results
    print("Johansen Cointegration Test Results (Testing for Zero Cointegrating Relationships):")
    print(f"Trace Statistics: {coint_test_result.lr1}")
    print(f"Critical Values: {coint_test_result.cvt}")

    # Define stock pairs
    stock_pairs = [('JPM', 'BAC'), ('BAC', 'WFC'), ('C', 'USB'), ('GS', 'MS')]

    # Separate the output sections
    print("\n" + "-" * 50 + "\n")
    st_dict = []
    # Interpret the results for each pair
    for i, (stock1, stock2) in enumerate(stock_pairs):
        st_dict.append({
            "st1" : stock1,
            "st2" : stock2,
            "trace_statistics" : trace_stats[i],
            "eigen_statistics" : eigen_stats[i]
        })

    # Determine cointegration based on critical values or other criteria
    # Add your cointegration assessment logic here
    print("Cointegration Assessment: Testing for Zero Cointegrating Relationships (Null Hypothesis)\n")
    pairs = [('JPM', 'BAC'), ('BAC', 'WFC'), ('C', 'USB'), ('GS', 'MS')]

    # Set the start date and the end date
    start_date = '2010-01-01'
    end_date = '2022-10-16'

    # Download stock price data for all pairs
    data = yf.download([pair[0] for pair in pairs] + [pair[1] for pair in pairs], start=start_date, end=end_date)['Adj Close']

    # Perform the Johansen Cointegration Test for all pairs
    coint_test_result_pair = coint_johansen(data, det_order=0, k_ar_diff=1)

    # Extract the eigenvalues and critical values
    tracevalues = coint_test_result_pair.lr1
    critical_values = coint_test_result_pair.cvt
    pair_dict = []
    # Interpret the results for each pair
    for i, (stock1, stock2) in enumerate(pairs):
        pair_dict.append({
            'stock1' : stock1,
            'stock2' : stock2,
            'trace_value' : tracevalues[i],
            'cr_value' : critical_values[i],
            'flag' : False,
        })
        if (tracevalues[i] > critical_values[:, 1]).all():
            pair_dict[i]['flag'] = True
    template = loader.get_template('index.html')
    context = {
      'trace_stats' : trace_stats,
      'eigen_stats' : eigen_stats,
      'crit_val' : crit_val,
      'st_dict' : st_dict,
      'pair_dict' : pair_dict
    }
    return HttpResponse(template.render(context, request))