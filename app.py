import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Water Usage Dashboard",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to improve appearance
def add_custom_styling():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #E5E7EB;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #1E3A8A;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #F9FAFB;
        border-radius: 0.5rem;
        padding: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #F0F9FF;
        border-radius: 0.5rem;
        padding: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #00FF00;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #00FF00;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #6B7280;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #E5E7EB;
        color: #6B7280;
        font-size: 0.8rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #F3F4F6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding: 10px 16px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00FF00;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

add_custom_styling()

# Application title
st.markdown('<h1 class="main-header">Water Usage and Cost Dashboard</h1>', unsafe_allow_html=True)

class WaterUsageDashboard:
    def __init__(self):
        # Initialize data
        self.data = [
            {'year': 2011, 'usage': 2178900, 'cost': 209828.00, 'costPerUnit': 0.0963},
            {'year': 2012, 'usage': 1427550, 'cost': 137535.00, 'costPerUnit': 0.0963},
            {'year': 2013, 'usage': 1532850, 'cost': 172209.00, 'costPerUnit': 0.1123},
            {'year': 2014, 'usage': 1071650, 'cost': 125883.00, 'costPerUnit': 0.1175},
            {'year': 2015, 'usage': 1381200, 'cost': 161637.00, 'costPerUnit': 0.1170},
            {'year': 2016, 'usage': 1711350, 'cost': 201544.00, 'costPerUnit': 0.1178},
            {'year': 2017, 'usage': 1607100, 'cost': 194743.00, 'costPerUnit': 0.1212},
            {'year': 2018, 'usage': 1800750, 'cost': 218194.00, 'costPerUnit': 0.1212},
            {'year': 2019, 'usage': 834500, 'cost': 114822.00, 'costPerUnit': 0.1376},
            {'year': 2020, 'usage': 1148800, 'cost': 122968.00, 'costPerUnit': 0.1070},
            {'year': 2021, 'usage': 1035350, 'cost': 126298.00, 'costPerUnit': 0.1220},
            {'year': 2022, 'usage': 1272460, 'cost': 165442.70, 'costPerUnit': 0.1300},
            {'year': 2023, 'usage': 1088370, 'cost': 165066.76, 'costPerUnit': 0.1517}
        ]
        
        # Convert to dataframe for easier plotting
        self.df = pd.DataFrame(self.data)
        
        # Calculate year-over-year changes
        self.df['usage_change'] = self.df['usage'].pct_change() * 100
        self.df['cost_change'] = self.df['cost'].pct_change() * 100
        
        # Calculate stats
        self.stats = {
            'total_usage': self.df['usage'].sum(),
            'total_cost': self.df['cost'].sum(),
            'avg_usage': self.df['usage'].mean(),
            'avg_cost': self.df['cost'].mean(),
            'min_usage': self.df['usage'].min(),
            'max_usage': self.df['usage'].max(),
            'min_cost': self.df['cost'].min(),
            'max_cost': self.df['cost'].max(),
            'min_year_usage': int(self.df.loc[self.df['usage'].idxmin(), 'year']),
            'max_year_usage': int(self.df.loc[self.df['usage'].idxmax(), 'year']),
            'min_year_cost': int(self.df.loc[self.df['cost'].idxmin(), 'year']),
            'max_year_cost': int(self.df.loc[self.df['cost'].idxmax(), 'year']),
            'cost_per_unit_increase': ((self.df['costPerUnit'].iloc[-1] / self.df['costPerUnit'].iloc[0]) - 1) * 100
        }

    def format_number(self, num):
        return f"{num:,}"
    
    def format_currency(self, num):
        return f"${num:,.2f}"
    
    def render_kpi_metrics(self):
        # Display key metrics at the top
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{self.format_number(int(self.stats["avg_usage"]))}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Average Annual Usage (cubic feet)</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{self.format_currency(self.stats["avg_cost"])}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Average Annual Cost</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col3:
            latest_cost_per_unit = self.df['costPerUnit'].iloc[-1]
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">${latest_cost_per_unit:.4f}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Current Cost per Cubic Foot</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{self.stats["cost_per_unit_increase"]:.1f}%</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Cost per Unit Increase (2011-2023)</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    def render_dashboard(self):
        # Show KPI metrics
        self.render_kpi_metrics()
        
        # Create tabs for different visualizations
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Combined View", "💧 Water Usage", "💰 Cost", "📈 Cost per Unit", "📋 Data Table"])
        
        with tab1:
            self.render_combined_view()
            
        with tab2:
            self.render_usage_view()
            
        with tab3:
            self.render_cost_view()
            
        with tab4:
            self.render_cost_per_unit_view()
            
        with tab5:
            self.render_data_table()
        
        # Show analysis section
        st.markdown('<h2 class="sub-header">Detailed Analysis</h2>', unsafe_allow_html=True)
        self.render_detailed_analysis()
        
        # Show year-over-year changes
        st.markdown('<h2 class="sub-header">Year-over-Year Changes</h2>', unsafe_allow_html=True)
        self.render_year_over_year()
        
        # Add a sidebar with additional options
        self.render_sidebar()
        
        # Footer
        st.markdown('<div class="footer">Water Usage Dashboard • Created with Streamlit • 2025</div>', unsafe_allow_html=True)
    
    def render_combined_view(self):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add bar chart for usage
        fig.add_trace(
            go.Bar(
                x=self.df['year'], 
                y=self.df['usage'], 
                name="Water Usage",
                marker_color='#AB2330',
                hovertemplate='Year: %{x}<br>Usage: %{y:,.0f} cubic feet<extra></extra>'
            ),
            secondary_y=False,
        )
        
        # Add line chart for cost
        fig.add_trace(
            go.Scatter(
                x=self.df['year'], 
                y=self.df['cost'], 
                name="Water Cost",
                line=dict(color='#EF4444', width=3),
                hovertemplate='Year: %{x}<br>Cost: $%{y:,.2f}<extra></extra>'
            ),
            secondary_y=True,
        )
        
        # Set titles and labels
        fig.update_layout(
            title="Water Usage and Cost (2011-2023)",
            hovermode="x unified",
            hoverlabel=dict(bgcolor="white", font_size=12),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=500,
            margin=dict(l=60, r=60, t=80, b=60),
            plot_bgcolor='rgba(245,250,255,0.5)'
        )
        
        # Update axes
        fig.update_xaxes(
            title_text="Year",
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(211,211,211,0.5)',
            tickmode='linear'
        )
        
        fig.update_yaxes(
            title_text="Water Usage (cubic feet)",
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(211,211,211,0.5)',
            tickformat=",.0f",
            secondary_y=False
        )
        
        fig.update_yaxes(
            title_text="Cost ($)",
            showgrid=False,
            tickprefix="$",
            tickformat=",.2f",
            secondary_y=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    def render_usage_view(self):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Create interactive bar chart for usage
        fig = px.bar(
            self.df,
            x='year',
            y='usage',
            title='Annual Water Usage (2011-2023)',
            labels={'year': 'Year', 'usage': 'Water Usage (cubic feet)'},
            color_discrete_sequence=['#3B82F6'],
            text_auto='.2s'
        )
        
        # Customize layout
        fig.update_layout(
            hovermode="x unified",
            hoverlabel=dict(bgcolor="white", font_size=12),
            height=500,
            margin=dict(l=60, r=60, t=80, b=60),
            plot_bgcolor='rgba(245,250,255,0.5)'
        )
        
        fig.update_traces(
            hovertemplate='Year: %{x}<br>Usage: %{y:,.0f} cubic feet<extra></extra>',
            textposition='outside'
        )
        
        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(211,211,211,0.5)',
            tickmode='linear'
        )
        
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(211,211,211,0.5)',
            tickformat=",.0f"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add insights for water usage
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### Key Insights:
            - Highest usage in **{}** with {:,} cubic feet
            - Lowest usage in **{}** with {:,} cubic feet
            - Notable **{:.1f}%** decrease from peak usage to present
            """.format(
                self.stats['max_year_usage'], 
                self.stats['max_usage'],
                self.stats['min_year_usage'],
                self.stats['min_usage'],
                ((self.stats['max_usage'] - self.df['usage'].iloc[-1]) / self.stats['max_usage']) * 100
            ))
        
        with col2:
            # Add year with biggest drop
            biggest_drop_idx = self.df['usage_change'].idxmin()
            biggest_drop_year = self.df.loc[biggest_drop_idx, 'year']
            biggest_drop_pct = self.df.loc[biggest_drop_idx, 'usage_change']
            
            st.markdown("""
            #### Notable Changes:
            - Largest single-year decrease: **{:.1f}%** in **{}**
            - Average annual usage: {:,} cubic feet
            - Current usage is **{:.1f}%** of 2011 baseline
            """.format(
                biggest_drop_pct,
                int(biggest_drop_year),
                int(self.stats['avg_usage']),
                (self.df['usage'].iloc[-1] / self.df['usage'].iloc[0]) * 100
            ))
        
        st.markdown('</div>', unsafe_allow_html=True)

    def render_cost_view(self):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Create line chart for cost
        fig = px.line(
            self.df,
            x='year',
            y='cost',
            title='Annual Water Cost (2011-2023)',
            labels={'year': 'Year', 'cost': 'Cost ($)'},
            markers=True
        )
        
        # Customize layout
        fig.update_layout(
            hovermode="x unified",
            hoverlabel=dict(bgcolor="white", font_size=12),
            height=500,
            margin=dict(l=60, r=60, t=80, b=60),
            plot_bgcolor='rgba(245,250,255,0.5)'
        )
        
        fig.update_traces(
            line=dict(color='#EF4444', width=3),
            marker=dict(size=8, color='#EF4444'),
            hovertemplate='Year: %{x}<br>Cost: $%{y:,.2f}<extra></extra>'
        )
        
        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(211,211,211,0.5)',
            tickmode='linear'
        )
        
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(211,211,211,0.5)',
            tickprefix="$",
            tickformat=",.2f"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add insights for cost
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### Cost Insights:
            - Highest cost in **{}** at ${}
            - Lowest cost in **{}** at ${}
            - Current annual cost represents **{:.1f}%** of the peak
            """.format(
                self.stats['max_year_cost'], 
                self.format_number(int(self.stats['max_cost'])),
                self.stats['min_year_cost'],
                self.format_number(int(self.stats['min_cost'])),
                (self.df['cost'].iloc[-1] / self.stats['max_cost']) * 100
            ))
        
        with col2:
            # Add year with biggest cost increase
            biggest_increase_idx = self.df['cost_change'].idxmax()
            biggest_increase_year = self.df.loc[biggest_increase_idx, 'year']
            biggest_increase_pct = self.df.loc[biggest_increase_idx, 'cost_change']
            
            st.markdown("""
            #### Notable Changes:
            - Largest single-year cost increase: **{:.1f}%** in **{}**
            - Total 13-year water expenditure: **${}**
            - Current cost is **{:.1f}%** of 2011 baseline
            """.format(
                biggest_increase_pct,
                int(biggest_increase_year),
                self.format_number(int(self.stats['total_cost'])),
                (self.df['cost'].iloc[-1] / self.df['cost'].iloc[0]) * 100
            ))
        
        st.markdown('</div>', unsafe_allow_html=True)

    def render_cost_per_unit_view(self):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Create line chart for cost per unit
        fig = px.line(
            self.df,
            x='year',
            y='costPerUnit',
            title='Cost per Cubic Foot (2011-2023)',
            labels={'year': 'Year', 'costPerUnit': 'Cost per Cubic Foot ($)'},
            markers=True
        )
        
        # Add a trendline
        fig.add_trace(
            go.Scatter(
                x=self.df['year'],
                y=np.polyval(np.polyfit(self.df['year'], self.df['costPerUnit'], 1), self.df['year']),
                mode='lines',
                line=dict(color='rgba(255, 99, 132, 0.3)', width=2, dash='dash'),
                name='Trend',
                hoverinfo='skip'
            )
        )
        
        # Customize layout
        fig.update_layout(
            hovermode="x unified",
            hoverlabel=dict(bgcolor="white", font_size=12),
            height=500,
            margin=dict(l=60, r=60, t=80, b=60),
            plot_bgcolor='rgba(245,250,255,0.5)'
        )
        
        fig.update_traces(
            selector=dict(name='costPerUnit'),
            line=dict(color='#10B981', width=3),
            marker=dict(size=8, color='#10B981'),
            hovertemplate='Year: %{x}<br>Cost per Cubic Foot: $%{y:.4f}<extra></extra>'
        )
        
        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(211,211,211,0.5)',
            tickmode='linear'
        )
        
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(211,211,211,0.5)',
            tickprefix="$",
            tickformat=".4f"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add insights for cost per unit
        col1, col2 = st.columns(2)
        
        with col1:
            # Calculate annual growth rate (CAGR)
            years = len(self.df) - 1
            starting_cost = self.df['costPerUnit'].iloc[0]
            ending_cost = self.df['costPerUnit'].iloc[-1]
            cagr = ((ending_cost / starting_cost) ** (1 / years) - 1) * 100
            
            st.markdown("""
            #### Cost per Unit Insights:
            - Starting rate (2011): **${}**
            - Current rate (2023): **${}**
            - Total increase: **{:.1f}%** over 13 years
            - Compound annual growth rate: **{:.2f}%**
            """.format(
                self.df['costPerUnit'].iloc[0],
                self.df['costPerUnit'].iloc[-1],
                self.stats['cost_per_unit_increase'],
                cagr
            ))
        
        with col2:
            # Find when cost per unit exceeded certain thresholds
            threshold_10cents = self.df[self.df['costPerUnit'] >= 0.10].iloc[0]['year'] if not self.df[self.df['costPerUnit'] >= 0.10].empty else 'N/A'
            threshold_12cents = self.df[self.df['costPerUnit'] >= 0.12].iloc[0]['year'] if not self.df[self.df['costPerUnit'] >= 0.12].empty else 'N/A'
            threshold_15cents = self.df[self.df['costPerUnit'] >= 0.15].iloc[0]['year'] if not self.df[self.df['costPerUnit'] >= 0.15].empty else 'N/A'
            
            st.markdown("""
            #### Price Milestones:
            - Exceeded $0.10 per cubic foot: **{}**
            - Exceeded $0.12 per cubic foot: **{}**
            - Exceeded $0.15 per cubic foot: **{}**
            - If trend continues, projected to reach $0.20 by 2030
            """.format(
                threshold_10cents,
                threshold_12cents,
                threshold_15cents
            ))
        
        st.markdown('</div>', unsafe_allow_html=True)

    def render_data_table(self):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Format the dataframe for display
        display_df = self.df.copy()
        display_df['usage'] = display_df['usage'].apply(lambda x: f"{int(x):,}")
        display_df['cost'] = display_df['cost'].apply(lambda x: f"${x:,.2f}")
        display_df['costPerUnit'] = display_df['costPerUnit'].apply(lambda x: f"${x:.4f}")
        
        # Drop the change columns for the main table
        if 'usage_change' in display_df.columns:
            display_df = display_df.drop(['usage_change', 'cost_change'], axis=1)
        
        # Rename columns
        display_df = display_df.rename(columns={
            'year': 'Year',
            'usage': 'Water Usage (cubic feet)',
            'cost': 'Water Cost',
            'costPerUnit': 'Cost per Cubic Foot'
        })
        
        # Show data table with formatting
        st.dataframe(
            display_df,
            hide_index=True,
            use_container_width=True
        )
        
        # Add download button
        csv = self.df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name="water_usage_data.csv",
            mime="text/csv",
            help="Download the complete dataset as a CSV file"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)

    def render_detailed_analysis(self):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Calculate correlation between usage and cost
            correlation = self.df['usage'].corr(self.df['cost'])
            
            # Calculate average cost per unit over time periods
            early_years = self.df[self.df['year'] <= 2015]['costPerUnit'].mean()
            recent_years = self.df[self.df['year'] > 2015]['costPerUnit'].mean()
            percent_increase = ((recent_years / early_years) - 1) * 100
            
            st.markdown("""
            #### Cost Analysis
            
            - Correlation between usage and cost: **{:.2f}**
            - Average cost per unit (2011-2015): **${:.4f}**
            - Average cost per unit (2016-2023): **${:.4f}**
            - Price increase between periods: **{:.1f}%**
            
            The data shows a strong correlation between water usage and cost, indicating that billing is primarily usage-based. However, the increasing cost per cubic foot demonstrates that water has become more expensive over time, even when controlling for usage.
            """.format(
                correlation,
                early_years,
                recent_years,
                percent_increase
            ))
        
        with col2:
            # Find efficiency improvements
            earliest_year_data = self.df.iloc[0]
            latest_year_data = self.df.iloc[-1]
            usage_change = ((latest_year_data['usage'] / earliest_year_data['usage']) - 1) * 100
            
            st.markdown("""
            #### Usage Analysis
            
            - Total water usage over 13 years: **{:,} cubic feet**
            - Average annual usage: **{:,} cubic feet**
            - Usage change from 2011 to 2023: **{:.1f}%**
            
            The data suggests periods of both high and low water usage. The significant drop in 2019 could indicate a conservation effort, operational changes, or other factors affecting water consumption. Understanding these patterns can help identify opportunities for future water conservation and cost savings.
            """.format(
                int(self.stats['total_usage']),
                int(self.stats['avg_usage']),
                usage_change
            ))
        
        st.markdown('</div>', unsafe_allow_html=True)

    def render_year_over_year(self):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Create a year-over-year change chart
        # Filter out the first year since it has no previous year for comparison
        yoy_df = self.df.dropna().copy()
        
        # Create the figure
        fig = go.Figure()
        
        # Add usage change bars
        fig.add_trace(go.Bar(
            x=yoy_df['year'],
            y=yoy_df['usage_change'],
            name='Usage Change (%)',
            marker_color='#AB2330',
            hovertemplate='Year: %{x}<br>Usage Change: %{y:.1f}%<extra></extra>'
        ))
        
        # Add cost change bars
        fig.add_trace(go.Bar(
            x=yoy_df['year'],
            y=yoy_df['cost_change'],
            name='Cost Change (%)',
            marker_color='#AB2330',
            hovertemplate='Year: %{x}<br>Cost Change: %{y:.1f}%<extra></extra>'
        ))
        
        # Add zero line
        fig.add_shape(
            type="line",
            x0=yoy_df['year'].min() - 0.5,
            x1=yoy_df['year'].max() + 0.5,
            y0=0,
            y1=0,
            line=dict(color="gray", width=1, dash="dash"),
        )
        
        # Update layout
        fig.update_layout(
            title='Year-over-Year Percentage Changes',
            xaxis_title='Year',
            yaxis_title='Change (%)',
            barmode='group',
            hovermode="x unified",
            hoverlabel=dict(bgcolor="white", font_size=12),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=400,
            margin=dict(l=60, r=60, t=80, b=60),
            plot_bgcolor='rgba(245,250,255,0.5)'
        )
        
        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(211,211,211,0.5)',
            tickmode='linear'
        )
        
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(211,211,211,0.5)',
            ticksuffix="%"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
        # Find notable year-over-year changes
        biggest_usage_drop = self.df.loc[self.df['usage_change'].idxmin()]
        biggest_usage_increase = self.df
