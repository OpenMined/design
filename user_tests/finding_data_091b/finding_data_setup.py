# Breaking down setup into different python functions
import syft as sy
import pandas as pd

# ADMIN CREATE AND DATASITE PROFILE UPDATE -------------------------------------------------

def setup_datasite(port):
    admin_client = sy.login(email="info@openmined.org", password="changethis", port=port)

    # Update Admin
    admin = admin_client.users[0]

    admin_client.users.update(
        uid=admin.id, 
        name='Moderator Chan',
        institution = 'US Census Bureau'
    )
    print("Admin Moderator Chan has been created! (1/2)")

    # Update Datasite

    admin_client.settings.allow_guest_signup(enable=True)

    new_welcome = '''
        <h2>Welcome to U.S. Stats</h2>
        <p><strong>Deployment Type:</strong> Local<br />
        <strong>Organization:</strong> U.S. Census Bureau<br />
        <strong>Website:</strong><a href="https://www.census.gov/">www.census.gov</a><br />
        <strong>Admin:</strong> Moderator Chan (admin@usstats.org)<br />

        <h3>About U.S. Stats</h3>
        <p>US Stats is a Datasite dedicated to the dissemination and repurposing of US Census Bureau microdata in efforts to promote statistical research and learning off of US population data for the public good.</p>
        '''

    admin_client.settings.welcome_customize(html=new_welcome)
    print("Datasite profile has been updated! (2/2)")


# Upload Datasets ---------------------------------------------------------------------------------

# LOAD ALL DATASETS TO MEM
def upload_datasets(port):
    import os
    current_directory = os.getcwd

    print("Loading data from 'github.com/OpenMined/design/user_tests/finding_data_091b/assets'...")

    # DP03 & DP05
    dp03_2015_local = pd.read_csv("https://raw.githubusercontent.com/OpenMined/design/main/user_tests/finding_data_091b/assets/acs2015_census_tract_data.csv")
    dp05_2015_local = pd.read_csv("https://raw.githubusercontent.com/OpenMined/design/main/user_tests/finding_data_091b/assets/acs2015_county_data.csv")
    # Adult Census
    adult_local = pd.read_csv("https://raw.githubusercontent.com/OpenMined/design/main/user_tests/finding_data_091b/assets/adult.csv")
    # Variability in Poverty
    pop_estimates_data_local = pd.read_csv("https://raw.githubusercontent.com/OpenMined/design/main/user_tests/finding_data_091b/assets/population_estimates_2015_data.csv")
    poverty_data_local = pd.read_csv("https://raw.githubusercontent.com/OpenMined/design/main/user_tests/finding_data_091b/assets/poverty_data_2015_data.csv")
    unemployment_local = pd.read_csv("https://raw.githubusercontent.com/OpenMined/design/main/user_tests/finding_data_091b/assets/unemployment_2015_data.csv")
    # US Economy Case Study
    avg_indv_income_local = pd.read_csv("https://raw.githubusercontent.com/OpenMined/design/main/user_tests/finding_data_091b/assets/average_indv_income_by_yr.csv")
    avg_house_sale_jan_local = pd.read_csv("https://raw.githubusercontent.com/OpenMined/design/main/user_tests/finding_data_091b/assets/avg_house_sale_jan.csv")
    avg_house_sale_us_local = pd.read_csv("https://raw.githubusercontent.com/OpenMined/design/main/user_tests/finding_data_091b/assets/avg_house_sale_us.csv")
    us_inflation_rate = pd.read_csv("https://raw.githubusercontent.com/OpenMined/design/main/user_tests/finding_data_091b/assets/us_inflation_rates.csv")
    # Gender Pay Gap
    current_pop_survey_local = pd.read_csv("https://raw.githubusercontent.com/OpenMined/design/main/user_tests/finding_data_091b/assets/CurrentPopulationSurvey_preview.csv")
    psid_local = pd.read_csv("https://raw.githubusercontent.com/OpenMined/design/main/user_tests/finding_data_091b/assets/PanelStudyIncomeDynamic_preview.csv")
    
    print("Data has been locally loaded! (1/4)")

# CREATE ASSETS
    print("Defining asset metadata...")
    
    # DP03 & DP05
    dp03_2015_asset = sy.Asset(
        name="ACS DP03 2015 Tract Data",
        data= dp03_2015_local,
        mock= dp03_2015_local
    )
    dp05_2015_asset = sy.Asset(
        name="ACS DP05 2015 Tract Data",
        data= dp05_2015_local,
        mock= dp05_2015_local
    )
    #Adult Census
    adult_asset = sy.Asset(
        name="Adult Income 2015",
        data= adult_local,
        mock= adult_local
    )
    # Variability
    population_asset = sy.Asset(
        name="Population Estimates 2015",
        data= pop_estimates_data_local,
        mock= pop_estimates_data_local
    )
    poverty_asset = sy.Asset(
        name="Poverty Data 2015",
        data= poverty_data_local,
        mock= poverty_data_local
    )
    unemployment_asset = sy.Asset(
        name="Unemployment Med 2015",
        data= unemployment_local,
        mock= unemployment_local
    )
    # US Economy
    indv_income_asset = sy.Asset(
        name="Average Individual Income By Year 1962-2021",
        data= avg_indv_income_local,
        mock= avg_indv_income_local
    )
    house_sale_jan_asset = sy.Asset(
        name="Average sales of Houses in Jan",
        data= avg_house_sale_jan_local,
        mock= avg_house_sale_jan_local
    )
    house_sale_us_asset = sy.Asset(
        name="Average sales of Houses in the US",
        data= avg_house_sale_us_local,
        mock= avg_house_sale_us_local
    )
    us_inflation_rate_asset = sy.Asset(
        name="US Historical Inflation Rates 1914-2022",
        data= us_inflation_rate,
        mock= us_inflation_rate
    )
    # Gender Pay Gap
    current_pop_survey_asset = sy.Asset(
        name="CurrentPopulationSurvey",
        data= current_pop_survey_local,
        mock= current_pop_survey_local,
        description = "Current Population Survey (CPS) data"
    )
    psid_local_asset = sy.Asset(
        name="PanelStudyIncomeDynamics",
        data= psid_local,
        mock= psid_local,
        description = "Panel Study of Income Dynamics (PSID) data"
    )
    print("Asset metadata has been defined! (2/4)")

