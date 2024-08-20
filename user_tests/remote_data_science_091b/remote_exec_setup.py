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

    print("Loading data from 'github.com/OpenMined/design/user_tests/remote_data_science_091b/assets'...")

    # Ages Dataset Upload
    age_local = pd.read_csv("https://raw.githubusercontent.com/OpenMined/design/main/user_tests/remote_data_science_091b/assets/ages_dataset_revised.csv")
    mock_local = pd.read_csv("https://raw.githubusercontent.com/OpenMined/design/main/user_tests/remote_data_science_091b/assets/mock_ages_dataset_revised.csv")
    
    print("Data has been locally loaded! (1/4)")
# --------------
# CREATE Dataset
    print("Defining dataset metadata...")
    age_dataset = sy.Dataset(
        name="Ages Dataset",
        description="""
        We developed a five-step method and inferred birth and death years, binary gender, and occupation from community-submitted data to all language versions
        of the Wikipedia project. The dataset is the largest on notable deceased people and includes individuals from a variety of social groups, including but
        not limited to 107k females, 124 non-binary people, and 90k researchers, who are spread across more than 300 contemporary or historical regions. The
        final product provides new insights into the demographics of mortality in relation to gender and profession in history. The technical method 
        demonstrates the usability of the latest text mining approaches to accurately clean historical data and reduce the missing values.
        """,
        summary="Dataset comparing occupation and lifespan.", 
        url="http://workshop-proceedings.icwsm.org/abstract?id=2022_82",
        citation="Annamoradnejad, Issa; Annamoradnejad, Rahimberdi (2022), “Age dataset: A structured general-purpose dataset on life, work, and death of 1.22 million distinguished people”, In Workshop Proceedings of the 16th International AAAI Conference on Web and Social Media (ICWSM), doi: 10.36190/2022.82",
        asset_list=[
            sy.Asset(
                name="Subsample for study",
                data=age_local,
                mock=mock_local
        )]
    )
    print("Dataset metadata has been defined! (2/4)")
#-------------
#UPLOAD DATASET
    admin_client = sy.login(email="info@openmined.org", password="changethis", port=port)
    admin_client.upload_dataset(dataset= age_dataset)
    print("Test datasets have been uploaded to US Stats datasite! (3/4)")

#-------------
# CREATE DS ACCOUNT
    print("Creating Data Scientist account...")
    admin_client.register(
        name='Pro Beta Tester', 
        email='ds_tester@openmined.org', 
        password='probetatester',
        password_verify='probetatester'
    )
    print("Data Scientist account created! (4/4)")
    print("You may now begin the test!")


# DATA OWNER RESPONSE -------------------------------------------------        

def data_owner_response(port):
    print("Moderator Chan is reviewing requests...")
    
    #Login as Admin
    admin_client= sy.login(
        email="info@openmined.org", 
        password="changethis", 
        port=port
    )

    # Define list of requests
    items = admin_client.requests

    # Define function to approve request
    def approve_item(index):
        admin_client.requests[index].approve()
    
    # Iterate over the list with indices and apply the function
    for index, item in enumerate(items):
        approve_item(index)

    print("Moderator Chan has finished reviewing requests!")
    print("You may begin Part Two of the test.")




#CONFIRMATION ----------------------------------------------------------------------------------------
print("Test Environment functions have been created!")