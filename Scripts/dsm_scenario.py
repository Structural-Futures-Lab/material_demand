# Dynamic stock model (DSM) for US building stock

# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from odym.modules import dynamic_stock_model as dsm

# --- MA run plot styling: prevent stacked-subplot title/label overlap; sensible default size ---
plt.rcParams['figure.figsize'] = (10, 7)
plt.rcParams['figure.constrained_layout.use'] = True

def _dg(yrs, y, gap=False):
    # Plot-only helper: blank the 1997 cold-start point, and (gap=True) the 2026-2029
    # interpolation bridge, so historic vs SSP-projection segments don't connect.
    yr = np.asarray(yrs, dtype=float); ya = np.array(y, dtype=float)
    m = (yr == 1997)
    if gap:
        m |= (yr >= 2026) & (yr <= 2029)
    ya[m] = np.nan
    return ya

# Load in datasets -- MA_model_inputs.xlsx is the only input file
data_pop_WiC = pd.read_excel('./InputData/MA_model_inputs.xlsx', sheet_name='final pop data')
data_gdp = pd.read_excel('./InputData/MA_model_inputs.xlsx', sheet_name='final gdp data')


# function to interpolate the population data
def interpolate_population(data_pop, year1=1900, year2=2100, proj='median', kind='cubic', plot=True):
    """ Interpolate the Massachusetts population data between the specified years.
        Choose a scenario for future population data (SSP1-SSP5, or 'All').
        Options for 'kind' are [linear, cubic, nearest, previous, and next] """
    # Create interpolations for population
    f_SSP1 = interp1d(data_pop.Year, data_pop.SSP1, kind=kind)
    f_SSP2 = interp1d(data_pop.Year, data_pop.SSP2, kind=kind)
    f_SSP3 = interp1d(data_pop.Year, data_pop.SSP3, kind=kind)
    f_SSP4 = interp1d(data_pop.Year, data_pop.SSP4, kind=kind)
    f_SSP5 = interp1d(data_pop.Year, data_pop.SSP5, kind=kind)

    # Study Period
    # year1 = 1900
    # year2 = 2100
    years = np.linspace(year1, year2, num=(year2 - year1 + 1), endpoint=True)

    if proj == 'SSP1':
        US_pop = f_SSP1(years)
        US_pop_years = pd.DataFrame({'Year': years,
                                     'US_pop_' + str(proj): US_pop})
    elif proj == 'SSP2':
        US_pop = f_SSP2(years)
        US_pop_years = pd.DataFrame({'Year': years,
                                     'US_pop_' + str(proj): US_pop})
    elif proj == 'SSP3':
        US_pop = f_SSP3(years)
        US_pop_years = pd.DataFrame({'Year': years,
                                     'US_pop_' + str(proj): US_pop})
    elif proj == 'SSP4':
        US_pop = f_SSP4(years)
        US_pop_years = pd.DataFrame({'Year': years,
                                     'US_pop_' + str(proj): US_pop})
    elif proj == 'SSP5':
        US_pop = f_SSP5(years)
        US_pop_years = pd.DataFrame({'Year': years,
                                     'US_pop_' + str(proj): US_pop})
    elif proj == 'All':
        US_pop_years = pd.DataFrame({'Year': years,
                               'US_pop_SSP1': f_SSP1(years),
                               'US_pop_SSP2': f_SSP2(years),
                               'US_pop_SSP3': f_SSP3(years),
                               'US_pop_SSP4': f_SSP4(years),
                               'US_pop_SSP5': f_SSP5(years),
                               })
    else:
        US_pop_years = None


    if plot == True:
        # Plot of population forecasts
        plt1, = plt.plot(years, _dg(years, f_SSP1(years), gap=True))
        plt2, = plt.plot(years, _dg(years, f_SSP2(years), gap=True))
        plt3, = plt.plot(years, _dg(years, f_SSP3(years), gap=True))
        plt4, = plt.plot(years, _dg(years, f_SSP4(years), gap=True))
        plt5, = plt.plot(years, _dg(years, f_SSP5(years), gap=True))
        plt.axvline(base_year, color='k', linestyle='--')
        plt.legend([plt1, plt2, plt3, plt4, plt5],
                   ['SSP1', 'SSP2', 'SSP3', 'SSP4', 'SSP5'],
                   loc=2)
        plt.xlabel('Year')
        plt.ylabel('Massachusetts Population')
        plt.title(r'Historical and Forecast of Population in Massachusetts' + '\n' + '(historical + SSP)')
        plt.show();

    return years, US_pop_years

# function to interpolate the gdp data
def interpolate_gdp(data_gdp, year1=1900, year2=2100, SSP='SSP1', kind='cubic', plot=True):
    """ Interpolate the GDP data between the specified years for the US.
        Choose a UN projection for future population data (median, upper_95, lower_95, upper_80, or lower_80).
        Options for 'kind' are [linear, cubic, nearest, previous, and next] """

    # Create interpolations for population
    f_SSP1 = interp1d(data_gdp.Year, data_gdp.SSP1, kind=kind)
    f_SSP2 = interp1d(data_gdp.Year, data_gdp.SSP2, kind=kind)
    f_SSP3 = interp1d(data_gdp.Year, data_gdp.SSP3, kind=kind)
    f_SSP4 = interp1d(data_gdp.Year, data_gdp.SSP4, kind=kind)
    f_SSP5 = interp1d(data_gdp.Year, data_gdp.SSP5, kind=kind)

    # Study Period
    # year1 = 1900
    # year2 = 2100
    years = np.linspace(year1, year2, num=(year2 - year1 + 1), endpoint=True)

    if SSP == 'SSP1':
        US_gdp = f_SSP1(years)
    elif SSP == 'SSP2':
        US_gdp = f_SSP2(years)
    elif SSP == 'SSP3':
        US_gdp = f_SSP3(years)
    elif SSP == 'SSP4':
        US_gdp = f_SSP4(years)
    elif SSP == 'SSP5':
        US_gdp = f_SSP5(years)
    elif SSP == 'All':
        US_gdp = pd.DataFrame({'gdp_SSP1': f_SSP1(years),
                               'gdp_SSP2': f_SSP2(years),
                               'gdp_SSP3': f_SSP3(years),
                               'gdp_SSP4': f_SSP4(years),
                               'gdp_SSP5': f_SSP5(years)})
    else:
        US_gdp = None
    years_df = pd.DataFrame({'Year': years})
    US_gdp_years = pd.concat([years_df, US_gdp], axis=1)

    if plot == True:
        # Plot of population forecasts
        plt1, = plt.plot(years, _dg(years, f_SSP1(years), gap=True))
        plt2, = plt.plot(years, _dg(years, f_SSP2(years), gap=True))
        plt3, = plt.plot(years, _dg(years, f_SSP3(years), gap=True))
        plt4, = plt.plot(years, _dg(years, f_SSP4(years), gap=True))
        plt5, = plt.plot(years, _dg(years, f_SSP5(years), gap=True))
        # plt6, = plt.plot([base_year, base_year], [2.4e8, 4.5e8], color='k', linestyle='--')
        plt.legend([plt1, plt2, plt3, plt4, plt5],
                   ['SSP1', 'SSP2', 'SSP3', 'SSP4', 'SSP5'],
                   loc=2)
        plt.xlabel('Year')
        plt.ylabel('Massachusetts GDP per capita')
        plt.title('Historical and Forecast of per-capita GDP in Massachusetts')
        plt.show();

    return US_gdp_years

