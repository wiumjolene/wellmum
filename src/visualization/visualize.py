import logging
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os

from src.utils import colours
from src.utils import config


class VizScatter:
    logger = logging.getLogger(f"{__name__}.VizScatter")
    """
    https://plotly.com/python-api-reference/generated/plotly.graph_objects.Scatter.html
    https://plotly.com/python/line-and-scatter/
    """

    def scatterplot(self, data, metadata):
        """ 
        data = {'xaxes': [[x,x,x,x,x],[x,x,x,x,x],[x,x,x,x,x],[x,x,x,x,x]],
                'yaxes': [[y,y,y,y,y],[y,y,y,y,y],[y,y,y,y,y],[y,y,y,y,y]],
                'names': ['name','name','name','name'],
                'colours': [colour,colour,colour,colour]
        }
        metadata = {
            'yaxis':{'name':'name', 'uom':'uom'},
            'xaxis':{'name':'name', 'uom':'uom'},
            'heading':'heading',
            'popcount':'popcount',
            'mode':'mode'
        }    
        """
        self.logger.debug(f"- scatterplot")

        fig = go.Figure()

        # Add traces
        for count, vals in enumerate(data['names']):

            fig.add_trace(go.Scatter(x=data['xaxes'][count], 
                                        y=data['yaxes'][count],
                                        mode=metadata['mode'],
                                        name=vals,
                                        marker_color=data['colours'][count])
                        )

        fig.update_traces(marker_line_width=0.3, marker_size=10)

        fig.update_layout(
            title=go.layout.Title(
                text=f"{metadata['heading']}<br><sup><i>(n={metadata['popcount']})</i></sup>",
                #text=f"{metadata['heading']}",
                xref="paper",
                x=0
            ),
            xaxis=go.layout.XAxis(
                title=go.layout.xaxis.Title(
                    text=f"{metadata['xaxis']['name']}<br><sup><i>{metadata['xaxis']['uom']}</i></sup>"
                )
            ),
            yaxis=go.layout.YAxis(
                title=go.layout.yaxis.Title(
                    text=f"{metadata['yaxis']['name']}<br><sup><i>{metadata['yaxis']['uom']}</i></sup>"
                ),
                gridcolor=colours.GRIDCOLOUR
            ),
            paper_bgcolor = colours.PAPERBACKGROUND,
            plot_bgcolor=colours.PLOTBACKGROUND,
        )
        fig.show()
        figpath = os.path.join(config.FIGFOLDER, f"{metadata['heading']}.jpeg")
        fig.write_image(figpath)
        return fig
 

class VizBar:
    logger = logging.getLogger(f"{__name__}.VizBar")
    """
    https://plotly.com/python-api-reference/generated/plotly.graph_objects.Bar.html
    https://plotly.com/python/bar-charts/
    """

    def verticalbar(self, data, metadata):
        """ 
        data = {'xaxes': [[x,x,x,x,x],[x,x,x,x,x],[x,x,x,x,x],[x,x,x,x,x]],
                'yaxes': [[y,y,y,y,y],[y,y,y,y,y],[y,y,y,y,y],[y,y,y,y,y]],
                'names': ['name','name','name','name'],
                'text': [[y,y,y,y,y],[y,y,y,y,y],[y,y,y,y,y],[y,y,y,y,y]],
                'colours': [colour,colour,colour,colour]
        }
        metadata = {
            'yaxis':{'name':'name', 'uom':'uom'},
            'xaxis':{'name':'name', 'uom':'uom'},
            'heading':'heading',
            'popcount':'popcount',
            'showlegend: 'showlegend',
        }    
        """
        self.logger.debug(f"- verticalbar")

        fig = go.Figure()

        # Add traces
        for count, vals in enumerate(data['names']):

            fig.add_trace(go.Bar(x=data['xaxes'][count], 
                                        y=data['yaxes'][count],
                                        text=data['text'][count],
                                        name=vals,
                                        marker_color=data['colours'][count])
                        )

        fig.update_layout(
            title=go.layout.Title(
                text=f"{metadata['heading']}<br><sup><i>(n={metadata['popcount']})</i></sup>",
                #text=f"{metadata['heading']}",
                xref="paper",
                x=0
            ),
            xaxis=go.layout.XAxis(
                title=go.layout.xaxis.Title(
                    text=f"{metadata['xaxis']['name']}<br><sup><i>{metadata['xaxis']['uom']}</i></sup>"
                )
            ),
            yaxis=go.layout.YAxis(
                title=go.layout.yaxis.Title(
                    text=f"{metadata['yaxis']['name']}<br><sup><i>{metadata['yaxis']['uom']}</i></sup>"
                ),
                gridcolor=colours.GRIDCOLOUR
            ),
            barmode='stack',
            paper_bgcolor = colours.PAPERBACKGROUND,
            uniformtext=dict(mode="hide", minsize=10),
            showlegend = metadata['showlegend'],
            plot_bgcolor=colours.PLOTBACKGROUND,
        )
        fig.show()
        figpath = os.path.join(config.FIGFOLDER, f"{metadata['heading']}.jpeg")
        fig.write_image(figpath)
        return fig
    

