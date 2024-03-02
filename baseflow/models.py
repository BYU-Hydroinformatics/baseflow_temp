import numpy as np


def lyne_hollick(streamflow_list, alpha):
    """
    Calculates baseflow approximations using the Lyne and Hollick equation.

    Args:
        streamflow_list (list): A list of streamflow values
        alpha (float): Catchment constant between 0 and 1

    Returns:
        list: A timeseries list of baseflow values

    Example:
        .. code-block:: python

            import pandas as pd
            discharge_time_series = pd.read_csv("/my/sample/file.csv")
            alpha = 0.925
            baseflow = lyne_hollick(discharge_time_series['Discharge'], alpha)

    """
    # Alpha must be between 0 and 1
    if alpha < 0 or alpha > 1:
        print("Alpha must be between 0 and 1.")

    else:
        # Get rid of all NaNs in dataframe and then reset the new first row to the first index
        streamflow_list.dropna(inplace=True)
        streamflow_list.reset_index(drop=True, inplace=True)

        # Assume the first baseflow value is equal to the first streamflow value to give you a starting point
        baseflow_value = streamflow_list[0]
        baseflow_list = [baseflow_value]

        # zip makes a list of pairs so that the function can use current and previous streamflow at the same time
        for currentStreamflow, prevStreamflow in zip((streamflow_list)[1:], (streamflow_list)[:-1]):
            # Equation
            baseflow_value = currentStreamflow - (alpha * (prevStreamflow - baseflow_value) + ((1 + alpha) / 2) * (
                    currentStreamflow - prevStreamflow))
            baseflow_list.append(baseflow_value)

        # Create the new column in the dataframe
        return baseflow_list


def chapman(streamflow_list, alpha, beta):
    '''
    Calculates baseflow approximations using the Chapman equation.
    
    Args:
        streamflow_list (float series): A list of streamflow values
        alpha (float): Hydrological recession constant between 0 and 1

    Returns:
        baseflow (float series): A list of baseflow values
    '''
    if alpha < 0 or alpha > 1:
        print("Alpha must be between 0 and 1.")

    else:
        streamflow_list.dropna(inplace=True)
        streamflow_list.reset_index(drop=True, inplace=True)

        baseflow_value = streamflow_list[0]
        baseflow_list = [baseflow_value]

        for currentStreamflow, prevStreamflow in zip((streamflow_list)[1:], (streamflow_list)[:-1]):
            baseflow_value = ((3 * alpha - 1) / (3 - alpha)) * baseflow_value + ((1 - alpha) / (3 - alpha)) * (
                    currentStreamflow + prevStreamflow)
            baseflow_list.append(baseflow_value)

        return baseflow_list


def eckhardt(streamflow_list, alpha, bfi_max):
    '''
    Calculates baseflow approximations using the Eckhardt equation.
    
    Args:
        streamflow_list (float series): A list of streamflow values
        alpha (float): Hydrological recession constant between 0 and 1

    Returns:
        baseflow (float series): A list of baseflow values
    '''    
    if alpha <= 0 or alpha >= 1:
        print("Alpha must be between 0 and 1.")
    if bfi_max <= 0 or bfi_max >= 1:
        print("BFI max must be between 0 and 1.")

    else:
        streamflow_list.dropna(inplace=True)
        streamflow_list.reset_index(drop=True, inplace=True)

        baseflow_value = streamflow_list[0]
        baseflow_list = [baseflow_value]

        for currentStreamflow in streamflow_list[1:]:
            baseflow_value = ((1 - bfi_max) * alpha * baseflow_value + (1 - alpha) * bfi_max * currentStreamflow) / (
                    1 - (alpha * bfi_max))
            baseflow_list.append(baseflow_value)

        return baseflow_list


def chapman_maxwell(streamflow_list, k):
    """
    Separates baseflow from a streamflow hydrograph using the Chapman & Maxwell method.

    Args:
        streamflow_list (list): A list of streamflow values in chronological order.
        k (float): A smoothing parameter between 0 and 1.

    Returns:
        list: A list containing the separated baseflow values.
  """
    if k < 0 or k > 1:
        print("k must be between 0 and 1.")
        return None

    else:
        streamflow_list.dropna(inplace=True)
        streamflow_list.reset_index(drop=True, inplace=True)

        baseflow_value = streamflow_list[0]
        baseflow_list = [baseflow_value]
        quickflow_list = []

        for currentStreamflow in streamflow_list[1:]:
            baseflow_value = (1 / (2 - k)) * baseflow_value + ((1 - k) / (2 - k)) * currentStreamflow
            baseflow_list.append(baseflow_value)

        for streamflow, baseflow in zip(streamflow_list, baseflow_list):
            quickflow = streamflow - baseflow
            # Check if quickflow is negative and set it to zero if it is
            quickflow = max(0, quickflow)
            quickflow_list.append(quickflow)

        return baseflow_list