# function to calculate the floor area elasticity by the methodology of the EDGE model
def FA_elasticity_EDGE(US_gdp, US_pop, SSP='All',
                       base_year=2016,FA_base_year=246, Area_country=9.14759e6, gamma=-0.03,
                       plot=True):
    """ Area of the USA is 9.834 million km².
        Base year floor are elasticity for all buildings is 347 m2/person as determined by article (in review)"""

    def calc_FA_elas(gdp, SSP, SSP_split_year=1985):
        # Beta values for each SSP
        Beta_SSP = {'SSP1': 0.3,
                    'SSP2': 0.7,
                    'SSP3': 0.8,
                    'SSP4': 0.7,
                    'SSP5': 1.0}
        # General Beta for floor space demand:
        Beta = 0.42

        FA_df = pd.merge(US_pop, gdp, on='Year')
        FA_df = FA_df.set_index('Year', drop=False)

        # calculate historical FA
        FA_df['Pop_Dens_'+SSP] = FA_df['US_pop_'+SSP] / Area_country
        base_year_0_df = FA_df.loc[[base_year]]
        alpha  = FA_base_year / (base_year_0_df['gdp_'+SSP] ** Beta * base_year_0_df['Pop_Dens_'+SSP] ** gamma)
        # alpha reported by EDGE model is 0.61.
        # alpha from Arehart et al. 2020 high   = 5.002223
        #                                median = 4.350305
        #                                low    = 3.635701
        # print('Alpha is = ' + str(alpha))

        FA_df.loc[FA_df['Year'] <= base_year, 'FA_elas_'+SSP] = alpha[base_year] * (FA_df['gdp_'+SSP] ** Beta) * FA_df['Pop_Dens_'+SSP] ** gamma
        for i in range(1,len(FA_df)):
            year_i = FA_df.index[i]
            if year_i > base_year:
                row_t_1 = FA_df.loc[year_i-1]
                FA_t_1 = row_t_1['FA_elas_'+SSP]
                I_t_1 = row_t_1['gdp_'+SSP]
                D_t_1 = row_t_1['Pop_Dens_'+SSP]
                row_t = FA_df.loc[year_i]
                I_t = row_t['gdp_'+SSP]
                D_t = row_t['Pop_Dens_'+SSP]
                FA_df.loc[int(year_i),'FA_elas_'+SSP] = FA_t_1 * (I_t/I_t_1) ** Beta_SSP[SSP] * (D_t/D_t_1) ** gamma
        return FA_df

    FA_SSP1 = calc_FA_elas(US_gdp, 'SSP1')
    FA_SSP2 = calc_FA_elas(US_gdp, 'SSP2')
    FA_SSP3 = calc_FA_elas(US_gdp, 'SSP3')
    FA_SSP4 = calc_FA_elas(US_gdp, 'SSP4')
    FA_SSP5 = calc_FA_elas(US_gdp, 'SSP5')

    if SSP=='SSP1':
        df_return = FA_SSP1
    elif SSP=='SSP2':
        df_return = FA_SSP2
    elif SSP=='SSP3':
        df_return = FA_SSP3
    elif SSP=='SSP4':
        df_return = FA_SSP4
    elif SSP=='SSP5':
        df_return = FA_SSP5
    elif SSP=='All':
        df_return = pd.DataFrame({'Year': FA_SSP1['Year'],
                                  'US_pop_SSP1': FA_SSP1['US_pop_SSP1'],
                                  'US_pop_SSP2': FA_SSP2['US_pop_SSP2'],
                                  'US_pop_SSP3': FA_SSP3['US_pop_SSP3'],
                                  'US_pop_SSP4': FA_SSP4['US_pop_SSP4'],
                                  'US_pop_SSP5': FA_SSP5['US_pop_SSP5'],
                                  'US_gdp_SSP1': FA_SSP1['gdp_SSP1'],
                                  'US_gdp_SSP2': FA_SSP2['gdp_SSP2'],
                                  'US_gdp_SSP3': FA_SSP3['gdp_SSP3'],
                                  'US_gdp_SSP4': FA_SSP4['gdp_SSP4'],
                                  'US_gdp_SSP5': FA_SSP5['gdp_SSP5'],
                                  'FA_SSP1': FA_SSP1['FA_elas_SSP1'],
                                  'FA_SSP2': FA_SSP2['FA_elas_SSP2'],
                                  'FA_SSP3': FA_SSP3['FA_elas_SSP3'],
                                  'FA_SSP4': FA_SSP4['FA_elas_SSP4'],
                                  'FA_SSP5': FA_SSP5['FA_elas_SSP5'], })

        if plot == True:
            # Plot GFA vs time.
            max_GFA = max(FA_SSP1.FA_elas_SSP1.max(), FA_SSP2.FA_elas_SSP2.max(), FA_SSP3.FA_elas_SSP3.max(), FA_SSP4.FA_elas_SSP4.max(), FA_SSP5.FA_elas_SSP5.max())
            plt1, = plt.plot(df_return.index, _dg(df_return.index, df_return.FA_SSP1, gap=True))
            plt2, = plt.plot(df_return.index, _dg(df_return.index, df_return.FA_SSP2, gap=True))
            plt3, = plt.plot(df_return.index, _dg(df_return.index, df_return.FA_SSP3, gap=True))
            plt4, = plt.plot(df_return.index, _dg(df_return.index, df_return.FA_SSP4, gap=True))
            plt5, = plt.plot(df_return.index, _dg(df_return.index, df_return.FA_SSP5, gap=True))
            plt6, = plt.plot([base_year, base_year], [0, max_GFA], color='k', linestyle='--')
            plt.legend([plt1, plt2, plt3, plt4, plt5],
                       ['SSP1', 'SSP2', 'SSP3', 'SSP4', 'SSP5'], loc=2)
            plt.xlabel('Year')
            plt.ylabel('Floor Area Elasticity')
            plt.title('Floor Area Elasticity for various SSPs')
            plt.show();
            # Plot GFA vs GDP.
            plt1, = plt.plot(df_return.US_gdp_SSP1, _dg(df_return.index, df_return.FA_SSP1, gap=True))
            plt2, = plt.plot(df_return.US_gdp_SSP2, _dg(df_return.index, df_return.FA_SSP2, gap=True))
            plt3, = plt.plot(df_return.US_gdp_SSP3, _dg(df_return.index, df_return.FA_SSP3, gap=True))
            plt4, = plt.plot(df_return.US_gdp_SSP4, _dg(df_return.index, df_return.FA_SSP4, gap=True))
            plt5, = plt.plot(df_return.US_gdp_SSP5, _dg(df_return.index, df_return.FA_SSP5, gap=True))
            plt.legend([plt1, plt2, plt3, plt4, plt5],
                       ['SSP1', 'SSP2', 'SSP3', 'SSP4', 'SSP5'], loc=2)
            plt.xlabel('GDP')
            plt.ylabel('Floor Area Elasticity')
            plt.title('Floor Area Elasticity for various SSPs')
            plt.show();


    return df_return


    # FA_historic = np.linspace(FA_elas_year1, FA_elas_base_year, num=(base_year - year1 + 1), endpoint=True)
    # FA_future = np.linspace(FA_elas_base_year, FA_elas_year2, num=(year2 - base_year), endpoint=True)
    #
    # FA_elas = pd.DataFrame({'Year': years,
    #                         'FA_elas': np.concatenate((FA_historic, FA_future), axis=0)
    #                         }, )

