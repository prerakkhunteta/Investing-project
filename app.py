import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title='Startup Analysis')

df = pd.read_csv('startup_clean.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')

df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_startup_details(company):
    st.title(company)
    
    # Find company category
    filtered_df = df.loc[df['startup'] == company, 'vertical']
    
    if not filtered_df.empty:
        category = filtered_df.iloc[0]
        st.metric(label="Category", value=category)

    filtered_subcategory = df.loc[df['startup']==company,'subvertical'] 
    if not filtered_subcategory.empty:
        subcategory = filtered_subcategory.iloc[0]
        st.metric(label='Subcategory',value=subcategory)

    filtered_city = df.loc[df['startup']==company,'city'] 
    if not filtered_city.empty:
        city_startup = filtered_city.iloc[0]
        st.metric(label='City',value=city_startup) 

    filtered_round =  df.loc[df['startup'] == 'Mamaearth', ['round', 'investors', 'date']].reset_index(drop=True)
    if not filtered_round.empty:
        st.dataframe(filtered_round)

       

    

















def load_overall_analysis():
    st.title('Overall Analysis')

    # Total invested amount
    total = round(df['amount'].sum())
    #max amount

    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]

    #Avg ticket size
    avg_funding = df.groupby('startup')['amount'].sum().mean()

    #total funded startups
    num_startups = df['startup'].nunique

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric('Total',str(total) + 'Cr')

    with col2:
        st.metric('Max',str(max_funding) + 'Cr')

    with col3:
        st.metric('Avg',str(round(avg_funding))+'Cr')

    with col4:
        st.metric('Funded Startup',str(num_startups) + 'Cr')  

    st.header('MoM graph')
    selected_option = st.selectbox('Select Type',['total','Count'])

    if selected_option=='total':
        temp_df = df.groupby(['year','month'])['amount'].sum().reset_index() 

    else:
        temp_df = df.groupby(['year','month'])['amount'].count().reset_index() 
    



    

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str') 

    fig6, ax6 = plt.subplots()
    ax6.plot(temp_df['x_axis'],temp_df['amount'])
    st.pyplot(fig6)    

    




    


def load_investor_details(investor):
    st.title(investor)
    
    # Load the recent 5 investments
    last5_df = df[df['investors'].str.contains(investor, na=False)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Biggest Investments
        big_series = df[df['investors'].str.contains(investor, na=False)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investment')
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)
    
    with col2:
        vertical_series = df[df['investors'].str.contains(investor, na=False)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct="%0.01f")
        st.pyplot(fig1)

    col3, col4 = st.columns(2)
    
    with col3:
        round_series = df[df['investors'].str.contains(investor, na=False)].groupby('round')['amount'].sum()
        st.subheader('Round in investment')
        fig2, ax2 = plt.subplots()
        ax2.pie(round_series, labels=round_series.index, autopct="%0.01f")
        st.pyplot(fig2)
    
    with col4:
        city_series = df[df['investors'].str.contains(investor, na=False)].groupby('city')['amount'].sum()
        st.subheader('Investment City')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels=city_series.index, autopct="%0.01f")
        st.pyplot(fig3)

    df.loc[:, 'year'] = df['date'].dt.year

    year_series = df[df['investors'].str.contains(investor, na=False)].groupby('year')['amount'].sum()
    
    st.subheader('YoY investment')
    fig4, ax4 = plt.subplots()
    ax4.plot(year_series.index, year_series.values, marker='o')
    ax4.set_xlabel('Year')
    ax4.set_ylabel('Investment Amount')
    st.pyplot(fig4)

st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()
elif option == 'Startup':
    selected_startup = st.sidebar.selectbox('Select Startup', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    if btn1:
        load_startup_details(selected_startup)

else:
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)