#create_dp03_dp05_dataset
    print("Creating dataset metadata...")
    # DP03 & DP05
    acs_dataset_metadata = '''
    ## About Dataset
    __Content__
    The data here is taken from the DP03 and DP05 tables of the 2015 American Community Survey 5-year estimates.
    - acs2015_census_tract_data.csv: Data for each census tract in the US, including DC and Puerto Rico.
    - acs2015_county_data.csv: Data for each county or county equivalent in the US, including DC and Puerto Rico.
    
    The two files have the same structure, with just a small difference in the name of the id column. Counties are political subdivisions, and the boundaries of some have been set for centuries. Census tracts, however, are defined by the census bureau and will have a much more consistent size. A typical census tract has around 5000 or so residents.
    
    __Frequency__
    The American Community Survey is updated yearly.
    
    __Acceptable Use__
    The data here were collected by the US Census Bureau. As a product of the US federal government, this is not subject to copyright within the US.
    The data collected is available under GPL Licensing.
    
    __Potential Use Cases__
    There are many questions that we could try to answer with the data here. Can we predict things such as the state (classification) or household income (regression)? What kinds of clusters can we find in the data? What other datasets can be improved by the addition of census data?
    
    '''

    acs_contributor = sy.Contributor(
        name="US Census Bureau", 
        role="Dataset Source", 
        email="admin@usstats.org"
    )
    acs_dataset = sy.Dataset(
        name="US Census Demographic Data",
        description= acs_dataset_metadata,
        summary= "Demographic and Economic Data for Tracts and Counties",
        contributors = [acs_contributor]
    )
    acs_dataset.add_asset(dp03_2015_asset)
    acs_dataset.add_asset(dp05_2015_asset)
    
# create_adult_census_dataset():
    # ADULT CSV METADATA
    adult_metadata = '''
    ## About Dataset
    This data was extracted from the 2015 Census bureau database by Jane Doe Kohavi and John Doe (Data Mining and Visualization, Silicon Graphics). A set of reasonably clean records was extracted using the following conditions: ((AAGE>16) && (AGI>100) && (AFNLWGT>1) && (HRSWK>0)). The prediction task is to determine whether a person makes over $50K a year.
    
    __Description of fnlwgt (final weight)__
    The weights on the Current Population Survey (CPS) files are controlled to independent estimates of the civilian noninstitutional population of the US. These are prepared monthly for us by Population Division here at the Census Bureau. We use 3 sets of controls. These are:
    - A single cell estimate of the population 16+ for each state.
    - Controls for Hispanic Origin by age and sex.
    - Controls by Race, age and sex.
    
    We use all three sets of controls in our weighting program and "rake" through them 6 times so that by the end we come back to all the controls we used. The term estimate refers to population totals derived from CPS by creating "weighted tallies" of any specified socio-economic characteristics of the population. People with similar demographic characteristics should have similar weights. There is one important caveat to remember about this statement. That is that since the CPS sample is actually a collection of 51 state samples, each with its own probability of selection, the statement only applies within state.
    
    __Acceptable Use__
    The data collected is available under GPL Licensing.
    
    '''

    #Fillout Contributor
    adult_contributor = sy.Contributor(
        name="Jane Doe", 
        role="Dataset Creator", 
        email="jane@university.edu"
    )

    #Create Dataset
    adult_income_dataset = sy.Dataset(
        name="Adult Census Income",
        description= adult_metadata,
        summary= "Predict whether income exceeds $50K/yr based on census data",
        contributors = [adult_contributor]
    )
    #Add Asset
    adult_income_dataset.add_asset(adult_asset)

# create_variability_dataset():
    # Variability in Poverty CSV METADATA
    variability_poverty_metadata = '''
    ## About Dataset
    __Goal and Objective :__
    Primary objective is to study variability in the poverty rate in the US counties by means of one or more of independent or control variable and provide best suitable model to quantify relationships in determining target value
    Our goal is to design various models to take into consideration the effect of various factors like employment, population and education to predict the poverty rate in all US Counties
    We further wish to analyze the status of a county based on whether it is metropolitan or not.
    
    __List of Datasets__
    Socioeconomic indicators like poverty rates, population change, unemployment rates, and education levels vary geographically across U.S. States and counties
    - Unemployment
    - Poverty Estimates
    - Population Estimates
    
    All the three individual datasets have common unique id FIPS Code defined as State-County FIPS Code. It is unique for each county falling under the states. In our dataset, we are covering all 52 USA states including federal district DC and Puerto Rico.
    
    __Data Modelling__
    Target Variable: Metro_2015 – This binary variable shows status of County as Metro or Non-Metro
    A decision tree model designed using Metro_2015 as target variable will efficiently determine the classification of the population into Metro and Non-metro counties.
    Dataset will be partitioned into training and validation datasets before implementing decision tree rules.
    The attributes that will be considered in selecting best model will be fit statistics, misclassification rate, and average square error.
    
    Clustering can be performed to create the collection of objects similar to each other which will give insight into data distribution.
    Variables will be standardized before performing clustering to avoid noisy data and outliers. Euclidean distance will be the measure to determine stability and separation.
    
    __Recommendation :__
    The regression equation determines % Poverty rate in a particular county based on significant factors. This model can be
    This model can be used by education boards to increase or decrease the funds spent on the education system in different counties in order to lower the poverty rate.
    Census board can use this model in identifying poverty line index based on a population estimate an average household income.
    By estimating the poverty rate and considering factors like unemployment and education, an analysis can be done to set up employment opportunities in targeted counties.
    
    '''    
    #Fillout Contributor
    poverty_contributor = sy.Contributor(
        name="John Smith", 
        role="Dataset Creator", 
        email="john@university.edu"
    )

    #Create Dataset
    variability_poverty_dataset = sy.Dataset(
        name="variability in the poverty rate in the US counties",
        description= variability_poverty_metadata,
        summary= "variability in the poverty rate in the US counties",
        contributors = [poverty_contributor]
    )

    # Add Assets
    variability_poverty_dataset.add_asset(population_asset)
    variability_poverty_dataset.add_asset(poverty_asset)
    variability_poverty_dataset.add_asset(unemployment_asset)
    