# Time period input variables
year1 = 1997
year2 = 2100
base_year = 2020

# interpolate population data for the US.
years, US_pop = interpolate_population(data_pop=data_pop_WiC, year1=year1, year2=year2, proj='All', plot=True)

# interpolate gdp data for the US.
US_gdp = interpolate_gdp(data_gdp, year1=year1, year2=year2, SSP='All', kind='cubic', plot=True)
# calculate total floor area elasticity
FA_all = FA_elasticity_EDGE(US_gdp, US_pop, SSP='All',
                       base_year=2020,FA_base_year=100.7, Area_country=20202, gamma=-0.03,
                       plot=True)      # area of continguous 48 = 8081867, area of all = 9833517


US_pop = US_pop.set_index('Year', drop=False)
US_gdp = US_gdp.set_index('Year', drop=False)


# ratio of residential floor area to total floor area:
ratio_res = 0.724062
ratio_com = 0.179763
ratio_pub = 0.034883

def do_stock_driven_model(t, s, lt):
    """ Compute a stock driven model from an initial stock.
        Returns an object with class dynamic_stock_model with age-cohort matrix
        with inputs, outputs, and stocks computed"""

    my_dsm = dsm.DynamicStockModel(t=t, s=s, lt=lt)
    CheckStr = my_dsm.dimension_check()
    print(CheckStr)

    S_C, O_C, I = my_dsm.compute_stock_driven_model(NegativeInflowCorrect=True)

    O = my_dsm.compute_outflow_total()  # Total outflow
    DS = my_dsm.compute_stock_change()  # Stock change
    Bal = my_dsm.check_stock_balance()  # Stock balance
    print('The mass balance between inflows and outflows is:   ')
    print(np.abs(Bal).sum())  # show sum absolute of all mass balance mismatches.
    return my_dsm

# A function to generate lifetime distributions for use in the ODYM dsm package.
def generate_lt(type, par1, par2):
    ''' Normal: par1  = mean, par2 = std. dev
        Weibull: par1 = shape, par2 = scale'''

    # ---- Building lifespan distributions ----
    # BldgLife_mean_res = 80  # years
    # BldgLife_StdDev_res = 0.2 *  np.array([BldgLife_mean_res] * len(years))
    # BldgLife_mean_com = 70  # years
    # BldgLife_StdDev_com = 0.2 *  np.array([BldgLife_mean_com] * len(years))
    # BldgLife_mean_pub = 90  # years
    # BldgLife_StdDev_pub = 0.2 * np.array([BldgLife_mean_com] * len(years))
    if type=='Normal':
        # Normal
        lt = {'Type': type, 'Mean': np.array([par1] * len(years)), 'StdDev': par2}
    elif type=='Weibull':
        # Weibull
        # lt_res = {'Type': 'Weibull', 'Shape': np.array([4.16343417]), 'Scale': np.array([85.18683893])}     # deetman_2018_res_distr_weibull
        # lt_res = {'Type': 'Weibull', 'Shape': np.array([5.5]), 'Scale': np.array([85.8])}
        # lt_com = {'Type': 'Weibull', 'Shape': np.array([4.8]), 'Scale': np.array([75.1])}
        # lt_res = {'Type': type, 'Shape': np.array([5]), 'Scale': np.array([130])}
        # lt_com = {'Type': type, 'Shape': np.array([3]), 'Scale': np.array([100])}
        # lt_pub = {'Type': type, 'Shape': np.array([6.1]), 'Scale': np.array([95.6])}
        lt = {'Type': type, 'Shape': np.array([par1]), 'Scale': np.array([par2])}
    return lt

