import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

    # App Config - MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="Climate Pulse", layout="wide")

# Load sample data (replace with real climate data)
@st.cache_data
def load_data():
    co2 = pd.read_csv("data/co2_emissions.csv")
    temp = pd.read_csv("data/temperature.csv")
    sea = pd.read_csv("data/sea_level.csv")
    return co2, temp, sea

co2_df, temp_df, sea_df = load_data()

st.title("🌍 Climate Pulse")
st.markdown("##### A Data-Driven Visual Insight Tool on Climate Change Impact")

# Horizontal navigation with tabs instead of sidebar
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌡️ Global Temperature Rise", 
    "🌍 CO₂ Emissions by Country",
    "🌊 Sea Level Trends",
    "🔮 What-If Scenarios",
    "🧭 Personalized Action"
])

# Global Temperature Rise Page
with tab1:
    st.subheader("📈 Global Temperature Rise Over Time")
    fig = px.line(temp_df, x="Year", y="Temp_Anomaly", 
                  title="Temperature Anomaly (°C) Over Time",
                  labels={"Temp_Anomaly": "Temperature Anomaly (°C)"})
    fig.update_layout(
        annotations=[
            dict(
                x=2010,
                y=0.7,
                xref="x",
                yref="y",
                text="Critical threshold approaching",
                showarrow=True,
                arrowhead=1
            )
        ]
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    ### Key Insights:
    - **Accelerating Change**: Notice the steep increase after 1950, showing how the warming rate has accelerated
    - **1.0°C Milestone**: By 2020, we crossed the critical 1.0°C warming threshold
    - **Historical Context**: The 1880-1950 period shows relatively stable temperatures compared to modern rapid warming
    - **Impact Perspective**: Even small temperature changes (0.5-1.0°C) can significantly disrupt ecosystems and weather patterns
    
    > 💡 **Did you know?** The Paris Agreement aims to limit global warming to well below 2°C, preferably 1.5°C, compared to pre-industrial levels.
    """)
    
    # Adding a temperature milestone visualization
    milestone_data = {
        "Milestone": ["Pre-industrial levels", "First recorded data", "Mid-century baseline", "Current warming", "Paris Agreement target", "High-risk threshold"],
        "Temperature (°C)": [0, -0.2, 0.0, 1.0, 1.5, 2.0],
        "Year": ["1750s", "1880", "1950", "2020", "Target", "Must avoid"],
        "Status": ["Baseline", "Historical", "Reference", "Current", "Goal", "Danger"]
    }
    milestone_df = pd.DataFrame(milestone_data)
    
    st.subheader("Temperature Milestones")
    fig_milestones = px.bar(milestone_df, x="Milestone", y="Temperature (°C)", color="Status", 
                           color_discrete_map={"Baseline":"lightgrey", "Historical":"lightblue", 
                                             "Reference":"blue", "Current":"orange", 
                                             "Goal":"green", "Danger":"red"})
    st.plotly_chart(fig_milestones, use_container_width=True)

# CO2 Emissions Page
with tab2:
    st.subheader("💨 CO₂ Emissions Over Time")
    
    # Add comparison option
    comparison_mode = st.checkbox("Compare countries")
    
    if comparison_mode:
        selected_countries = st.multiselect(
            "Select countries to compare", 
            options=sorted(co2_df["Country"].unique()),
            default=["USA", "China", "India"]
        )
        
        if selected_countries:
            filtered_data = co2_df[co2_df["Country"].isin(selected_countries)]
            fig = px.line(filtered_data, x="Year", y="Emissions", color="Country",
                         title="Comparative CO₂ Emissions Trends",
                         labels={"Emissions": "Emissions (MtCO₂)"})
            st.plotly_chart(fig, use_container_width=True)
            
            # Add per country analysis
            st.subheader("Country-specific Emission Analysis")
            col1, col2 = st.columns(2)
            
            with col1:
                # Calculate emission growth rates
                for country in selected_countries:
                    country_data = co2_df[co2_df["Country"] == country]
                    if len(country_data) >= 2:
                        first_year = country_data["Year"].min()
                        last_year = country_data["Year"].max()
                        first_emissions = country_data[country_data["Year"] == first_year]["Emissions"].values[0]
                        last_emissions = country_data[country_data["Year"] == last_year]["Emissions"].values[0]
                        growth_pct = ((last_emissions - first_emissions) / first_emissions) * 100
                        
                        if growth_pct > 50:
                            emoji = "🔴"
                        elif growth_pct > 20:
                            emoji = "🟠"
                        else:
                            emoji = "🟢"
                            
                        st.markdown(f"**{country}**: {emoji} {growth_pct:.1f}% growth from {first_year} to {last_year}")
            
            with col2:
                # Show total emissions pie chart
                total_by_country = filtered_data.groupby("Country")["Emissions"].sum().reset_index()
                fig_pie = px.pie(total_by_country, values="Emissions", names="Country", 
                                title="Total Emissions Share")
                st.plotly_chart(fig_pie, use_container_width=True)
    else:
        selected_country = st.selectbox("Select a Country", sorted(co2_df["Country"].unique()))
        country_data = co2_df[co2_df["Country"] == selected_country]
        
        fig = px.line(country_data, x="Year", y="Emissions", 
                    title=f"{selected_country} - CO₂ Emissions",
                    labels={"Emissions": "Emissions (MtCO₂)"})
                    
        # Add trend line
        if len(country_data) > 1:
            x = country_data["Year"]
            y = country_data["Emissions"]
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            fig.add_scatter(x=x, y=p(x), mode="lines", line=dict(dash="dash", color="red"), name="Trend")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Country-specific insights
        emissions_insights = {
            "USA": "As one of the largest historical emitters, the USA has seen a slower growth rate recently due to a shift towards renewable energy and natural gas. However, per capita emissions remain among the highest globally.",
            "China": "China's rapid industrialization has led to a steep increase in emissions, making it the world's largest emitter. The nation is also the leading investor in renewable energy technologies.",
            "India": "India's emissions continue to grow with its developing economy and increasing energy demands. The country faces the challenge of balancing development needs with climate commitments."
        }
        
        st.markdown("### Country Analysis")
        st.markdown(emissions_insights.get(selected_country, "This country has its own unique emissions profile based on its energy mix, industrial activity, and climate policies."))
        
        # Calculate growth rate
        if len(country_data) >= 2:
            first_year = country_data["Year"].min()
            last_year = country_data["Year"].max()
            first_emissions = country_data[country_data["Year"] == first_year]["Emissions"].values[0]
            last_emissions = country_data[country_data["Year"] == last_year]["Emissions"].values[0]
            avg_annual_change = (last_emissions - first_emissions) / (last_year - first_year)
            
            st.markdown(f"**Average annual change**: {avg_annual_change:.2f} MtCO₂ per year")
            
            if avg_annual_change > 0:
                st.warning(f"At this rate, emissions will increase by approximately {avg_annual_change * 10:.0f} MtCO₂ over the next decade.")
            else:
                st.success(f"Emissions are decreasing at a rate of {-avg_annual_change:.2f} MtCO₂ per year.")

# Sea Level Page
with tab3:
    st.subheader("🌊 Global Sea Level Rise")
    fig = px.line(sea_df, x="Year", y="Sea_Level_Change", 
                  title="Global Sea Level Rise (mm)",
                  labels={"Sea_Level_Change": "Sea Level Rise (mm)"})
                  
    # Add trend annotation
    trend_slope = (sea_df["Sea_Level_Change"].iloc[-1] - sea_df["Sea_Level_Change"].iloc[0]) / (sea_df["Year"].iloc[-1] - sea_df["Year"].iloc[0])
    fig.add_annotation(x=1950, y=80,
        text=f"Avg. rise: {trend_slope:.1f} mm/year",
        showarrow=False,
        bgcolor="rgba(255, 255, 255, 0.8)")
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    ### Sea Level Rise Insights:
    
    - **Accelerating Trend**: The data shows sea level rise is accelerating - notice how the curve steepens after 1950
    - **Human Impact**: The rapid rise correlates with increased industrial activity and global warming
    - **Coastal Risk**: A 160mm rise may seem small, but can significantly increase flooding frequency in coastal areas
    - **Future Projection**: Scientists predict sea levels could rise by 0.3-2.5 meters by 2100 if current trends continue
    
    #### Regional Impact Analysis
    """)
    
    # Regional impact tab system
    region_tab1, region_tab2, region_tab3 = st.tabs(["Low-lying Islands", "Coastal Cities", "Delta Regions"])
    
    with region_tab1:
        st.markdown("""
        **Small Island Developing States (SIDS)**
        
        Nations like Maldives, Tuvalu, and Kiribati face existential threats from sea level rise, with some projections suggesting partial or complete submersion within decades. Many islands are already experiencing increased flooding, saltwater intrusion, and coastal erosion.
        """)
        
    with region_tab2:
        st.markdown("""
        **Major Coastal Cities at Risk**
        
        - **Miami, USA**: Already experiences regular "sunny day flooding" during high tides
        - **Jakarta, Indonesia**: Sinking while sea levels rise, prompting plans to relocate the capital
        - **Venice, Italy**: Historic flooding becoming more frequent and severe
        - **Mumbai, India**: Densely populated low-lying areas increasingly vulnerable
        """)
        
    with region_tab3:
        st.markdown("""
        **Critical Delta Regions**
        
        The Ganges-Brahmaputra (Bangladesh), Mekong (Vietnam), and Nile (Egypt) deltas are home to millions but face severe impacts from rising seas, including:
        - Saltwater intrusion affecting agriculture
        - Loss of vital farmland
        - Displacement of communities
        - Increased vulnerability to storm surges
        """)