# create_us_economy_dataset():
    # Create Metadata
    us_economy_metadata = '''
    ## About Dataset
    This dataset was inspired by rising prices for essential goods, the abnormally high inflation rate in March of 7.9 percent of this year, and the 30 trillion-dollar debt that we have. I was extremely curious to see how sustainable this is for the average American and if wages are increasing at the same rate to help combat this inflation. This is not politically driven in the slightest nor was this made to put the blame on Americans. This dataset was inspired by rising prices for essential goods and the abnormally high inflation rate in March of 7.9 percent of this year. I was extremely curious to see how sustainable this is for the average American and if wages are increasing at the same rate to help combat this inflation. This is not politically driven in the slightest nor was this made to put the blame on Americans. All of the datasets were obtained from third party sources websites such as https://dqydj.com/household-income-by-year/ and https://www.usinflationcalculator.com/inflation/historical-inflation-rates/ and only excluding https://fred.stlouisfed.org/series/ASPUS, which is first-party data.
    
    I labeled all of the datasets to be self-explanatory based off of the title of the datasets. Lastly, the Average Sales of Houses in Jan is just a filtered version of "Average Sales of Houses in the US" dataset.
    
    __License__
    CC0: Public Domain
    
    '''

    # Define Contributor
    economy_contributor = sy.Contributor(
        name="Charles Schwett", 
        role="Dataset Creator", 
        email="cs@gmail.com"
    )
    # Define Dataset
    us_economy_dataset = sy.Dataset(
        name="US Economy Case Study",
        description= us_economy_metadata,
        summary= "How well is the U.S. economy doing according to government's standards?",
        contributors = [economy_contributor]
    )
    # Add Assets
    us_economy_dataset.add_asset(indv_income_asset)
    us_economy_dataset.add_asset(house_sale_jan_asset)
    us_economy_dataset.add_asset(house_sale_us_asset)
    us_economy_dataset.add_asset(us_inflation_rate_asset)