lt_res = generate_lt('Weibull',par1=5.5, par2=85.8)
lt_com = generate_lt('Weibull',par1=4.8, par2=75.1)
lt_pub = generate_lt('Weibull',par1=6.1, par2=95.6)

# Debugging
# lt_res = generate_lt('Weibull',par1=5, par2=100)
# lt_com = generate_lt('Weibull',par1=5, par2=100)
# lt_pub = generate_lt('Weibull',par1=5, par2=100)

# Plot lifetime distributions:
plot_lifetime_distr=False
if plot_lifetime_distr==True:
    x = np.arange(1,200)
    def weib(x,n,a):
        return (a / n) * (x / n)**(a - 1) * np.exp(-(x / n)**a)

    # count, bins, ignored = plt.hist(np.random.weibull(5.5,1000))
    # scale = count.max()/weib(x, 85.8, 5.5).max()
    plt1, = plt.plot(x, weib(x, lt_res['Scale'][0], lt_res['Shape'][0])*lt_res['Scale'][0], label='Weibull Residential')
    plt2, = plt.plot(x, weib(x, lt_com['Scale'][0], lt_com['Shape'][0])*lt_com['Scale'][0], label='Weibull Commercial')
    plt3, = plt.plot(x, weib(x, lt_pub['Scale'][0], lt_pub['Shape'][0])*lt_pub['Scale'][0], label='Weibull Public')
    plt.legend(loc=2)
    plt.title('Input Weibull Distributions')
    plt.xlabel('Building lifespan')
    plt.show()

    # mess around
    lt1 = generate_lt('Weibull', par1=8, par2=100)
    lt2 = generate_lt('Weibull', par1=6, par2=100)
    lt3 = generate_lt('Weibull', par1=3, par2=100)
    lt4 = generate_lt('Weibull', par1=5, par2=60)
    lt5 = generate_lt('Weibull', par1=5, par2=80)
    lt6 = generate_lt('Weibull', par1=5, par2=100)
    lt7 = generate_lt('Weibull', par1=5, par2=120)

    plt1, = plt.plot(x, weib(x, lt1['Scale'][0], lt1['Shape'][0]) * lt1['Scale'][0], label='weibull(8, 100)', linestyle='--')
    plt2, = plt.plot(x, weib(x, lt2['Scale'][0], lt2['Shape'][0]) * lt2['Scale'][0], label='weibull(6, 100)', linestyle='--')
    plt3, = plt.plot(x, weib(x, lt3['Scale'][0], lt3['Shape'][0]) * lt3['Scale'][0], label='weibull(3, 100)', linestyle='--')
    plt4, = plt.plot(x, weib(x, lt4['Scale'][0], lt4['Shape'][0]) * lt4['Scale'][0], label='weibull(5, 60)')
    plt5, = plt.plot(x, weib(x, lt5['Scale'][0], lt5['Shape'][0]) * lt5['Scale'][0], label='weibull(5, 80)')
    plt6, = plt.plot(x, weib(x, lt6['Scale'][0], lt6['Shape'][0]) * lt6['Scale'][0], label='weibull(5, 100)')
    plt7, = plt.plot(x, weib(x, lt7['Scale'][0], lt7['Shape'][0]) * lt7['Scale'][0], label='weibull(5, 120)')

    plt.legend(loc=2)
    plt.title('Input Weibull Distributions')
    plt.xlabel('Building lifespan')
    plt.show()

# function to calculate the dynamic stock.
def calc_MFA(scenario, lt_res, lt_com, lt_pub):
    # select a scenario to consider during debugging
    # scenario = 'SSP1'
    # lifetime = 'Weibull'
    scenario_pop = US_pop['US_pop_'+scenario]
    scenario_gdp = US_gdp['gdp_'+scenario]
    scenario_FAE_res = FA_all['FA_'+scenario] * ratio_res
    scenario_FAE_com = FA_all['FA_'+scenario] * ratio_com
    scenario_FAE_pub = FA_all['FA_' + scenario] * ratio_pub

    # calculate demanded floor area stock
    stock_res = scenario_pop.mul(scenario_FAE_res) / 1000000
    stock_com = scenario_pop.mul(scenario_FAE_com) / 1000000
    stock_pub = scenario_pop.mul(scenario_FAE_pub) / 1000000

    t = years
    US_stock_res = do_stock_driven_model(t, np.array(stock_res), lt_res)
    US_stock_com = do_stock_driven_model(t, np.array(stock_com), lt_com)
    US_stock_pub = do_stock_driven_model(t, np.array(stock_pub), lt_pub)

    return US_stock_res, US_stock_com, US_stock_pub

# Calculate MFA for individual scenarios
SSP1_dsm_res, SSP1_dsm_com, SSP1_dsm_pub = calc_MFA('SSP1', lt_res, lt_com, lt_pub)
SSP2_dsm_res, SSP2_dsm_com, SSP2_dsm_pub = calc_MFA('SSP2', lt_res, lt_com, lt_pub)
SSP3_dsm_res, SSP3_dsm_com, SSP3_dsm_pub = calc_MFA('SSP3', lt_res, lt_com, lt_pub)
SSP4_dsm_res, SSP4_dsm_com, SSP4_dsm_pub = calc_MFA('SSP4', lt_res, lt_com, lt_pub)
SSP5_dsm_res, SSP5_dsm_com, SSP5_dsm_pub = calc_MFA('SSP5', lt_res, lt_com, lt_pub)