class VizBox:
    logger = logging.getLogger(f"{__name__}.VizBox")
    """
    https://plotly.com/python-api-reference/generated/plotly.graph_objects.Bar.html
    https://plotly.com/python/bar-charts/
    """

    def distrboxplot(self, data, metadata):
        """ 
        data = {
                'yaxes': [[y,y,y,y,y],[y,y,y,y,y],[y,y,y,y,y],[y,y,y,y,y]],
                'names': ['name','name','name','name'],
                'colours': [colour,colour,colour,colour]
        }
        metadata = {
            'yaxis':{'name':'name', 'uom':'uom'},
            'xaxis':{'name':'name', 'uom':'uom'},
            'heading':'heading',
            'popcount':'popcount',
            'mode':'mode'
        }    
        """
        self.logger.debug(f"- scatterplot")

        fig = go.Figure()

        # Add traces
        for count, vals in enumerate(data['names']):

            fig.add_trace(go.Box(y=data['yaxes'][count],
                                    marker_color=data['colours'][count],
                                    name=vals,
                                    notched=True,
                                    jitter=0.3,
                                    pointpos=-1.8,
                                    boxpoints='all',  # represent all points
                                        )
                        )

        fig.update_layout(
            title=go.layout.Title(
                text=f"{metadata['heading']}<br><sup><i>(n={metadata['popcount']})</i></sup>",
                #text=f"{metadata['heading']}",
                xref="paper",
                x=0
            ),
            showlegend=False,
            yaxis=go.layout.YAxis(
                title=go.layout.yaxis.Title(
                    text=f"{metadata['yaxis']['name']}<br><sup><i>{metadata['yaxis']['uom']}</i></sup>"
                ),
                gridcolor=colours.GRIDCOLOUR
            ),
            paper_bgcolor = colours.PAPERBACKGROUND,
            plot_bgcolor=colours.PLOTBACKGROUND,
        )
        fig.show()
        figpath = os.path.join(config.FIGFOLDER, f"{metadata['heading']}.jpeg")
        fig.write_image(figpath)
        return fig

    def distrboxplot_horizontal(self, data, metadata):
        """ 
        data = {
                'yaxes': [[y,y,y,y,y],[y,y,y,y,y],[y,y,y,y,y],[y,y,y,y,y]],
                'names': ['name','name','name','name'],
                'colours': [colour,colour,colour,colour]
        }
        metadata = {
            'yaxis':{'name':'name', 'uom':'uom'},
            'xaxis':{'name':'name', 'uom':'uom'},
            'heading':'heading',
            'popcount':'popcount',
            'mode':'mode'
        }    
        """
        self.logger.debug(f"- scatterplot")

        fig = go.Figure()

        # Add traces
        for count, vals in enumerate(data['names']):

            fig.add_trace(go.Box(x=data['yaxes'][count],
                                    marker_color=data['colours'][count],
                                    name=vals,
                                    notched=True,
                                    jitter=0.3,
                                    pointpos=-1.8,
                                    boxpoints=False,  # represent all points
                                        )
                        )

        fig.update_layout(
            title=go.layout.Title(
                text=f"{metadata['heading']}<br><sup><i>(n={metadata['popcount']})</i></sup>",
                #text=f"{metadata['heading']}",
                xref="paper",
                x=0
            ),
            showlegend=False,
            xaxis=go.layout.XAxis(
                title=go.layout.xaxis.Title(
                    text=f"{metadata['yaxis']['name']}<br><sup><i>{metadata['yaxis']['uom']}</i></sup>"
                ),
                gridcolor=colours.GRIDCOLOUR
            ),
            paper_bgcolor = colours.PAPERBACKGROUND,
            plot_bgcolor=colours.PLOTBACKGROUND,
        )
        fig.show()
        figpath = os.path.join(config.FIGFOLDER, f"{metadata['heading']}.jpeg")
        fig.write_image(figpath)
        return fig 