# create_gender_pay_gap_dataset():
    # Define Metadata
    gender_pay_gap_metadata = '''
    ## About Dataset
    ### Context
    The gender pay gap or gender wage gap is the average difference between the remuneration for men and women who are working. Women are generally considered to be paid less than men. There are two distinct numbers regarding the pay gap: non-adjusted versus adjusted pay gap. The latter typically takes into account differences in hours worked, occupations were chosen, education, and job experience. In the United States, for example, the non-adjusted average female's annual salary is 79% of the average male salary, compared to 95% for the adjusted average salary.
    
    The reasons link to legal, social, and economic factors, and extend beyond "equal pay for equal work".
    
    The gender pay gap can be a problem from a public policy perspective because it reduces economic output and means that women are more likely to be dependent upon welfare payments, especially in old age.
    
    This dataset aims to replicate the data used in the famous paper "The Gender Wage Gap: Extent, Trends, and Explanations", which provides new empirical evidence on the extent of and trends in the gender wage gap, which declined considerably during the 1980–2010 period.
    
    ### Content
    There are 2 files in this dataset: a) the Panel Study of Income Dynamics (PSID) microdata over the 1980-2010 period, and b) the Current Population Survey (CPS) to provide some additional US national data on the gender pay gap.
    
    __PSID Variables__
    > __NOTES:__ THE VARIABLES WITH fz ADDED TO THEIR NAME REFER TO EXPERIENCE WHERE WE HAVE FILLED IN SOME ZEROS IN THE MISSING PSID YEARS WITH DATA FROM THE RESPONDENTS’ ANSWERS TO QUESTIONS ABOUT JOBS WORKED ON DURING THESE MISSING YEARS. THE fz variables WERE USED IN THE REGRESSION ANALYSES
    > THE VARIABLES WITH A predict PREFIX REFER TO THE COMPUTATION OF ACTUAL EXPERIENCE ACCUMULATED DURING THE YEARS IN WHICH THE PSID DID NOT SURVEY THE RESPONDENTS. THERE ARE MORE PREDICTED EXPERIENCE LEVELS THAT ARE NEEDED TO IMPUTE EXPERIENCE IN THE MISSING YEARS IN SOME CASES.
    > NOTE THAT THE VARIABLES yrsexpf, yrsexpfsz, etc., INCLUDE THESE COMPUTATIONS, SO THAT IF YOU WANT TO USE FULL TIME OR PART TIME EXPERIENCE, YOU DON’T NEED TO ADD THESE PREDICT VARIABLES IN. THEY ARE INCLUDED IN THE DATA SET TO ILLUSTRATE THE RESULTS OF THE COMPUTATION PROCESS.
    > THE VARIABLES WITH AN orig PREFIX ARE THE ORIGINAL PSID VARIABLES. THESE HAVE BEEN PROCESSED AND IN SOME CASES RENAMED FOR CONVENIENCE. THE hd SUFFIX MEANS THAT THE VARIABLE REFERS TO THE HEAD OF THE FAMILY, AND THE wf SUFFIX MEANS THAT IT REFERS TO THE WIFE OR FEMALE COHABITOR IF THERE IS ONE. AS SHOWN IN THE ACCOMPANYING REGRESSION PROGRAM, THESE orig VARIABLES AREN’T USED DIRECTLY IN THE REGRESSIONS. THERE ARE MORE OF THE ORIGINAL PSID VARIABLES, WHICH WERE USED TO CONSTRUCT THE VARIABLES USED IN THE REGRESSIONS. HD MEANS HEAD AND WF MEANS WIFE OR FEMALE COHABITOR.
    
    1. intnum68: 1968 INTERVIEW NUMBER
    2. pernum68: PERSON NUMBER 68
    3. wave: Current Wave of the PSID
    4. sex: gender SEX OF INDIVIDUAL (1=male, 2=female)
    5. intnum: Wave-specific Interview Number
    6. farminc: Farm Income
    7. region: regLab Region of Current Interview
    8. famwgt: this is the PSID’s family weight, which is used in all analyses
    9. relhead: ER34103L this is the relation to the head of household (10=head; 20=legally married wife; 22=cohabiting partner)
    10. age: Age
    11. employed: ER34116L Whether or not employed or on temp leave (everyone gets a 1 for this variable, since our wage analyses use only the currently employed)
    12. sch: schLbl Highest Year of Schooling
    13. annhrs: Annual Hours Worked
    14. annlabinc: Annual Labor Income
    15. occ: 3 Digit Occupation 2000 codes
    16. ind: 3 Digit Industry 2000 codes
    17. white: White, nonhispanic dummy variable
    18. black: Black, nonhispanic dummy variable
    19. hisp: Hispanic dummy variable
    20. othrace: Other Race dummy variable
    21. degree: degreeLbl Agent's Degree Status (0=no college degree; 1=bachelor’s without advanced degree; 2=advanced degree)
    22. degupd: degreeLbl Agent's Degree Status (Updated with 2009 values)
    23. schupd: schLbl Schooling (updated years of schooling)
    24. annwks: Annual Weeks Worked
    25. unjob: unJobLbl Union Coverage dummy variable
    26. usualhrwk: Usual Hrs Worked Per Week
    27. labincbus: Labor Income from Business
    28. yrsexp: Experience
    29. yrsftexp: FT Experience
    30. yrsptexp: PT Experience
    31. yrsptexpsq: PT Experience^2
    32. yrsftexpsq: FT Experience^2
    33. yrsExpSq: Experience^2
    34. yrsexpfz: Experience (filling in zeros)
    35. yrsftexpfz: FT Experience (filling in zeros)
    36. yrsptexpfz: Years of Part-Time Experience (Filling in zeros)
    37. yrsexpfzsq: Experience^2 (filling in zeros)
    38. yrsftexpfzsq: FT Experience^2 (filling in zeros)
    39. wtrgov: Works in Government (dummy variable)
    40. selfemp: selfEmpLbl =1 If Self Employed for ANY Job in the Current Wave. Everyone gets a zero for this variable because our wage analyses only include wage and salary workers.
    41. predict98: Total Experience must be predicted for 1998
    42. predictft98: FT Experience must be predicted for 1998
    43. predict00: Total Experience must be predicted for 2000
    44. predictft00: Experience must be predicted for 2000
    45. predict02: Total Experience must be predicted for 2002
    46. predictft02: FT Experience must be predicted for 2002
    47. predict04: Total Experience must be predicted for 2004
    48. predictft04: FT Experience must be predicted for 2004
    49. predict06: Total Experience must be predicted for 2006
    50. predictft06: FT Experience must be predicted for 2006
    51. predict08: Total Experience must be predicted for 2008
    52. predictft08: FT Experience must be predicted for 2008
    53. predict1: Total Experience must be predicted for 2010
    54. predictft10: FT Experience must be predicted for 2010
    55. origage:
    56. origannHrsHD:
    57. origannHrsWF:
    58. origannLabIncHD:
    59. origannLabIncWF:
    60. origannWeeksHD:
    61. origannWeeksWF:
    62. origcurrHrWkHD:
    63. origcurrHrWkWF:
    64. origdegreeHD:
    65. origdegreeWF:
    66. origemp: ER34116L
    67. origeverwrkHD07: ER36351L BC62 WTR EVER WORKED
    68. origeverwrkHD09: ER42376L BC62 WTR EVER WORKED
    69. origeverwrkHD11: ER47689L BC62 WTR EVER WORKED
    70. origeverwrkHD99: ER13476L C4 EVER WORKED? (HD-U)
    71. origeverwrkWF07: ER36609L DE62 WTR EVER WORKED
    72. origeverwrkWF09: ER42628L DE62 WTR EVER WORKED
    73. origeverwrkWF11: ER47946L DE62 WTR EVER WORKED
    74. origeverwrkWF99: ER13988L E4 EVER WORKED? (WF-U)
    75. origfamWgt:
    76. origfarmInc:
    77. origindHD:
    78. origindWF:
    79. origmarSt: ER47323L
    80. orignumChld: ER47320L
    81. origoccHD:
    82. origoccWF:
    83. origraceHD: ER51904L
    84. origraceWF: ER51810L
    85. origregion: ER52398L
    86. origrelHead: ER34103L
    87. origsch: ER34119L
    88. origschfamHD07: ER41037L COMPLETED ED-HD
    89. origschfamHD09: ER46981L COMPLETED ED-HD
    90. origschfamHD11: ER52405L COMPLETED ED-HD
    91. origschfamHD81: V8039L M28 EDUCATION-HD
    92. origschfamHD99: ER16516L COMPLETED ED-HD
    93. origschfamWF07: ER41038L COMPLETED ED-WF
    94. origschfamWF09: ER46982L COMPLETED ED-WF
    95. origschfamWF11: ER52406L COMPLETED ED-WF
    96. origschfamWF81: V7998L L2 EDUCATION-WF
    97. origschfamWF99: ER16517L COMPLETED ED-WF
    98. origsexHead: ER47318L
    99. origspanHD: ER51903L Spanish Descent Head
    100. origspanWF: ER51809L Spanish Descent Wife
    101. origstopw~DE299: ER13307L B53 STOP WRK OTR EMP H-E
    102. origstopw~DE399: ER13388L B92 STOP WRK XJOB1 (H-E)
    103. origstopw~DE499: ER13413L B104 STOP WORK XJOB2 H-E
    104. origstopw~DE599: ER13437L B116 STOP WRK XTRA JOB3
    105. origstopw~DE699: ER13461L B128 STOP WRK XTRA JOB4
    106. origstopw~DU299: ER13560L C45 STOP WRK OTR EMP H-U
    107. origstopw~DU399: ER13641L C84 STOP WORK XJOB1 H-U
    108. origstopw~DU499: ER13665L C96 STOP WORK XJOB2 H-U
    109. origstopw~DU599: ER13689L C108 STOP WRK XTRA JOB3
    110. origstopw~DU699: ER13713L C120 STOP WRK XTRA JOB4
    111. origstopw~FE299: ER13819L D53 STOP WRK OTR EMP W-E
    112. origstopw~FE399: ER13900L D92 STOP WRK XJOB1 (W-E)
    113. origstopw~FE499: ER13925L D104 STOP WRK XJOB2 W-E
    114. origstopw~FE599: ER13949L D116 STOP WRK XTRA JOB3
    115. origstopw~FE699: ER13973L D128 STOP WRK XTRA JOB4
    116. origstopw~FU299: ER14072L E45 STOP WRK OTR EMP W-U
    117. origstopw~FU399: ER14153L E84 STOP WORK XJOB1 W-U
    118. origstopw~FU499: ER14177L E96 STOP WORK XJOB2 W-U
    119. origstopw~FU599: ER14201L E108 STOP WRK XTRA JOB3
    120. origstopw~FU699: ER14225L E120 STOP WRK XTRA JOB4
    121. origtotYrsFTHD: ER51956L
    122. origtotYrsFTWF: ER51862L
    123. origtotYrsHD: ER51955L
    124. origtotYrsWF: ER51861L
    125. origunJobHD: ER47491L
    126. origunJobWF: ER47748L
    127. origwrkPriorJ~D: ER47453L
    128. origwrkPriorJ~F: ER47710L
    129. origwtrNewHD: ER51865L
    130. origwtrNewWF: ER51771L
    131. origyrNewHD: this is PSID start year
    132. origyrNewWF: this is PSID start year
    133. origyrsFTEXp: ER47462L
    134. origyrsFTHD: ER34122L
    135. origyrsFTWF: ER34123L
    136. origyrsPTExp: ER47464L
    137. origyrsPTExpHD: ER34124L
    138. origyrsPTExpWF: ER34125L
    139. origyrsexp: ER47460L
    140. origyrsftexp: ER47461L
    141. origyrsptexp: ER47463L
    142. origyrsexpfz:
    143. origyrsftexpfz: ER47465L
    144. origyrsptexpfz: ER47466L
    145. origyrsftexpfzsq: ER47468L
    146. origyrsptexpfzsq: ER47470L
    147. origyrsexpfzsq: ER47467L
    148. origyrsexpsq: ER47469L
    149. origyrsftexpsq: ER47471L
    150. origyrsptexpsq: ER47472L
    151. region5: 5-region variable
    152. rural: Labeled as "Urban or rural." 1 if rural, 0 otherwise.
    153. urban: Labeled as "Urban or rural." 1 if urban, 0 otherwise.
    154. rural2: Labeled as "Urban or rural." 1 if rural, 0 otherwise.
    155. schAge: Computed age from the schooling variable
    156. unjobHD: Union Status of Head of Household
    157. unjobWF: Union Status of Wife
    158. yrsexpFZ: Experience (Filling in Zeros)
    159. yrsFTExpFZ: Full-Time Experience (Filling in Zeros)
    160. yrsPTExpFZ: Part-Time Experience (Filling in Zeros)
    161. yrsexpFZSq: Experience Squared (Filling in Zeros)
    162. yrsFTExpFZSq: Full-Time Experience Squared (Filling in Zeros)
    163. yrsPTExpFZSq: Part-Time Experience Squared (Filling in Zeros)
    164. predictfz08: fz Total Experience must be predicted for 2008
    165. predictftfz08: fz FT Experience must be predicted for 2008
    166. predict2009: Total Experience must be predicted for 2009
    167. predictft2009: FT Experience must be predicted for 2009
    168. predictfz09: fz Total Experience must be predicted for 2009
    169. predictftfz09: fz FT Experience must be predicted for 2009
    170. predictfz10: fz Total Experience must be predicted for 2010
    171. predictftfz10: fz FT Experience must be predicted for 2010
    172. predict2011: Total Experience must be predicted for 2011
    173. predictft2011: FT Experience must be predicted for 2011
    174. predictfz11: fz Total Experience must be predicted for 2011
    175. predictftfz11: fz FT Experience must be predicted for 2011
    176. origAdvHD: Adv is advanced degree
    177. origAdvWF:
    178. origBAHD: BA is bachelor’s degree
    179. origBAWF:
    180. origannWeeksHDE: annWeeks is annual weeks worked E means currently employed
    181. origannWeeksHDR: R means currently retired
    182. origannWeeksHDU: U means currently not employed
    183. origannWeeksWFE:
    184. origannWeeksWFR:
    185. origannWeeksWFU:
    186. origindHDE: ind is industry
    187. origindWFE:
    188. origindHDU:
    189. origindWFU:
    190. origindHDR:
    191. origindWFR:
    192. origoccHDE: occ is occupation
    193. origoccHDR:
    194. origoccHDU:
    195. origoccWFE:
    196. origoccWFR:
    197. origoccWFU:
    198. origrace: race is race
    199. origschHD: sch is years of schooling
    200. origschWF:
    201. origyrHghstDe~D: yrHghstDegHD is year of highest degree for head
    202. origyrHghstDe~F:
    203. origwtrCollDe~D: whether college degree
    204. origwtrCollDe~F:
    205. origwtrCollHD: whether attended college
    206. origwtrCollWF:
    207. predict: ==1 if Logit Prediction Needed for ANY gap year
    208. predictft: ==1 if FT Logit Prediction Needed for ANY gap year
    209. smsa: SMSA dummy variable variable
    210. perconexp: T-1 Personal Consumption Expenditure
    211. hrwage: hourly wage
    212. annhrs2: alternate measure of annual hours worked
    213. expendbase10: level of National Income and Products Account Personal Consumption Expenditures (PCE) price deflator for 2010
    214. inflate: inflation factor to multiply earnings by in order to convert to 2010 dollars
    215. realhrwage: Real Hourly Wage in 2010 PCE corrected dollars
    216. immigrantsamp: Immigrant Sub-Sample (zero for everyone since we don’t use the immigrant subsample)
    217. northeast: Region: North-East
    218. northcentral: Region: North-Central
    219. south: Region: South
    220. west: Region: West, Alaska and Hawaii
    221. lnrealwg: Log(Real Hourly Wage)
    222. ft: full time work dummy variable
    223. potexp: potential experience (age-years of schooling-6) truncated to be between 0 and age-18
    224. potexp2: potential experience squared
    225. ba: bachelor's Degree
    226. adv: advanced Degree
    227. military: zero for everyone since we study civilians
    228. basesamp: this is base sample, which is 1 for everyone in this data set
    229. wagesamp: this is wage sample
    230. female:
    231. ind2: 2-digit Industry
    232. occ2: 2-digit Occupation
    233. occ2name:
    234. Agriculture:
    235. miningconstru~n: Ind: Mining and Construction
    236. durables: Ind: Durables Manufacturing
    237. nondurables: Ind: Non-durables Manufacturing
    238. Transport: Ind: Transport
    239. Utilities: Ind: Utilities
    240. Communications: Ind: Communications
    241. retailtrade: Ind: Retail Trade
    242. wholesaletrade: Ind: Wholesale Trade
    243. finance: Ind: Finance
    244. SocArtOther: Ind: Social Work, Arts and Recreation, Other Services
    245. hotelsrestaur~s: Ind: Hotels and Restaurants
    246. Medical: Ind: Medical
    247. Education: Ind: Education
    248. professional: Ind: Professional Services
    249. publicadmin: Ind: Public Administration
    250. sumind: this is the sum of industry dummy variables, which is 1 for everyone
    251. manager: Manager
    252. business: Business Operations Specialists
    253. financialop: Financial Operations Specialists
    254. computer: Computer and Math Technicians
    255. architect: Architects an Engineers
    256. scientist: Life, Physical and Social Sciences
    257. socialworker: Community and Social Workers
    258. postseceduc: Post-secondary educators
    259. legaleduc: Other Education, Training, Library and Legal Occupations
    260. artist: Arts, Design, Entertainment, Sports and Media
    261. lawyerphysician: Physicians and Dentists
    262. healthcare: Nurses and HealthCare Practitioners and Technicians
    263. healthsupport: Healthcare Support Occupations
    264. protective: Protective Service Occupations
    265. foodcare: Food Preparation and Serving and Personal Care Services
    266. building: Building and Grounds Cleaning and Maintenance
    267. sales: Sales and Related
    268. officeadmin: Office and Administrative Support
    269. farmer:
    270. constructextr~l: Construction, Extraction, Installation
    271. production: Production
    272. transport: Transportation and Materials Moving
    273. sumocc: this is sum of the occupation dummy variables which is 1 for everyone
    274. LEHS: High School or Less
    
    
    __CPS variables:__
    
    > NOTES: VARIABLES WITH A q AT THE BEGINNING ARE DATA QUALITY FLAGS. ANY VALUE GREATER THAN ZERO INDICATES SOME ISSUE WITH DATA QUALITY. THE EARNINGS DATA WITH ZEROS WAS ONLY USED DURING THE CREATION OF THIS VARIABLE. DUE TO LACK OF DATA AVAILABILITY for 1981, ALL OF THE HOURS AND WEEKS DATA WERE FORCED TO USE REGARDLESS OF THE DATA QUALITY FLAG.
    > THE ORIGINAL CPS VARIABLES HAVE BEEN KEPT.
    > OCCUPATION AND INDUSTRY WERE NOT USED IN THE CPS ANALYSIS.
    > THE VARIABLES WITH tc AT THE BEGINNING INDICATE TOPCODED VALUES.
    
    1. year: Survey year
    2. serial: Household serial number
    3. numprec: Number of person records following
    4. hwtsupp: hwtsupp_lbl Household weight, Supplement
    5. gq: gq_lbl Group Quarters status
    6. region: region_lbl Region and division
    7. statefip: statefip_lbl State (FIPS code)
    8. metro: metro_lbl Metropolitan central city status
    9. metarea: metarea_lbl Metropolitan area
    10. county: FIPS county code
    11. farm: farm_lbl Farm (1=this is a farm, 2= it’s not a farm)
    12. month: month_lbl Month
    13. pernum: Person number in sample unit
    14. wtsupp: Supplement Weight
    15. relate: relate_lbl Relationship to household head (Head/hous=101, Spouse=201, Child=301, Stepchild=303, Parent=501, Sibling=701, Grandchil=901, Other rel=1001, Partner/r=1113, Unmarried=1114, Housemate=1115, Roomer/bo=1241, Foster ch=1242, Other non=1260)
    16. age: age_lbl Age
    17. sex: sex_lbl Sex (1=male, 2=female)
    18. race: raceLbl Race (White nonhisp=1, Black nonhisp=2, Hispanic=3, Other nonhisp=4)
    19. marst: marst_lbl Marital status (Married, spouse present=1, Married, spouse absent=2, Separated=3, Divorced=4, Widowed=5, Never mar=6)
    20. popstat: popstat_lbl Adult civilian, armed forces, or Child (1 for everyone—we include only civilian adults)
    21. bpl: bpl_lbl Birthplace
    22. yrimmig: yrimmig_lbl Year of immigration
    23. citizen: citizen_lbl Citizenship status
    24. mbpl: mbpl_lbl Mother's birthplace
    25. fbpl: fbpl_lbl Father's birthplace
    26. nativity: nativity_lbl Foreign birthplace or parentage
    27. hispan: hispan_lbl Hispanic origin
    28. sch: educLbl Educational attainment recode (None=0, 1=1, Grades 1=2, 2.5=2.5, 3=3, 4=4, Grades 5=5, 5.5=5.5, 6=6, Grades 7=7, 7.5=7.5, 8=8, Grade 9=9, Grade 10=10, Grade 11=11, Grade 12=12, Some Coll=13, Assoc.=14, BA=16, Adv. Degr=18)
    29. educ99: educ99_lbl Educational attainment, 1990, available for 1999 and later (No school=1, 1st-4th g=4, 5th-8th g=5, 9th grade=6, 10th grad=7, 11th grad=8, 12th grad=9, High scho=10, Some coll=11, Associate=13, Associate=14, Bachelors=15, Masters d=16, Professio=17, Doctorate=18)
    30. schlcoll: schlcoll_lbl School or college attendance; available only in 2013 (High school full time=1, High school part time=2, College or univ full time=3, College or univ part time=4, Does not attend school=5)
    31. empstat: empstat_lbl Employment status (At work=10, Has job, not at work now=12)
    32. labforce: labforce_lbl Labor force status everyone gets a 2—in the labor force
    33. occ: occ_lbl Occupation
    34. occ1990: occ1990_lbl Occupation, 1990 basis
    35. ind1990: ind1990_lbl Industry, 1990 basis
    36. occ1950: occ1950_lbl Occupation, 1950 basis
    37. ind: ind_lbl Industry
    38. ind1950: ind1950_lbl Industry, 1950 basis
    39. classwkr: classwkr_lbl Class of worker (Self-empl=10, Wage/salary, private sector=21, Wage/salary, government=24, Federal govt employee=25, State govt employee=27, Local govt employee=28, Unpaid family worker=29)
    40. occly: occly_lbl Occupation last year
    41. occ50ly: occ50ly_lbl Occupation last year, 1950 basis
    42. indly: indly_lbl Industry last year
    43. ind50ly: ind50ly_lbl Industry last year, 1950 basis
    44. classwly: classwly_lbl Class of worker last year (Self-employed=14, Wage/salary private=22, Federal govt=25, State gov=27, Local gov=28, Unpaid family worker=29)
    45. wkswork1: wkswork1_lbl Weeks worked last year
    46. wkswork2: wkswork2_lbl Weeks worked last year, intervalled
    47. hrswork: hrswork_lbl Hours worked last week
    48. uhrswork: uhrswork_lbl Usual hours worked per week (last yr)
    49. union: union_lbl Union membership (only available for outgoing rotation group) (NIU=0, No union coverage=1, Member of labor union=2, Covered by union but not a member=3)
    50. incwage: incwage_lbl Wage and salary income
    51. incbus: incbus_lbl Non-farm business income
    52. incfarm: incfarm_lbl Farm income
    53. inclongj: inclongj_lbl Earnings from longest job
    54. oincwage: oincwage_lbl Earnings from other work included wage and salary earnings
    55. srcearn: srcearn_lbl Source of earnings from longest (1=wage and salary; 4=without pay) job
    56. ftype: ftype_lbl Family Type (Primary family=1, Nonfamily householder=2, Related subfamily=3, Unrelated subfamily=4, Secondary individual=5)
    57. quhrswor: quhrswor_lbl Data quality flag for UHRSWORK
    58. qwkswork: qwkswork_lbl Data quality flag for WKSWORK1 and WKSWORK2
    59. qincbus: qincbus_lbl Data quality flag for INCBUS
    60. qincfarm: qincfarm_lbl Data quality flag for INCFARM
    61. qinclong: qinclong_lbl Data quality flag for INCLONGJ
    62. qincwage: qincwage_lbl Data quality flag for INCWAGE
    63. qsrcearn: qsrcearn_lbl Data quality flag for SRCEARN
    64. o_numprec: Original Number of person records following
    65. o_hwtsupp: Original Household weight, Supplement
    66. o_gq: Original Group Quarters status
    67. o_region: Original Region and division
    68. o_statefip: Original State (FIPS code)
    69. o_metro: Original Metropolitan central city status
    70. o_metarea: Original Metropolitan area
    71. o_county: Original FIPS county code
    72. o_farm: Original Farm
    73. o_month: Original Month
    74. o_pernum: Original Person number in sample unit
    75. o_wtsupp: Original Supplement Weight
    76. o_relate: Original Relationship to household head
    77. o_age: Original Age
    78. o_sex: Original Sex
    79. o_race: Original Race
    80. o_marst: Original Marital status
    81. o_popstat: Original Adult civilian, armed forces, or child
    82. o_bpl: Original Birthplace
    83. o_yrimmig: Original Year of immigration
    84. o_citizen: Original Citizenship status
    85. o_mbpl: Original Mother's birthplace
    86. o_fbpl: Original Father's birthplace
    87. o_nativity: Original Foreign birthplace or parentage
    88. o_hispan: Original Hispanic origin
    89. o_educ: Original Educational attainment recode
    90. o_educ99: Original Educational attainment, 1990
    91. o_schlcoll: Original School or college attendance
    92. o_empstat: Original Employment status
    93. o_labforce: Original Labor force status
    94. o_occ: Original Occupation
    95. o_occ1990: Original Occupation, 1990 basis
    96. o_ind1990: Original Industry, 1990 basis
    97. o_occ1950: Original Occupation, 1950 basis
    98. o_ind: Original Industry
    99. o_ind1950: Original Industry, 1950 basis
    100. o_classwkr: Original Class of worker
    101. o_occly: Original Occupation last year
    102. o_occ50ly: Original Occupation last year, 1950 basis
    103. o_indly: Original Industry last year
    104. o_ind50ly: Original Industry last year, 1950 basis
    105. o_classwly: Original Class of worker last year
    106. o_wkswork1: Original Weeks worked last year
    107. o_wkswork2: Original Weeks worked last year, intervalled
    108. o_hrswork: Original Hours worked last week
    109. o_uhrswork: Original Usual hours worked per week (last yr)
    110. o_union: Original Union membership
    111. o_incwage: Original Wage and salary income
    112. o_incbus: Original Non-farm business income
    113. o_incfarm: Original Farm income
    114. o_inclongj: Original Earnings from longest job
    115. o_oincwage: Original Earnings from other work included wage and salary earnings
    116. o_srcearn: Original Source of earnings from longest job
    117. o_ftype: Original Family Type
    118. o_quhrswor: Original Data quality flag for UHRSWORK
    119. o_qwkswork: Original Data quality flag for WKSWORK1 and WKSWORK2
    120. o_qincbus: Original Data quality flag for INCBUS
    121. o_qincfarm: Original Data quality flag for INCFARM
    122. o_qincwage: Original Data quality flag for INCWAGE
    123. origrace: race_lbl Race
    124. white: white nonhispanic dummy variable
    125. black: black nonhispanic dummy variable
    126. hisp: Hispanic dummy variable
    127. othrace: other race dummy variable
    128. educorig: original education codes (see CPS documentation site mentioned above)
    129. ba: bachelor’s degree dummy variable
    130. adv: advanced degree dummy variable
    131. groupquar: group quarters dummy variable. Zero for everyone.
    132. potexp: age-yrs of schooling-6
    133. potexp2: potexp squared
    134. selfemp: self employment dummy variable. Zero for everyone.
    135. military: =1 if military (Based on popstat variable). Variable is zero for everyone.
    136. employed: equals 1 for everyone
    137. annhrs: annual work hours
    138. ft: full time work dummy variable
    139. niincwage: Not Imputed incwage
    140. incwageman: Manually Created INCWAGE
    141. tcoincwage
    142. tcinclongj
    143. tcincwage: True Topcoded INCWAGE (Includes Imputed Values)
    144. hrwage: hourly wage
    145. perconexp: T-1 Personal Consumption Expenditure
    146. expendbase10: 2010 PCE value
    147. inflate: inflation factor for expressing wages in 2010 dollars
    148. realhrwage: Real Hourly Wage, inflated to 2010 dollars
    149. uncenrealhrwage: Real Hourly Wage (same as realhrwage)
    150. lnrwg: log of real hourly wage
    151. hdwfcoh: Head/Wife/Cohabitator Indicator
    152. notalloc: not allocated wage. Equals 1 for everyone.
    153. basesamp: base sample; 1 for everyone
    154. wagesamp: wage sample dummy variable
    155. occ_orig
    156. adj_occ: in some years, occupation has four digits and in others it has 3. This expresses occupation in 3 digits
    157. occ_2010_orig
    158. ind_orig
    159. adj_ind
    160. ind_2002_orig
    161. ind_2007_orig
    162. occ_81
    163. ind_81
    164. occ_2000female: 2000 Occupation Code
    165. unmatched_fe~81
    166. occ_2000male: 2000 Occupation Code
    167. unmatched_ma~81
    168. ind_2000
    169. occ2000_81: 1981 occupation codes converted to 2000 codes
    170. ind2000_81: 1981 industry codes converted to 2000 codes
    171. occ_1990
    172. ind_1990
    173. occ_1999
    174. ind_1999
    175. unmatched_oc~90
    176. occ2000_90: 1990 occupation codes converted to 2000 codes
    177. unmatched_in~90
    178. ind2000_90: 1990 industry codes converted to 2000 codes
    179. indname2000_90
    180. unmatched_oc~99
    181. occ2000_99: 1990 occupation codes converted to 2000 codes
    182. unmatched_in~99
    183. ind2000_99: 1990 industry codes converted to 2000 codes
    184. indname2000_99
    185. un_lnrealwg: Log of Real Hourly Wage
    186. northeast: Region: North-East
    187. northcentral: Region: North-Central
    188. south: Region: South
    189. west: Region: West, Alaska and Hawaii
    190. female
    191. adj_ind2
    192. adj_occ2
    193. adj_occ2name
    194. Agriculture
    195. miningconstru~n: adj_ind: Mining and Construction
    196. durables: adj_ind: Durables Manufacturing
    197. nondurables: adj_ind: Non-durables
    198. Manufacturing
    199. Transport: adj_ind: Transport
    200. Utilities: adj_ind: Utilities
    201. Communications: adj_ind: Communications
    202. retailtrade: adj_ind: Retail Trade
    203. wholesaletrade: adj_ind: Wholesale Trade
    204. finance: adj_ind: Finance
    205. SocArtOther: adj_ind: Social Work, Arts and Recreation, Other Services
    206. hotelsrestaur~s: adj_ind: Hotels and Restaurants
    207. Medical: adj_ind: Medical
    208. Education: adj_ind: Education
    209. professional: adj_ind: Professional Services
    210. publicadmin: adj_ind: Public Administration
    211. sumadj_ind: sum of industry dummy variables
    212. manager: Manager
    213. business: Business Operations Specialists
    214. financialop: Financial Operations Specialists
    215. computer: Computer and Math Technicians
    216. architect: Architects an Engineers
    217. scientist: Life, Physical and Social Sciences
    218. socialworker: Community and Social Workers
    219. postseceduc: Post-secondary educators
    220. legaleduc: Other Education, Training, Library and Legal adj_occupations
    221. artist: Arts, Design, Entertainment, Sports and Media
    222. lawyerphysician: Physicians and Dentists
    223. healthcare: Nurses and HealthCare Practitioners and Technicians
    224. healthsupport: Healthcare Support adj_occupations
    225. protective: Protective Service adj_occupations
    226. foodcare: Food Preparation and Serving and Personal Care Services
    227. building: Building and Grounds Cleaning and Maintenance
    228. sales: Sales and Related
    229. officeadmin: Office and Administrative Support
    230. farmer
    231. constructextr~l: Construction, Extraction, Installation
    232. production: Production
    233. transport: Transportation and Materials Moving
    234. sumadj_occ: sum of occupation dummy variables
    235. LEHS: dummy for less than or equal to high school
    
    ### License
    Data files © Original Authors
    You must contact Sally Mae at sally@univeristy.edu in order to gain permission to compute off of this dataset.
    
    '''

    # Define Contributor
    pay_gap_contributor = sy.Contributor(
        name="Sally Mae", 
        role="Dataset Creator", 
        email="sally@univeristy.ed"
    )
    # Define Datasets
    pay_gap_dataset = sy.Dataset(
        name="Gender Pay Gap Dataset",
        description= gender_pay_gap_metadata,
        summary= "The Gender Wage Gap: Extent, Trends, and Explanations for differences in Salary",
        contributors = [pay_gap_contributor]
    )
    # Add Assets
    pay_gap_dataset.add_asset(psid_local_asset)
    pay_gap_dataset.add_asset(current_pop_survey_asset)
    
    print("Finished creating dataset metadata! (3/4)")
    
# Upload Datasets
    print("Uploading datasets to datasite...")
    admin_client = sy.login(email="info@openmined.org", password="changethis", port=port)
    admin_client.upload_dataset(dataset= acs_dataset)
    admin_client.upload_dataset(dataset= adult_income_dataset)
    admin_client.upload_dataset(dataset= variability_poverty_dataset)
    admin_client.upload_dataset(dataset= us_economy_dataset)
    admin_client.upload_dataset(dataset= pay_gap_dataset)
    print("Test datasets have been uploaded to US Stats datasite! (4/4)")
    print("You may now begin the test!")

        



#CONFIRMATION ----------------------------------------------------------------------------------------
print("Test Environment functions have been created!")