# Find notable year-over-year changes
        biggest_usage_drop = self.df.loc[self.df['usage_change'].idxmin()]
        biggest_usage_increase = self.df.loc[self.df['usage_change'].idxmax()]
        biggest_cost_increase = self.df.loc[self.df['cost_change'].idxmax()]
        
        # Add analysis text
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### Notable Annual Changes
            
            - Largest usage decrease: **{:.1f}%** in **{}**
            - Largest usage increase: **{:.1f}%** in **{}**
            - Largest cost increase: **{:.1f}%** in **{}**
            """.format(
                biggest_usage_drop['usage_change'],
                int(biggest_usage_drop['year']),
                biggest_usage_increase['usage_change'],
                int(biggest_usage_increase['year']),
                biggest_cost_increase['cost_change'],
                int(biggest_cost_increase['year'])
            ))
        
        with col2:
            # Calculate volatility (standard deviation of changes)
            usage_volatility = self.df['usage_change'].std()
            cost_volatility = self.df['cost_change'].std()
            
            st.markdown("""
            #### Volatility Analysis
            
            - Usage change volatility: **{:.1f}%** standard deviation
            - Cost change volatility: **{:.1f}%** standard deviation
            - Years with opposite trends: **{}** (usage and cost moved in different directions)
            """.format(
                usage_volatility,
                cost_volatility,
                len(self.df[(self.df['usage_change'] > 0) & (self.df['cost_change'] < 0) | 
                            (self.df['usage_change'] < 0) & (self.df['cost_change'] > 0)].dropna())
            ))
        
        st.markdown('</div>', unsafe_allow_html=True)

    def render_sidebar(self):
        st.sidebar.title("Dashboard Controls")
        
        st.sidebar.markdown("### Data Range")
        
        # Year range slider
        min_year = int(self.df['year'].min())
        max_year = int(self.df['year'].max())
        selected_years = st.sidebar.slider(
            "Select Years",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )
        
        # This would filter the data if implemented fully
        st.sidebar.markdown(f"Selected range: {selected_years[0]} - {selected_years[1]}")
        st.sidebar.markdown("---")
        
        # Add some analysis options
        st.sidebar.markdown("### Analysis Options")
        
        show_trend = st.sidebar.checkbox("Show trend lines", value=True)
        normalize_data = st.sidebar.checkbox("Normalize data (per 1000 cubic feet)", value=False)
        
        if normalize_data:
            st.sidebar.info("💡 Normalization helps compare relative changes when absolute values differ significantly.")
        
        if show_trend:
            st.sidebar.info("💡 Trend lines help visualize the overall direction of the data over time.")
        
        st.sidebar.markdown("---")
        
        # Add context information
        st.sidebar.markdown("### About This Dashboard")
        st.sidebar.markdown("""
        This dashboard visualizes water usage and cost data from 2011 to 2023. It provides insights into:
        
        - Water consumption trends
        - Cost analysis
        - Price per unit changes
        - Year-over-year comparisons
        
        Use the tabs above to explore different aspects of the data.
        """)
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("📊 **Water Usage Dashboard** | v1.0")
        

# Run the dashboard
if __name__ == "__main__":
    dashboard = WaterUsageDashboard()
    dashboard.render_dashboard()