# Save the floor area models as .csv files.
SSP1_dsm_df = pd.DataFrame({'time': SSP1_dsm_res.t,
                            'stock_res': SSP1_dsm_res.s,
                            'inflow_res': SSP1_dsm_res.i,
                            'outflow_res': SSP1_dsm_res.o,
                            'stock_com': SSP1_dsm_com.s,
                            'inflow_com': SSP1_dsm_com.i,
                            'outflow_com': SSP1_dsm_com.o,
                            'stock_pub': SSP1_dsm_pub.s,
                            'inflow_pub': SSP1_dsm_pub.i,
                            'outflow_pub': SSP1_dsm_pub.o,
                            'stock_total': SSP1_dsm_res.s + SSP1_dsm_com.s + SSP1_dsm_pub.s,
                            'inflow_total': SSP1_dsm_res.i + SSP1_dsm_com.i + SSP1_dsm_pub.i,
                            'outflow_total': SSP1_dsm_res.o + SSP1_dsm_com.o + SSP1_dsm_pub.o
                            })
SSP2_dsm_df = pd.DataFrame({'time': SSP2_dsm_res.t,
                            'stock_res': SSP2_dsm_res.s,
                            'inflow_res': SSP2_dsm_res.i,
                            'outflow_res': SSP2_dsm_res.o,
                            'stock_com': SSP2_dsm_com.s,
                            'inflow_com': SSP2_dsm_com.i,
                            'outflow_com': SSP2_dsm_com.o,
                            'stock_pub': SSP2_dsm_pub.s,
                            'inflow_pub': SSP2_dsm_pub.i,
                            'outflow_pub': SSP2_dsm_pub.o,
                            'stock_total': SSP2_dsm_res.s + SSP2_dsm_com.s + SSP2_dsm_pub.s,
                            'inflow_total': SSP2_dsm_res.i + SSP2_dsm_com.i + SSP2_dsm_pub.i,
                            'outflow_total': SSP2_dsm_res.o + SSP2_dsm_com.o + SSP2_dsm_pub.o
                            })
SSP3_dsm_df = pd.DataFrame({'time': SSP3_dsm_res.t,
                            'stock_res': SSP3_dsm_res.s,
                            'inflow_res': SSP3_dsm_res.i,
                            'outflow_res': SSP3_dsm_res.o,
                            'stock_com': SSP3_dsm_com.s,
                            'inflow_com': SSP3_dsm_com.i,
                            'outflow_com': SSP3_dsm_com.o,
                            'stock_pub': SSP3_dsm_pub.s,
                            'inflow_pub': SSP3_dsm_pub.i,
                            'outflow_pub': SSP3_dsm_pub.o,
                            'stock_total': SSP3_dsm_res.s + SSP3_dsm_com.s + SSP3_dsm_pub.s,
                            'inflow_total': SSP3_dsm_res.i + SSP3_dsm_com.i + SSP3_dsm_pub.i,
                            'outflow_total': SSP3_dsm_res.o + SSP3_dsm_com.o + SSP3_dsm_pub.o
                            })
SSP4_dsm_df = pd.DataFrame({'time': SSP4_dsm_res.t,
                            'stock_res': SSP4_dsm_res.s,
                            'inflow_res': SSP4_dsm_res.i,
                            'outflow_res': SSP4_dsm_res.o,
                            'stock_com': SSP4_dsm_com.s,
                            'inflow_com': SSP4_dsm_com.i,
                            'outflow_com': SSP4_dsm_com.o,
                            'stock_pub': SSP4_dsm_pub.s,
                            'inflow_pub': SSP4_dsm_pub.i,
                            'outflow_pub': SSP4_dsm_pub.o,
                            'stock_total': SSP4_dsm_res.s + SSP4_dsm_com.s + SSP4_dsm_pub.s,
                            'inflow_total': SSP4_dsm_res.i + SSP4_dsm_com.i + SSP4_dsm_pub.i,
                            'outflow_total': SSP4_dsm_res.o + SSP4_dsm_com.o + SSP4_dsm_pub.o
                            })
SSP5_dsm_df = pd.DataFrame({'time': SSP5_dsm_res.t,
                            'stock_res': SSP5_dsm_res.s,
                            'inflow_res': SSP5_dsm_res.i,
                            'outflow_res': SSP5_dsm_res.o,
                            'stock_com': SSP5_dsm_com.s,
                            'inflow_com': SSP5_dsm_com.i,
                            'outflow_com': SSP5_dsm_com.o,
                            'stock_pub': SSP5_dsm_pub.s,
                            'inflow_pub': SSP5_dsm_pub.i,
                            'outflow_pub': SSP5_dsm_pub.o,
                            'stock_total': SSP5_dsm_res.s + SSP5_dsm_com.s + SSP5_dsm_pub.s,
                            'inflow_total': SSP5_dsm_res.i + SSP5_dsm_com.i + SSP5_dsm_pub.i,
                            'outflow_total': SSP5_dsm_res.o + SSP5_dsm_com.o + SSP5_dsm_pub.o
                            })

SSP1_sc_df = pd.DataFrame(SSP1_dsm_res.s_c + SSP1_dsm_com.s_c + SSP1_dsm_pub.s_c)
SSP2_sc_df = pd.DataFrame(SSP2_dsm_res.s_c + SSP2_dsm_com.s_c + SSP2_dsm_pub.s_c)
SSP3_sc_df = pd.DataFrame(SSP3_dsm_res.s_c + SSP3_dsm_com.s_c + SSP3_dsm_pub.s_c)
SSP4_sc_df = pd.DataFrame(SSP4_dsm_res.s_c + SSP4_dsm_com.s_c + SSP4_dsm_pub.s_c)
SSP5_sc_df = pd.DataFrame(SSP5_dsm_res.s_c + SSP5_dsm_com.s_c + SSP5_dsm_pub.s_c)