# What-If Scenarios Page
with tab4:
    st.subheader("🔮 Climate Projection Scenarios")
    
    scenario = st.radio(
        "Select emissions scenario",
        ["Business as usual", "Moderate reduction (30% cut)", "Aggressive reduction (60% cut)"]
    )
    
    scenario_year = st.slider("Project to year", 2025, 2100, 2050)
    
    # Create simplified projection model
    base_co2 = co2_df.groupby("Year")["Emissions"].sum().reset_index()
    latest_year = base_co2["Year"].max()
    latest_emissions = base_co2[base_co2["Year"] == latest_year]["Emissions"].values[0]
    
    years_projected = list(range(latest_year + 5, scenario_year + 5, 5))
    
    if scenario == "Business as usual":
        growth_rate = 0.02  # 2% annual growth
        projected_emissions = [latest_emissions * (1 + growth_rate)**(i/5) for i, _ in enumerate(years_projected)]
        temp_increase = 0.3 + (0.015 * (scenario_year - latest_year))  # Simplified model
        sea_increase = 40 + (3 * (scenario_year - latest_year))  # Simplified model
        scenario_description = "Continuing current emission trends will significantly accelerate climate change."
        impact_level = "Severe"
        color = "red"
    elif scenario == "Moderate reduction (30% cut)":
        reduction_factor = 0.3
        decay_rate = 0.03  # 3% annual reduction after initial cut
        baseline = latest_emissions * (1 - reduction_factor)
        projected_emissions = [baseline * (1 - decay_rate)**(i/5) for i, _ in enumerate(years_projected)]
        temp_increase = 0.3 + (0.008 * (scenario_year - latest_year))
        sea_increase = 40 + (2 * (scenario_year - latest_year))
        scenario_description = "A 30% emissions cut would slow climate change but may not prevent significant impacts."
        impact_level = "Moderate"
        color = "orange"
    else:  # Aggressive reduction
        reduction_factor = 0.6
        decay_rate = 0.05  # 5% annual reduction after initial cut
        baseline = latest_emissions * (1 - reduction_factor)
        projected_emissions = [baseline * (1 - decay_rate)**(i/5) for i, _ in enumerate(years_projected)]
        temp_increase = 0.3 + (0.004 * (scenario_year - latest_year))
        sea_increase = 40 + (1 * (scenario_year - latest_year))
        scenario_description = "Aggressive 60% cuts could help limit warming to safer levels."
        impact_level = "Manageable"
        color = "green"
    
    # Create projection dataframe
    projection_df = pd.DataFrame({
        "Year": years_projected,
        "Emissions": projected_emissions,
        "Scenario": [scenario] * len(years_projected)
    })
    
    # Combine with historical data
    historical_df = pd.DataFrame({
        "Year": base_co2["Year"],
        "Emissions": base_co2["Emissions"],
        "Scenario": ["Historical"] * len(base_co2)
    })
    
    combined_df = pd.concat([historical_df, projection_df])
    
    # Plot projections
    fig = px.line(combined_df, x="Year", y="Emissions", color="Scenario",
                 title=f"Emissions Projection to {scenario_year}",
                 color_discrete_map={"Historical": "blue", scenario: color})
    st.plotly_chart(fig, use_container_width=True)
    
    # Show impact metrics
    st.markdown(f"### Projected Climate Impacts by {scenario_year}")
    st.info(scenario_description)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Temperature Increase",
            f"+{temp_increase:.2f}°C",
            f"Impact: {impact_level}"
        )
    
    with col2:
        st.metric(
            "Sea Level Rise",
            f"+{sea_increase:.0f}mm",
            f"From {latest_year}"
        )
    
    with col3:
        # Calculate arbitrary vulnerability index
        if impact_level == "Severe":
            vulnerability = 85
        elif impact_level == "Moderate":
            vulnerability = 60
        else:
            vulnerability = 30
            
        st.metric(
            "Coastal Vulnerability Index",
            f"{vulnerability}/100",
            None
        )
    
    # Regional impact section
    st.subheader("Regional Impact Projection")
    
    impact_data = {
        "Region": ["North America", "Europe", "Asia", "Africa", "Small Island Nations"],
        "Severe": [70, 65, 85, 90, 95],
        "Moderate": [50, 45, 65, 75, 85],
        "Manageable": [20, 15, 40, 60, 70]
    }
    
    impact_df = pd.DataFrame(impact_data)
    
    # Select the appropriate column based on impact level
    impact_values = impact_df[impact_level]
    
    fig_impact = px.bar(
        impact_df, 
        x="Region", 
        y=impact_level,
        labels={impact_level: "Vulnerability Score"},
        color="Region",
        title=f"Regional Vulnerability with {scenario}"
    )
    
    st.plotly_chart(fig_impact, use_container_width=True)

