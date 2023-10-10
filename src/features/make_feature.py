import logging

import pandas as pd
import numpy as np
from src.utils import config
from src.utils import colours
#from src.utils.connect import DatabaseModelsClass
from src.data.get_data import GetDataTemplate
from src.visualization import visualize
import os


class MakeCharts:
    """ Class to make features of income statement. """
    logger = logging.getLogger(f"{__name__}.MakeFeatures")

    def make_chart_bar(self, df, tracevar, xvar, yvar, title, popcount, barcol=True):
        xaxes = []
        yaxes = []
        names = []
        text = []
        cols = []

        for count, var in enumerate(df[f"{tracevar}"].unique()):
            dft = df[df[f"{tracevar}"] == var]
            xaxes.append(list(dft[f"{xvar}"]))
            yaxes.append(list(dft[f"{yvar}"]))
            names.append(var)
            text.append(list(dft[f"{yvar}"]))
            if barcol:
                cols.append(colours.COLOURS[((count + 1) * 10)])
            else: 
                cols.append(colours.COLOURS[10])

        data = {
            'xaxes'   : xaxes,
            'yaxes'   : yaxes,
            'names'   : names,
            'text'    : text,
            'colours' : cols
        }

        metadata = {
            'yaxis'   : {'name': yvar, 'uom': config.UOM[yvar]},
            'xaxis'   : {'name': xvar, 'uom': config.UOM[xvar]},
            'heading' : title,
            'popcount': popcount,
            'showlegend': True
        }   

        
        viz = visualize.VizBar()
        fig = viz.verticalbar(data, metadata)

        return fig
    
    def make_chart_scatter(self, df, tracevar, xvar, yvar, title):

        xaxes = []
        yaxes = []
        names = []
        cols = []

        for count, var in enumerate(df[f"{tracevar}"].unique()):
            dft = df[df[f"{tracevar}"] == var]
            xaxes.append(list(dft[f"{xvar}"]))
            yaxes.append(list(dft[f"{yvar}"]))
            names.append(var)
            cols.append(colours.COLOURS[((count + 1) * 10)])

        data = {
            'xaxes'   : xaxes,
            'yaxes'   : yaxes,
            'names'   : names,
            'colours' : cols
        }

        metadata = {
            'yaxis'   : {'name': yvar, 'uom': config.UOM[yvar]},
            'xaxis'   : {'name': xvar, 'uom': config.UOM[xvar]},
            'heading' : title,
            'popcount': len(df),
            'mode'    : 'markers',
        }   

        viz = visualize.VizScatter()
        fig = viz.scatterplot(data, metadata)

        return fig

    def make_chart_box(self, df, tracevar, yvar, title, popcount):

        yaxes = []
        names = []
        text = []
        cols = []

        for count, var in enumerate(df[f"{tracevar}"].unique()):
            dft = df[df[f"{tracevar}"] == var]
            yaxes.append(list(dft[f"{yvar}"]))
            names.append(var)
            text.append(list(dft[f"{yvar}"]))
            cols.append(colours.COLOURS[((count + 1) * 10)])

        data = {
            'yaxes'   : yaxes,
            'names'   : names,
            'text'    : text,
            'colours' : cols
        }

        metadata = {
            'yaxis'   : {'name': yvar, 'uom': config.UOM[yvar]},
            'heading' : title,
            'popcount': popcount,
        }   

        viz = visualize.VizBox()
        fig = viz.distrboxplot(data, metadata)

        return fig

    def make_chart_splom(self, df, tracevar, dimlist, title, colsdic):
        print(colsdic)

        #yaxes = []
        dimensions = []
        names = []
        text = []
        markers = []

        for count, var in enumerate(df[f"{tracevar}"].unique()):
            print(var)
            dft = df[df[f"{tracevar}"] == var]

            _d = []
            for dim in dimlist:
                _d.append(
                    dict(label=dim,
                        values=dft[dim])
                )
            dimensions.append(_d)
            names.append(var)
            # marker=dict(color=colours.COLOURS[((count + 1 ) * 10)],
            #             showscale=False,  # colors encode categorical variables
            #             line_color='white', line_width=0.5)
            marker=dict(color=colsdic[var],
                        showscale=False,  # colors encode categorical variables
                        line_color='white', line_width=0.5)
            markers.append(marker)

        data = {
            'dimensions': dimensions,
            'names'   : names,
            'text'    : text,
            'markers' : markers
        }

        metadata = {
            'heading' : title,
            'popcount': len(df),
        }   

        viz = visualize.VizSplom()
        fig = viz.splom(data, metadata)
        return fig

    def make_chart_heatmap(self, df, dimlist):

        for col in dimlist:
            df[col] = df[col].astype(float)

        df_hm = df[dimlist]

        viz = visualize.VizSplom()
        fig = viz.heatmap(df_hm)
        return fig

    def make_chart_sankey(self, df):

        df_sankey  = df[['Hb', 'Hb Term']]

        a_a = np.sum(df_sankey['Hb'] <= 120)
        a_n_a = np.sum(df_sankey['Hb'] > 120)
        a_nan = df_sankey['Hb'].isnull().sum()
        #print(f"{a_a}-{a_n_a}-{a_nan}")

        df_sankey2 = df_sankey[df_sankey['Hb'] <= 120]
        b_a = np.sum(df_sankey2['Hb Term'] <= 120)
        b_n_a = np.sum(df_sankey2['Hb Term'] > 120)
        b_nan = df_sankey2['Hb Term'].isnull().sum()
        #print(f"{b_a}-{b_n_a}-{b_nan}")

        #labels = ['Patients',  
        #          'Hb <= 120', 'Hb > 120', 'Not measured',
        #          'Anemic at Term', 'Cleared', 'Not measured']

        #source=[0, 0, 0, 1, 1, 1],
        #target=[1, 2, 3, 4, 5, 6],
        #value=[a_a, a_n_a, a_nan, b_a, b_n_a, b_nan]  

        #viz = visualize.VizSankey()
        #fig = viz.sankey(labels, source, target, value)
        return fig

    def age_bar(self, dft):
        df = dft[['Age', 'Race']].reset_index(drop=True)
        df.loc[df['Age'] < 35, 'Age Category'] = '< 35'
        df.loc[(df['Age'] > 35) & (df['Age'] <= 40), 'Age Category'] = '35 - 40'
        df.loc[(df['Age'] > 40) & (df['Age'] <= 45), 'Age Category'] = '40 - 45'
        df.loc[df['Age'] > 45, 'Age Category'] = '> 45'

        age = df.groupby(['Age Category', 'Race']).size().reset_index(name='Counts')

        age.loc[age['Age Category'] == '< 35', 'Sort'] = 10
        age.loc[age['Age Category'] == '35 - 40', 'Sort'] = 20
        age.loc[age['Age Category'] == '40 - 45', 'Sort'] = 30
        age.loc[age['Age Category'] == '> 45', 'Sort'] = 40

        age = age.sort_values(by=['Sort'])
        age['Percentage'] = round(age['Counts'] / len(df) * 100, 2)

        fig = self.make_chart_bar(age, 'Race', 'Age Category', 'Percentage', 'Age Distribution', len(df))

        return fig
    
    def race_bar(self, df):
        race = df.groupby(['Race']).size().reset_index(name='Counts')
        race = race.sort_values(by=['Counts'], ascending=False)
        race['Percentage'] = round(race['Counts'] / len(df) * 100, 2)

        fig = self.make_chart_bar(race, 'Race', 'Race', 'Percentage', 'Race Distribution', len(df))

        return fig
    
    def parity_bar(self, df):
        par = df.groupby(['Parity']).size().reset_index(name='Counts')
        par['Percentage'] = round(par['Counts']/par['Counts'].sum() * 100)

        par['Parity'] = par['Parity'].astype(str)

        fig = self.make_chart_bar(par, 'Parity', 'Parity', 'Percentage', 'Parity Distribution', 
                                  len(df), barcol=False)

        return fig
    
    def bmi_bar(self, df):
        dft = df[['BMI', 'Race']].reset_index(drop=True)

        dft.loc[dft['BMI'] <= 18, 'BMI Category'] = '< 18'
        dft.loc[(dft['BMI'] > 18) & (dft['BMI'] <= 25), 'BMI Category'] = '18-25'
        dft.loc[(dft['BMI'] > 25) & (dft['BMI'] <= 30), 'BMI Category'] = '25-30'
        dft.loc[(dft['BMI'] > 30) & (dft['BMI'] <= 35), 'BMI Category'] = '30-35'
        dft.loc[dft['BMI'] > 35, 'BMI Category'] = '> 35'

        dft = dft.groupby(['BMI Category', 'Race']).size().reset_index(name='Counts')

        dft.loc[dft['BMI Category'] == '< 18', 'Sort'] = 10
        dft.loc[dft['BMI Category'] == '18-25', 'Sort'] = 20
        dft.loc[dft['BMI Category'] == '25-30', 'Sort'] = 30
        dft.loc[dft['BMI Category'] == '30-35', 'Sort'] = 40
        dft.loc[dft['BMI Category'] == '> 35', 'Sort'] = 40

        dft = dft.sort_values(by=['Sort'])
        dft['Percentage'] = round(dft['Counts'] / len(df) * 100, 2)

        fig = self.make_chart_bar(dft, 'Race', 'BMI Category', 'Percentage', 'BMI Distribution', len(df))

        return fig
    
    def bmi_box(self, df):
        dfcats = df[['BMI', 'Race']]

        dfall = dfcats.copy()
        dfall['Race'] = 'All'

        dfchart = pd.concat([dfcats, dfall])

        fig = self.make_chart_box(dfchart, 'Race', 'BMI', 'BMI Spread by Race', len(df))
        
        return fig
    
    def hba1c_race_bar(self, df):
        dfcat = df[['HbA1C', 'Race']].reset_index(drop=True)

        dfcat.loc[dfcat['HbA1C'] < 38, 'HbA1C Category'] = '< 38'
        dfcat.loc[(dfcat['HbA1C'] >= 38) & (dfcat['HbA1C'] < 47), 'HbA1C Category'] = '39 - 47'
        dfcat.loc[dfcat['HbA1C'] >= 47, 'HbA1C Category'] = '> 48'

        dft = dfcat.groupby(['HbA1C Category', 'Race']).size().reset_index(name='Counts')
        dft.loc[dft['HbA1C Category'] == '< 38', 'Sort'] = 10
        dft.loc[dft['HbA1C Category'] == '39 - 47', 'Sort'] = 20
        dft.loc[dft['HbA1C Category'] == '> 48', 'Sort'] = 30

        dft = dft.sort_values(by=['Sort'])
        dft['Percentage'] = round(dft['Counts'] / len(df) * 100, 2)

        fig = self.make_chart_bar(dft, 'Race', 'HbA1C Category', 'Percentage', 'HbA1C Distribution by Race', len(df))

        return fig

    def hba1c_bar(self, df):
        dfcat = df[['HbA1C']].reset_index(drop=True)

        dfcat.loc[dfcat['HbA1C'] < 38, 'HbA1C Category'] = '< 38'
        dfcat.loc[(dfcat['HbA1C'] >= 38) & (dfcat['HbA1C'] < 47), 'HbA1C Category'] = '39 - 47'
        dfcat.loc[dfcat['HbA1C'] >= 47, 'HbA1C Category'] = '> 48'

        dft = dfcat.groupby(['HbA1C Category']).size().reset_index(name='Counts')
        dft.loc[dft['HbA1C Category'] == '< 38', 'Sort'] = 10
        dft.loc[dft['HbA1C Category'] == '39 - 47', 'Sort'] = 20
        dft.loc[dft['HbA1C Category'] == '> 48', 'Sort'] = 30

        dft = dft.sort_values(by=['Sort'])
        dft['Percentage'] = round(dft['Counts'] / len(df) * 100, 2)

        fig = self.make_chart_bar(dft, 'HbA1C Category', 'HbA1C Category', 'Percentage', 'HbA1C Distribution', len(df), barcol=False)

        return fig

    def hba1c_splom(self, df):
        cols = ['HbA1C', 'eGFR', 'Age', 'Hb', 'ALT', 'ACR', 'MAP']
        dfcat = df[cols].reset_index(drop=True)
        dfcat = dfcat

        dfcat.loc[dfcat['HbA1C'] < 38, 'HbA1C Category'] = '< 38'
        dfcat.loc[(dfcat['HbA1C'] >= 38) & (dfcat['HbA1C'] < 47), 'HbA1C Category'] = '39 - 47'
        dfcat.loc[dfcat['HbA1C'] >= 47, 'HbA1C Category'] = '> 48'

        colsdic = {
            '< 38': colours.COLOURS[10],
            '39 - 47': colours.COLOURS[40],
            '> 48': colours.COLOURS[100]

        }

        fig = self.make_chart_splom(dfcat, 'HbA1C Category', cols, 'HbA1C Relationships', colsdic)

        fig2 = self.make_chart_heatmap(df, cols)

        return fig

    def hba1c_box(self, df):
        dfcats = df[['HbA1C', 'Race']]

        dfall = dfcats.copy()
        dfall['Race'] = 'All'

        dfchart = pd.concat([dfcats, dfall])

        fig = self.make_chart_box(dfchart, 'Race', 'HbA1C', 'HbA1C Spread by Race', len(df))
        
        return fig
   
    def hb_bar(self, df):
        dfcat = df[['Hb']].reset_index(drop=True)

        dfcat['Hb120'] = 0
        dfcat.loc[df['Hb'] < 120, 'Hb120'] = 1

        #df['Hb Category'] = 0
        dfcat.loc[df['Hb'] <= 100, 'Hb Category'] = '<= 100'
        dfcat.loc[(df['Hb'] > 100) & (dfcat['Hb'] <= 120), 'Hb Category'] = '100 - 120'
        dfcat.loc[(dfcat['Hb'] > 120), 'Hb Category'] = '> 120'

        dft = dfcat.groupby(['Hb Category']).size().reset_index(name='Counts')
        dft.loc[dft['Hb Category'] == '<= 100', 'Sort'] = 10
        dft.loc[dft['Hb Category'] == '100 - 120', 'Sort'] = 20
        dft.loc[dft['Hb Category'] == '> 120', 'Sort'] = 30

        dft = dft.sort_values(by=['Sort'])
        dft['Percentage'] = round(dft['Counts'] / len(df) * 100, 2)

        fig = self.make_chart_bar(dft, 'Hb Category', 'Hb Category', 'Percentage', 'Hb Category Distribution', len(df), barcol=False)

        return fig

    def hb_box(self, df):
        dfcats = df[['Hb', 'Race']]

        dfall = dfcats.copy()
        dfall['Race'] = 'All'

        dfchart = pd.concat([dfcats, dfall])

        fig = self.make_chart_box(dfchart, 'Race', 'Hb', 'Hb Spread by Race', len(df))
        
        return fig
   
    def egfr_splom(self, df):
        cols = ['HbA1C', 'eGFR', 'Age', 'Hb', 'ALT', 'ACR']
        dfcat = df[cols].reset_index(drop=True)

        dfcat.loc[dfcat['eGFR'] <= 90, 'eGFR Category'] = '<= 90'
        dfcat.loc[dfcat['eGFR'] > 90,  'eGFR Category'] = '> 90'

        colsdic = {
            '> 90': colours.COLOURS[10],
            '<= 90': colours.COLOURS[100]

        }

        #dimlist = cols.remove('Id')
        fig = self.make_chart_splom(dfcat, 'eGFR Category', cols, 'eGFR Relationships', colsdic)

        return fig

    def egfr_box(self, df):
        dfcats = df[['eGFR', 'Race']]

        dfall = dfcats.copy()
        dfall['Race'] = 'All'

        dfchart = pd.concat([dfcats, dfall])

        fig = self.make_chart_box(dfchart, 'Race', 'eGFR', 'eGFR Spread by Race', len(df))
        
        return fig
  
    def bmi_muac_scatter(self, df):
        dfc = df[['BMI', 'MUAC', 'Race']]

        fig = self.make_chart_scatter(dfc, 'Race', 'BMI', 'MUAC', 'BMI vs MUAC')
        
        return fig

    def hba1c_randgluc_scatter(self, df):
        dfc = df[['HbA1C', 'RandomGlucose', 'Race']]

        fig = self.make_chart_scatter(dfc, 'Race', 'HbA1C', 'RandomGlucose', 'HbA1C vs Random Glucose')
        
        return fig

    def syst_bmi_scatter(self, df):
        dfc = df[['Systolic', 'Diastolic', 'BMI', 'eGFR', 'MAP']]
        dfc['Cat'] = 'All'

        #fig = self.make_chart_scatter(dfc, 'Cat', 'Systolic', 'BMI', 'Systolic vs BMI')
        fig = self.make_chart_scatter(dfc, 'Cat', 'MAP', 'BMI', 'MAP vs BMI')
        fig = self.make_chart_scatter(dfc, 'Cat', 'MAP', 'eGFR', 'MAP vs eGFR')
        #fig = self.make_chart_scatter(dfc, 'Cat', 'Diastolic', 'eGFR', 'Diastolic vs eGFR')

        return fig

    def anemia_cascade(self, df):

        df_c  = df[['Hb', 'Hb Term']]

        a_a = np.sum(df_c['Hb'] <= 120)
        a_n_a = np.sum(df_c['Hb'] > 120)
        a_nan = df_c['Hb'].isnull().sum()

        df_c2 = df_c[df_c['Hb'] <= 120]
        b_a = np.sum(df_c2['Hb Term'] <= 105)
        b_n_a = np.sum(df_c2['Hb Term'] > 105)
        b_nan = df_c2['Hb Term'].isnull().sum()

        data = [['Patients', '1', len(df), f'Patients<br>({len(df)})', colours.COLOURS[10]],
                ['Visit 1', '3', a_n_a, f'> 120<br>({a_n_a})', colours.COLOURS[20]],
                ['Visit 1', '2', a_nan, f'Not measured<br>({a_nan})', '#c4c4c4'],
                ['Visit 1', '1', a_a, f'<= 120<br>({a_a})', colours.COLOURS[100]],
                ['Term', '2', a_nan + a_n_a, f'Cleared<br>({a_nan + a_n_a})', colours.PLOTBACKGROUND],
                ['Term', '3', b_nan, f'Not measured ({b_nan})','#c4c4c4'],
                ['Term', '1', b_a, f'<= 105 ({b_a})', colours.COLOURS[100]],
                ['Term', '1', b_n_a, f'> 105<br>({b_n_a})', colours.COLOURS[20]]]
        
        dfm = pd.DataFrame(data=data, columns=['Bars', 'Hb', 'Count', 'Text', 'Colour'])

        xaxes = []
        yaxes = []
        names = []
        text = []
        cols = []

        for count, var in enumerate(dfm['Hb'].unique()):
            dft = dfm[dfm['Hb'] == var]
            xaxes.append(list(dft['Bars']))
            yaxes.append(list(dft['Count']))
            names.append(var)
            text.append(list(dft['Text']))
            cols.append(list(dft['Colour']))


        data = {
            'xaxes'   : xaxes,
            'yaxes'   : yaxes,
            'names'   : names,
            'text'    : text,
            'colours' : cols
        }

        metadata = {
            'yaxis'   : {'name': 'Count', 'uom': config.UOM['Count']},
            'xaxis'   : {'name': '', 'uom': ''},
            'heading' : 'Cascade of Anemic Patients at First Visit and Term',
            'popcount': len(df),
            'showlegend': False
        }   

        
        viz = visualize.VizBar()
        fig = viz.verticalbar(data, metadata)


        #self.make_chart_bar(dft, 'Hb', 'Bars', 'Count', 'title', len(df))

        return 