class VizSplom:
    logger = logging.getLogger(f"{__name__}.VizSplom")
    """
    https://plotly.com/python-api-reference/generated/plotly.graph_objects.Splom.html
    https://plotly.com/python/splom/
    """

    def splom(self, data, metadata):
        """ 
        data = {'dimensions': [dict(label=label,values=values),
                                dict(label=label,values=values)],
                'names': ['name', 'name'],
                'text': [mode, mode],
                'markers': [dict(color=color,
                                showscale=False,  
                                line_color='white', 
                                line_width=0.5),
                            dict(color=color,
                                showscale=False,  
                                line_color='white', 
                                line_width=0.5)
                        ]
        }
        metadata = {
            'yaxis':{'name':'name', 'uom':'uom'},
            'xaxis':{'name':'name', 'uom':'uom'},
            'heading':'heading',
            'popcount':'popcount',
            'mode':'mode'
        }    
        """
        self.logger.debug(f"- splom")

        fig = go.Figure()

        # Add traces
        for count, vals in enumerate(data['names']):
            fig.add_trace(go.Splom(
                            dimensions=data['dimensions'][count],
                            diagonal_visible=False,
                            #text=data['text'][count],
                            name=data['names'][count],
                            marker=data['markers'][count]
                            )
                        )

        fig.update_layout(
            title=go.layout.Title(
                text=f"{metadata['heading']}<br><sup><i>(n={metadata['popcount']})</i></sup>",
                #text=f"{metadata['heading']}",
                xref="paper",
                x=0
            ),

            showlegend=True,
            plot_bgcolor='#ececec',
            width=1000,
            height=1000,
        )
        fig.show()
        figpath = os.path.join(config.FIGFOLDER, f"{metadata['heading']}.jpeg")
        fig.write_image(figpath)
        return fig
 
    def heatmap(self, df):
        """ 

        """
        self.logger.debug(f"- splom")

        values = []
        columns = list(df.columns)

        for x in columns:
            vals = []
            for y in columns:
                corr = round(df[x].corr(df[y]), 4)
                vals.append(corr)
            values.append(vals)

        fig = go.Figure(data=go.Heatmap(
            z=values,
            x=columns,
            y=columns,
            text=values,
            texttemplate="%{text}",
            hoverongaps=True, 
            colorscale = 'RdBu_r'))

        fig.update_layout(
            # title='Creatinine > 80',
            title=f"Correlation matrix<br><sup><i>(n={len(df)})</i></sup>",
            showlegend=False,
        )
        fig.show()
        figpath = os.path.join(config.FIGFOLDER, f"heatmap.jpeg")
        fig.write_image(figpath)
        return fig


class VizSankey:
    logger = logging.getLogger(f"{__name__}.VizSankey")
    """
    https://plotly.com/python-api-reference/generated/plotly.graph_objects.Splom.html
    https://plotly.com/python/sankey-diagram/
    """

    def sankey(self, labels, srcs, targets, vals):
        """ 
        data = {'dimensions': [dict(label=label,values=values),
                                dict(label=label,values=values)],
                'names': ['name', 'name'],
                'text': [mode, mode],
                'markers': [dict(color=color,
                                showscale=False,  
                                line_color='white', 
                                line_width=0.5),
                            dict(color=color,
                                showscale=False,  
                                line_color='white', 
                                line_width=0.5)
                        ]
        }
        metadata = {
            'yaxis':{'name':'name', 'uom':'uom'},
            'xaxis':{'name':'name', 'uom':'uom'},
            'heading':'heading',
            'popcount':'popcount',
            'mode':'mode'
        }    
        """
        self.logger.debug(f"- sankey")

        fig = go.Figure()

        labels = ['Patients',  
                  'Hb <= 120', 'Hb > 120', 'Not measured',
                  'Anemic at Term', 'Cleared', 'Not measured T']

        # Add traces
        fig.add_trace(go.Sankey(
            arrangement='snap',
            node=dict(
                #label=['A', 'B', 'C', 'D', 'E', 'F'],
                label = labels,
                x=[0.1, 0.3, 0.3, 0.5, 0.7, 0.8, 0.9],
                y=[0.1, 0.1, 0.5, 0.8, 0.1, 0.2, 0.3],
                pad=10  
            ),
            link=dict(
                arrowlen=15,
                #source=srcs,
                #target=targets,
                value=vals,
                source=[0, 0, 0, 1, 1, 1],
                target=[1, 2, 3, 4, 5, 6],
                #value=[1, 2, 1, 1, 1, 1] 
                #source=[0, 0, 1, 2, 5, 4, 3, 5],
                #target=[5, 3, 4, 3, 0, 2, 2, 3],
                #value=[1, 2, 1, 1, 1, 1, 1, 2]  
            )
                        )
                    )

        fig.update_layout(
            title=go.layout.Title(
                #text=f"{metadata['heading']}<br><sup><i>(n={metadata['popcount']})</i></sup>",
                text=f"Anemia",
                xref="paper",
                x=0
            ),

            showlegend=True,
            plot_bgcolor='#ececec',
            width=1000,
            height=1000,
        )
        fig.show()
        figpath = os.path.join(config.FIGFOLDER, f"Anemia.jpeg")
        fig.write_image(figpath)
        return fig
 