# Personalized Action Page
with tab5:
    st.subheader("🧭 Climate Action Tips Based on Your Region")
    country = st.selectbox("Where Are You From?", sorted(co2_df["Country"].unique()))
    
    # Country-specific action recommendations
    country_actions = {
        "USA": {
            "description": "As one of the highest per-capita emitters, individual actions in the USA can have significant impact.",
            "highest_impact": "Transportation - Reducing car usage and flying less",
            "actions": [
                "Switch to renewable energy through your utility provider",
                "Consider electric or hybrid vehicles for your next car purchase",
                "Reduce beef consumption - the US has one of the highest beef consumption rates globally",
                "Support climate policy advocacy at local and federal levels",
                "Install home solar panels with available tax incentives"
            ]
        },
        "China": {
            "description": "China faces unique urban pollution challenges while leading in renewable energy development.",
            "highest_impact": "Supporting clean energy transition and reducing coal dependence",
            "actions": [
                "Use public transportation in urban centers to reduce notorious air pollution",
                "Support companies making verifiable sustainability commitments",
                "Consider air purification at home to reduce health impacts of pollution",
                "Advocate for continued investment in the country's ambitious renewable energy targets",
                "Participate in community tree-planting initiatives in urban areas"
            ]
        },
        "India": {
            "description": "India balances development needs with climate goals while facing severe climate impacts.",
            "highest_impact": "Water conservation and sustainable agriculture",
            "actions": [
                "Practice water conservation amid increasing water stress",
                "Support farmers practicing sustainable agriculture techniques",
                "Consider solar installations for reliable energy access",
                "Reduce plastic waste which often ends up in waterways",
                "Use natural cooling techniques to reduce air conditioning needs"
            ]
        }
    }
    
    # Default actions for countries not specifically listed
    default_actions = {
        "description": "Every region faces unique climate challenges that require tailored solutions.",
        "highest_impact": "Reducing carbon footprint through daily choices",
        "actions": [
            "Reduce single-use plastic and support local eco-friendly businesses",
            "Use public transport or carpool at least 3x a week",
            "Support climate NGOs and local initiatives",
            "Offset your carbon footprint using apps like [Wren](https://www.wren.co)",
            "Advocate for stronger climate policies in your local government"
        ]
    }
    
    # Get the appropriate actions
    country_info = country_actions.get(country, default_actions)
    
    # Display personalized information
    st.markdown(f"### 💡 Climate Impact Profile: {country}")
    st.markdown(country_info["description"])
    
    st.markdown(f"**Highest impact focus area:** {country_info['highest_impact']}")
    
    st.markdown("### Recommended Actions")
    for i, action in enumerate(country_info["actions"], 1):
        st.markdown(f"{i}. {action}")
    
    # Calculate your impact section
    st.subheader("Calculate Your Impact")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Estimate Your Carbon Footprint")
        flights = st.number_input("Flights per year", 0, 50, 2)
        meat_consumption = st.slider("Meat consumption", 0, 7, 3, help="Days per week")
        car_usage = st.slider("Car usage (km/week)", 0, 500, 100)
        renewable_energy = st.checkbox("Do you use renewable energy at home?")
    
    with col2:
        # Very simplified calculation
        flight_footprint = flights * 0.7  # tonnes CO2
        meat_footprint = meat_consumption * 0.3
        car_footprint = car_usage * 0.0002 * 52  # annual
        home_energy = 2.0 * (0.4 if renewable_energy else 1.0)
        
        total_footprint = flight_footprint + meat_footprint + car_footprint + home_energy
        
        st.markdown("### Your Estimated Annual Footprint")
        st.markdown(f"## {total_footprint:.1f} tonnes CO2e")
        
        # Comparison to average
        country_averages = {"USA": 15.5, "China": 7.4, "India": 1.9}
        country_avg = country_averages.get(country, 4.8)  # Global average as fallback
        
        comparison = (total_footprint / country_avg - 1) * 100
        
        if comparison < 0:
            st.success(f"Your footprint is {abs(comparison):.1f}% lower than the average in {country}!")
        else:
            st.warning(f"Your footprint is {comparison:.1f}% higher than the average in {country}")
    
    st.success("✅ You're part of the solution! Share this app and your results to raise awareness.")