class MakeAnalysis:
    """ Class to make features of income statement. """
    logger = logging.getLogger(f"{__name__}.MakeAnalysis")
    gt = GetDataTemplate()
    mc = MakeCharts()

    def manage(self):
        self.logger.info(f"manage")
        #df=self.gt.get_excel_WELLMUM(True)

        self.population_description()
        self.disease_description_hba1c()

        return 
 
    def population_description(self):
        df=self.gt.get_excel_WELLMUM()

        # Age
        self.mc.age_bar(df)

        # Race
        self.mc.race_bar(df)

        # Parity
        self.mc.parity_bar(df)

        # BMI
        self.mc.bmi_bar(df)
        self.mc.bmi_box(df)

        return

    def disease_description_hba1c(self):

        df=self.gt.get_excel_WELLMUM()

        #########################
        # Diabetes
        ## HbA1C
        #########################

        ## HbA1C 
        self.mc.hba1c_bar(df)
        
        ## HbA1C by Race
        self.mc.hba1c_race_bar(df)

        ## HbA1C by Correlation
        self.mc.hba1c_splom(df)

        ## HbA1C Spread
        self.mc.hba1c_box(df)

        return

    def disease_description_anemia(self):

        df=self.gt.get_excel_WELLMUM()
        #########################
        # Anemia
        ## Hb
        #########################
        #self.mc.make_chart_sankey(df)
        self.mc.anemia_cascade(df)

        ## Hb
        self.mc.hb_bar(df)

        ## Hb by Race

        ## Hb by Correlation

        ## Spread
        self.mc.hb_box(df)
        return

    def disease_description_renal(self):

        df=self.gt.get_excel_WELLMUM()
        #########################
        # Renal
        ## Creatinine
        ## EGFR
        #########################

        ## EGFR
        #self.mc.hba1c_bar(df)

        ## EGFR by Race
        #self.mc.hba1c_race_bar(df)

        ## EGFR by Correlation
        self.mc.egfr_splom(df)

        ## Spread
        self.mc.egfr_box(df)

        return

    def disease_relationships(self):

        df=self.gt.get_excel_WELLMUM()

        #########################
        # Correlations
        #########################

        ## HbA1C vs Random Glucose
        self.mc.bmi_muac_scatter(df)

        ## MUAC vs BMI
        #self.mc.hba1c_randgluc_scatter(df)

        ## Systolic vs BMI
        self.mc.syst_bmi_scatter(df)

        return
    
    def make_readme(self):
        files = os.listdir(os.path.join(config.FIGFOLDER))
        f = open('readme.md', 'w')

        for file in files:

            fig = f"""<img src="images/202310/{file}"  width="250">"""
            f.write(fig)
            #print(fig)

        f.close()

        return