# write to excel
writer = pd.ExcelWriter('./Results/SSP_dsm.xlsx', engine='xlsxwriter')
SSP1_dsm_df.to_excel(writer, sheet_name='SSP1')
SSP2_dsm_df.to_excel(writer, sheet_name='SSP2')
SSP3_dsm_df.to_excel(writer, sheet_name='SSP3')
SSP4_dsm_df.to_excel(writer, sheet_name='SSP4')
SSP5_dsm_df.to_excel(writer, sheet_name='SSP5')
SSP1_sc_df.to_excel(writer, sheet_name='SSP1_sc', index=False)
SSP2_sc_df.to_excel(writer, sheet_name='SSP2_sc', index=False)
SSP3_sc_df.to_excel(writer, sheet_name='SSP3_sc', index=False)
SSP4_sc_df.to_excel(writer, sheet_name='SSP4_sc', index=False)
SSP5_sc_df.to_excel(writer, sheet_name='SSP5_sc', index=False)
writer.close()

# Plot the material flow analyses

# # ----------------------------------------------------------------------------------------------------------------------
# # Plot all scenarios together for all buildings
# --- plotting only: blank the 1997 cold-start point (the whole existing stock is
# --- dumped into year one); the Excel results above are unaffected.
for _d in [SSP1_dsm_res, SSP1_dsm_com, SSP1_dsm_pub, SSP2_dsm_res, SSP2_dsm_com, SSP2_dsm_pub,
           SSP3_dsm_res, SSP3_dsm_com, SSP3_dsm_pub, SSP4_dsm_res, SSP4_dsm_com, SSP4_dsm_pub]:
    _d.i[0] = np.nan; _d.o[0] = np.nan; _d.s[0] = np.nan
plot_MFA_all_same_graph = True
no_SSP5 = True      # True for ignoring SSP5, False for including SSP5
if plot_MFA_all_same_graph == True:
    plt.subplot(211)
    plt1, = plt.plot(SSP1_dsm_res.t, SSP1_dsm_res.s + SSP1_dsm_com.s + SSP1_dsm_pub.s)
    plt2, = plt.plot(SSP2_dsm_res.t, SSP2_dsm_res.s + SSP2_dsm_com.s + SSP2_dsm_pub.s)
    plt3, = plt.plot(SSP3_dsm_res.t, SSP3_dsm_res.s + SSP3_dsm_com.s + SSP3_dsm_pub.s)
    plt4, = plt.plot(SSP4_dsm_res.t, SSP4_dsm_res.s + SSP4_dsm_com.s + SSP4_dsm_pub.s)
    plt.axvline(base_year, color='k', linestyle='--')

    plt.legend([plt1, plt2, plt3, plt4], ['SSP1', 'SSP2', 'SSP3', 'SSP4'], loc=(1.05, 0.5))
    # plt.legend([plt1, plt2, plt3, plt4, plt5], ['SSP1', 'SSP2', 'SSP3', 'SSP4', 'SSP5'], loc=(1.05, 0.5))
    # plt.legend(loc=(1.05, 0.5))
    plt.xlabel('Year')
    plt.xlim(left=1980)
    plt.ylabel('million $m^2$')
    plt.title('Total Floor Space - Stock')
    # plt.show();

    plt.subplot(212)
    plt1, = plt.plot(SSP1_dsm_res.t, SSP1_dsm_res.i + SSP1_dsm_com.i + SSP1_dsm_pub.i, linestyle='dashed', color='#1f77b4')
    plt2, = plt.plot(SSP1_dsm_res.t, SSP1_dsm_res.o + SSP1_dsm_com.o + SSP1_dsm_pub.o, color = '#1f77b4')
    plt3, = plt.plot(SSP2_dsm_res.t, SSP2_dsm_res.i + SSP2_dsm_com.i + SSP2_dsm_pub.i, linestyle='dashed', color='#ff7f0e' )
    plt4, = plt.plot(SSP2_dsm_res.t, SSP2_dsm_res.o + SSP2_dsm_com.o + SSP2_dsm_pub.o, color='#ff7f0e')
    plt5, = plt.plot(SSP3_dsm_res.t, SSP3_dsm_res.i + SSP3_dsm_com.i + SSP3_dsm_pub.i, linestyle='dashed', color='#2ca02c')
    plt6, = plt.plot(SSP3_dsm_res.t, SSP3_dsm_res.o + SSP3_dsm_com.o + SSP3_dsm_pub.o, color='#2ca02c')
    plt7, = plt.plot(SSP4_dsm_res.t, SSP4_dsm_res.i + SSP4_dsm_com.i + SSP4_dsm_pub.i, linestyle='dashed', color='#d62728')
    plt8, = plt.plot(SSP4_dsm_res.t, SSP4_dsm_res.o + SSP4_dsm_com.o + SSP4_dsm_pub.o, color='#d62728')

    plt.axvline(base_year, color='k', linestyle='--')

    plt.legend([plt1, plt2, plt3, plt4, plt5, plt6, plt7, plt8],
               ['Inflow SSP1', 'Outflow SSP1',
                'Inflow SSP2', 'Outflow SSP2',
                'Inflow SSP3', 'Outflow SSP3',
                'Inflow SSP4', 'Outflow SSP4'], loc='center left', bbox_to_anchor=(1, 0.5))

    # plt.ylim(top=5000)
    # plt.xlim(left=SSP1_dsm_res.t[0] + 5)
    plt.xlim(left=1980)
    plt.xlabel('Year')
    plt.ylabel('million m$^2/year$')
    plt.title('Total Floor Space - Flows')
    plt.show();


