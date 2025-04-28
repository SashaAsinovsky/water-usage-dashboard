# Water Usage Dashboard

A polished, interactive dashboard for visualizing water usage and cost data from 2011 to 2023.

![Dashboard Preview](https://github.com/yourusername/water-usage-dashboard/assets/preview.png)

## Features

- 📊 **Interactive Visualizations**: Multiple views including combined charts, usage analysis, cost analysis, and cost per unit tracking
- 📈 **Trend Analysis**: Year-over-year changes and long-term trend identification
- 💧 **Usage Insights**: Detailed statistics and key observations about water consumption patterns
- 💰 **Cost Analysis**: Comprehensive examination of water costs and price changes over time
- 📱 **Responsive Design**: Optimized for both desktop and mobile viewing
- 📥 **Data Export**: Download the analyzed data in CSV format

## Live Demo

You can view the live dashboard at: [https://yourusername-water-usage-dashboard.streamlit.app](https://yourusername-water-usage-dashboard.streamlit.app)

## Running Locally

To run this dashboard locally:

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/water-usage-dashboard.git
   cd water-usage-dashboard
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

4. Open your browser and navigate to http://localhost:8501

## Deploying to Streamlit Cloud

This repository is ready for deployment on Streamlit Cloud:

1. Fork this repository to your GitHub account
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Sign in with your GitHub account
4. Create a new app, selecting this repository
5. Choose `app.py` as the main file
6. Deploy!

## Data Structure

The dashboard visualizes the following data:
- Annual water usage (cubic feet)
- Annual water costs ($)
- Cost per cubic foot
- Year-over-year changes

## Customization

To use with your own data, modify the `data` list in the `WaterUsageDashboard` class in `app.py`.

## Technologies Used

- [Streamlit](https://streamlit.io/): Web application framework
- [Plotly](https://plotly.com/): Interactive charts and visualizations
- [Pandas](https://pandas.pydata.org/): Data manipulation and analysis
- [NumPy](https://numpy.org/): Numerical computing

## License

MIT

## Contact

For questions or feedback, please open an issue on this repository.
