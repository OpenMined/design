# Breaking down setup into different python functions
import syft as sy
import pandas as pd
from io import BytesIO

# CREATE DS ACCOUNTS ---------------------------------------------------------------------------------

# CREATE ABBY
def create_user(port):
    print("Creating external researcher profile...")
    admin_client = sy.login(email="info@openmined.org", password="changethis", port=port)

    admin_client.register(
        name='Diana Deets', 
        email='diana@openmined.org', 
        password='diana',
        password_verify= 'diana'
    )
    print("External researcher 'Diana' has been created!")


# CODE SUBMISSION ---------------------------------------------------------------------------------

def code_submission(port):

    # Login as data scientist user
    ds_client = sy.login(
        email= "diana@openmined.org", 
        password= "diana", 
        port=8080
    )
    print("External Researcher Diana has logged in! (1/3)")

    # Create Project
    description="I would like to study, per the legal agreement, the relationships between occupation and the life span of population."
    
    project = ds_client.create_project(
        name="Occupations & Life Span Relationship",
        description=description,
        user_email_address= "diana@openmined.org"
    )
    print("Diana has created a project, 'Occupations & Life Span Relationship'! (2/3)")

    # Create Syft Functions
    print("Diana is writing code for their project...")

    # Syft_Function 1 ----------------------------------------------------------------------------
    @sy.syft_function_single_use(data=ds_client.datasets[0].assets[0])
    def compute_short_lifespan_top_10_occupations(data: pd.DataFrame) -> BytesIO:
        # Dependencies
        import numpy as np
        import matplotlib.pyplot as plt
        from io import BytesIO
        import pandas as pd
        
        """
        Computes and plots the top 10 occupations with the shortest average lifespan.
        
        Args:
            data (pd.DataFrame): DataFrame containing 'Occupation' and 'Age of death' columns.
        
        Returns:
            BytesIO: In-memory PNG image of the plot.
        """
        if not {'Occupation', 'Age of death'}.issubset(data.columns):
            raise ValueError("DataFrame must contain 'Occupation' and 'Age of death' columns.")
        
        # Compute the mean lifespan by each occupation and get the top 10 shortest
        mean_life_span = (data.groupby('Occupation')['Age of death']
                          .mean()
                          .sort_values()
                          .head(10))
    
        # Plotting
        plt.figure(figsize=(15, 10))
        plt.title('Top 10 Occupations with Lowest Lifespan')
        plt.xlabel('Occupation')
        plt.ylabel('Average Lifespan')
        plt.style.use('ggplot')
    
        # Bar plot
        plt.bar(mean_life_span.index, mean_life_span.values, color='skyblue')
        plt.xticks(rotation=90)  # Rotate x-axis labels for readability
        plt.tight_layout()       # Adjust layout to prevent clipping
    
        # Save the plot to a BytesIO object
        figfile = BytesIO()
        plt.savefig(figfile, format='png')
        #plt.close()  # Close the plot to free up memory
        #figfile.seek(0)  # Rewind the BytesIO object to the beginning
    
        return figfile
    
        # Example usage:
        #compute_short_lifespan_top_10_occupations(data)


    # Syft_Function 2 ----------------------------------------------------------------------------   
    @sy.syft_function_single_use(data=ds_client.datasets[0].assets[0])
    def actuary_occupation(data):
        import numpy as np
        import matplotlib.pyplot as plt
    
        # Find all rows where the occupation is "Actuary"
        actuary = data[data['Occupation'] == 'Actuary']
    
        # Create the age of death distribution chart
        plt.figure(figsize=(10, 6))
        plt.hist(actuary['Age of death'], bins=range(int(data['Age of death'].min()), int(data['Age of death'].max()) + 1), edgecolor='black')
        actuary.to_csv('../actuary_sample.csv', index=False)
        plt.xlabel('Age of death')
        plt.ylabel('Number of People')
        plt.title('Age of Death Distribution for Actuaries')
        plt.grid(True)
        plt.tight_layout()
    
        # Save the plot to a file or display it
        plt.show()
    
        # Example Usage
        #actuary_occupation(data)

    # Syft_Function 3 ----------------------------------------------------------------------------   
    @sy.syft_function_single_use(data=ds_client.datasets[0].assets[0])
    def analyze_age_distribution(data):
        # Dependencies
        import numpy as np
        import matplotlib.pyplot as plt
        
        """
        Analyzes the age distribution and provides various insights.
        
        Args:
            data (pd.DataFrame): DataFrame containing 'Name' and 'Age of death' columns.
        """
        # Ensure the necessary columns are in the DataFrame
        if 'Name' not in data.columns or 'Age of death' not in data.columns:
            raise ValueError("DataFrame must contain 'Name' and 'Age of death' columns.")
        
        # Create the age distribution chart
        plt.figure(figsize=(10, 6))
        plt.hist(data['Age of death'], bins=range(int(data['Age of death'].min()), int(data['Age of death'].max()) + 1), edgecolor='black')
        plt.xlabel('Age of death')
        plt.ylabel('Number of People')
        plt.title('Age of Death Distribution')
        plt.grid(True)
        plt.tight_layout()
    
        # Save the plot to a file or display it
        plt.show()
    
        # Compute statistics
        oldest_age = data['Age of death'].max()
        youngest_age = data['Age of death'].min()
        
        num_oldest = len(data[data['Age of death'] == oldest_age])
        num_youngest = len(data[data['Age of death'] == youngest_age])
    
        # Print the number of people with the oldest and youngest age
        print(f"Number of people with the oldest age ({oldest_age}): {num_oldest}")
        print(f"Number of people with the youngest age ({youngest_age}): {num_youngest}")
        
        # Get the first five oldest people
        top_5_oldest = data.sort_values(by='Age of death', ascending=False).head(5)
        print("Names of the first five oldest people:")
        print(top_5_oldest['Name'].tolist())
        
        # Get the first five youngest people
        bottom_5_youngest = data.sort_values(by='Age of death').head(5)
        print("Names of the first five youngest people:")
        print(bottom_5_youngest['Name'].tolist())
    
    # SUBMIT CODE REQUESTS -----------------------------------------------------------------------
    project.create_code_request(compute_short_lifespan_top_10_occupations)
    project.create_code_request(analyze_age_distribution)
    project.create_code_request(actuary_occupation)
    print("Diana has submitted their code for review! (3/3)")
    print("→→ You may now begin Part Two of the Mission.")



#CONFIRMATION ----------------------------------------------------------------------------------------
print("Test Environment functions have been created!")