# # Plot all scenarios together for residential buildings
plot_MFA_all_same_graph = True
no_SSP5 = True      # True for ignoring SSP5, False for including SSP5
if plot_MFA_all_same_graph == True:
    plt.subplot(211)
    plt1, = plt.plot(SSP1_dsm_res.t, SSP1_dsm_res.s)
    plt2, = plt.plot(SSP2_dsm_res.t, SSP2_dsm_res.s)
    plt3, = plt.plot(SSP3_dsm_res.t, SSP3_dsm_res.s)
    plt4, = plt.plot(SSP4_dsm_res.t, SSP4_dsm_res.s)
    plt.axvline(base_year, color='k', linestyle='--')
    if no_SSP5 == True:
        temp = 'bleh'
    else:
        plt5, = plt.plot(SSP5_dsm_res.t, SSP5_dsm_res.s)
    if no_SSP5 == True:
        plt.legend([plt1, plt2, plt3, plt4], ['SSP1', 'SSP2', 'SSP3', 'SSP4'], loc=(1.05, 0.5))
    else:
        plt.legend([plt1, plt2, plt3, plt4, plt5], ['SSP1', 'SSP2', 'SSP3', 'SSP4', 'SSP5'], loc=(1.05, 0.5))
    # plt.legend([plt1, plt2, plt3, plt4, plt5], ['SSP1', 'SSP2', 'SSP3', 'SSP4', 'SSP5'], loc=(1.05, 0.5))
    # plt.legend(loc=(1.05, 0.5))
    plt.xlabel('Year')
    plt.xlim(left=1980)
    plt.ylabel('million $m^2$')
    plt.title('Residential Floor Space - Stock')
    # plt.show();

    plt.subplot(212)
    plt1, = plt.plot(SSP1_dsm_res.t, SSP1_dsm_res.i, linestyle='dashed', color='#1f77b4')
    plt2, = plt.plot(SSP1_dsm_res.t, SSP1_dsm_res.o, color='#1f77b4')
    plt3, = plt.plot(SSP2_dsm_res.t, SSP2_dsm_res.i, linestyle='dashed', color='#ff7f0e' )
    plt4, = plt.plot(SSP2_dsm_res.t, SSP2_dsm_res.o, color='#ff7f0e' )
    plt5, = plt.plot(SSP3_dsm_res.t, SSP3_dsm_res.i, linestyle='dashed', color='#2ca02c')
    plt6, = plt.plot(SSP3_dsm_res.t, SSP3_dsm_res.o, color='#2ca02c')
    plt7, = plt.plot(SSP4_dsm_res.t, SSP4_dsm_res.i, linestyle='dashed', color='#d62728')
    plt8, = plt.plot(SSP4_dsm_res.t, SSP4_dsm_res.o, color='#d62728')
    if no_SSP5 == True:
        temp = 'bleh'
    else:
        plt9, = plt.plot(SSP5_dsm_res.t, SSP5_dsm_res.i, linestyle='dashed')
        plt0, = plt.plot(SSP5_dsm_res.t, SSP5_dsm_res.o)

    plt.axvline(base_year, color='k', linestyle='--')

    if no_SSP5 == True:
        plt.legend([plt1, plt2, plt3, plt4, plt5, plt6, plt7, plt8],
                   ['Inflow SSP1', 'Outflow SSP1',
                    'Inflow SSP2', 'Outflow SSP2',
                    'Inflow SSP3', 'Outflow SSP3',
                    'Inflow SSP4', 'Outflow SSP4'], loc='center left', bbox_to_anchor=(1, 0.5))
    else:
        plt.legend([plt1, plt2, plt3, plt4, plt5, plt6, plt7, plt8, plt9, plt0],
                   ['Inflow SSP1', 'Outflow SSP1',
                    'Inflow SSP2', 'Outflow SSP2',
                    'Inflow SSP3', 'Outflow SSP3',
                    'Inflow SSP4', 'Outflow SSP4',
                    'Inflow SSP5', 'Outflow SSP5'], loc='center left', bbox_to_anchor=(1, 0.5))
    # plt.ylim(top=5000)
    # plt.xlim(left=SSP1_dsm_res.t[0] + 5)
    plt.xlim(left=1980)
    plt.xlabel('Year')
    plt.ylabel('million m$^2/year$')
    plt.title('Residential Floor Space - Flows')
    plt.show();


# # Plot all scenarios together for commercial buildings
plot_MFA_all_same_graph = True
no_SSP5 = True      # True for ignoring SSP5, False for including SSP5
if plot_MFA_all_same_graph == True:
    plt.subplot(211)
    plt1, = plt.plot(SSP1_dsm_com.t, SSP1_dsm_com.s)
    plt2, = plt.plot(SSP2_dsm_com.t, SSP2_dsm_com.s)
    plt3, = plt.plot(SSP3_dsm_com.t, SSP3_dsm_com.s)
    plt4, = plt.plot(SSP4_dsm_com.t, SSP4_dsm_com.s)
    plt.axvline(base_year, color='k', linestyle='--')
    if no_SSP5 == True:
        temp = 'bleh'
    else:
        plt5, = plt.plot(SSP5_dsm_com.t, SSP5_dsm_com.s)
    if no_SSP5 == True:
        plt.legend([plt1, plt2, plt3, plt4], ['SSP1', 'SSP2', 'SSP3', 'SSP4'], loc=(1.05, 0.5))
    else:
        plt.legend([plt1, plt2, plt3, plt4, plt5], ['SSP1', 'SSP2', 'SSP3', 'SSP4', 'SSP5'], loc=(1.05, 0.5))
    # plt.legend([plt1, plt2, plt3, plt4, plt5], ['SSP1', 'SSP2', 'SSP3', 'SSP4', 'SSP5'], loc=(1.05, 0.5))
    # plt.legend(loc=(1.05, 0.5))
    plt.xlim(left=1980)
    plt.xlabel('Year')
    plt.ylabel('million $m^2$')
    plt.title('Commercial Floor Space - Stock')
    # plt.show();

    plt.subplot(212)
    plt1, = plt.plot(SSP1_dsm_com.t, SSP1_dsm_com.i, linestyle='dashed', color='#1f77b4')
    plt2, = plt.plot(SSP1_dsm_com.t, SSP1_dsm_com.o, color='#1f77b4')
    plt3, = plt.plot(SSP2_dsm_com.t, SSP2_dsm_com.i, linestyle='dashed', color='#ff7f0e' )
    plt4, = plt.plot(SSP2_dsm_com.t, SSP2_dsm_com.o, color='#ff7f0e' )
    plt5, = plt.plot(SSP3_dsm_com.t, SSP3_dsm_com.i, linestyle='dashed',color='#2ca02c')
    plt6, = plt.plot(SSP3_dsm_com.t, SSP3_dsm_com.o, color='#2ca02c')
    plt7, = plt.plot(SSP4_dsm_com.t, SSP4_dsm_com.i, linestyle='dashed', color='#d62728')
    plt8, = plt.plot(SSP4_dsm_com.t, SSP4_dsm_com.o, color='#d62728')
    if no_SSP5 == True:
        temp = 'bleh'
    else:
        plt9, = plt.plot(SSP5_dsm_com.t, SSP5_dsm_com.i, linestyle='dashed')
        plt0, = plt.plot(SSP5_dsm_com.t, SSP5_dsm_com.o)

    plt.axvline(base_year, color='k', linestyle='--')

    if no_SSP5 == True:
        plt.legend([plt1, plt2, plt3, plt4, plt5, plt6, plt7, plt8],
                   ['Inflow SSP1', 'Outflow SSP1',
                    'Inflow SSP2', 'Outflow SSP2',
                    'Inflow SSP3', 'Outflow SSP3',
                    'Inflow SSP4', 'Outflow SSP4'], loc='center left', bbox_to_anchor=(1, 0.5))
    else:
        plt.legend([plt1, plt2, plt3, plt4, plt5, plt6, plt7, plt8, plt9, plt0],
                   ['Inflow SSP1', 'Outflow SSP1',
                    'Inflow SSP2', 'Outflow SSP2',
                    'Inflow SSP3', 'Outflow SSP3',
                    'Inflow SSP4', 'Outflow SSP4',
                    'Inflow SSP5', 'Outflow SSP5'], loc='center left', bbox_to_anchor=(1, 0.5))
    # plt.ylim(top=5000)
    # plt.xlim(left=SSP1_dsm_com.t[0] + 5)
    plt.xlim(left=1980)
    plt.xlabel('Year')
    plt.ylabel('million m$^2/year$')
    plt.title('Commercial Floor Space - Flows')
    plt.show();


# # Plot all scenarios together for public buildings
plot_MFA_all_same_graph = True
no_SSP5 = True      # True for ignoring SSP5, False for including SSP5
if plot_MFA_all_same_graph == True:
    plt.subplot(211)
    plt1, = plt.plot(SSP1_dsm_pub.t, SSP1_dsm_pub.s)
    plt2, = plt.plot(SSP2_dsm_pub.t, SSP2_dsm_pub.s)
    plt3, = plt.plot(SSP3_dsm_pub.t, SSP3_dsm_pub.s)
    plt4, = plt.plot(SSP4_dsm_pub.t, SSP4_dsm_pub.s)
    plt.axvline(base_year, color='k', linestyle='--')
    if no_SSP5 == True:
        temp = 'bleh'
    else:
        plt5, = plt.plot(SSP5_dsm_pub.t, SSP5_dsm_pub.s)
    if no_SSP5 == True:
        plt.legend([plt1, plt2, plt3, plt4], ['SSP1', 'SSP2', 'SSP3', 'SSP4'], loc=(1.05, 0.5))
    else:
        plt.legend([plt1, plt2, plt3, plt4, plt5], ['SSP1', 'SSP2', 'SSP3', 'SSP4', 'SSP5'], loc=(1.05, 0.5))
    # plt.legend([plt1, plt2, plt3, plt4, plt5], ['SSP1', 'SSP2', 'SSP3', 'SSP4', 'SSP5'], loc=(1.05, 0.5))
    # plt.legend(loc=(1.05, 0.5))
    plt.xlabel('Year')
    plt.xlim(left=1980)
    plt.ylabel('million $m^2$ ')
    plt.title('Public Floor Space - Stock')
    # plt.show();

    plt.subplot(212)
    plt1, = plt.plot(SSP1_dsm_pub.t, SSP1_dsm_pub.i, linestyle='dashed', color='#1f77b4')
    plt2, = plt.plot(SSP1_dsm_pub.t, SSP1_dsm_pub.o, color='#1f77b4')
    plt3, = plt.plot(SSP2_dsm_pub.t, SSP2_dsm_pub.i, linestyle='dashed', color='#ff7f0e' )
    plt4, = plt.plot(SSP2_dsm_pub.t, SSP2_dsm_pub.o, color='#ff7f0e' )
    plt5, = plt.plot(SSP3_dsm_pub.t, SSP3_dsm_pub.i, linestyle='dashed', color='#2ca02c')
    plt6, = plt.plot(SSP3_dsm_pub.t, SSP3_dsm_pub.o, color='#2ca02c')
    plt7, = plt.plot(SSP4_dsm_pub.t, SSP4_dsm_pub.i, linestyle='dashed', color='#d62728')
    plt8, = plt.plot(SSP4_dsm_pub.t, SSP4_dsm_pub.o, color='#d62728')
    if no_SSP5 == True:
        temp = 'bleh'
    else:
        plt9, = plt.plot(SSP5_dsm_pub.t, SSP5_dsm_pub.i, linestyle='dashed')
        plt0, = plt.plot(SSP5_dsm_pub.t, SSP5_dsm_pub.o)

    plt.axvline(base_year, color='k', linestyle='--')

    if no_SSP5 == True:
        plt.legend([plt1, plt2, plt3, plt4, plt5, plt6, plt7, plt8],
                   ['Inflow SSP1', 'Outflow SSP1',
                    'Inflow SSP2', 'Outflow SSP2',
                    'Inflow SSP3', 'Outflow SSP3',
                    'Inflow SSP4', 'Outflow SSP4'], loc='center left', bbox_to_anchor=(1, 0.5))
    else:
        plt.legend([plt1, plt2, plt3, plt4, plt5, plt6, plt7, plt8, plt9, plt0],
                   ['Inflow SSP1', 'Outflow SSP1',
                    'Inflow SSP2', 'Outflow SSP2',
                    'Inflow SSP3', 'Outflow SSP3',
                    'Inflow SSP4', 'Outflow SSP4',
                    'Inflow SSP5', 'Outflow SSP5'], loc='center left', bbox_to_anchor=(1, 0.5))
    # plt.ylim(top=5000)
    # plt.xlim(left=SSP1_dsm_pub.t[0] + 5)
    plt.xlim(left=1980)
    plt.xlabel('Year')
    plt.ylabel('million m$^2/year$')
    plt.title('Public Floor Space - Flows')
    plt.show();
