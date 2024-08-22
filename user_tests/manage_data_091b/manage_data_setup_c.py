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
        name='Carl Jung', 
        email='carl@openmined.org', 
        password='carl',
        password_verify= 'carl'
    )
    print("External researcher 'Carl' has been created!")


# CODE SUBMISSION ---------------------------------------------------------------------------------

def code_submission(port):

    # Login as data scientist user
    ds_client = sy.login(
        email= "carl@openmined.org", 
        password= "carl", 
        port=8080
    )
    print("External Researcher Carl has logged in! (1/3)")

    # Create Project
    description="I would like to study, per the legal agreement, the relationships between occupation and the life span of population."
    
    project = ds_client.create_project(
        name="Occupations & Life Span Relationship",
        description=description,
        user_email_address= "carl@openmined.org"
    )
    print("Carl has created a project, 'Occupations & Life Span Relationship'! (2/3)")

    # Create Syft Functions
    print("Carl is writing code for his project...")

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
    def long_lifespan(data):
        import numpy as np
        import matplotlib.pyplot as plt
        life_span = data.groupby('Occupation')['Age of death'].mean().sort_values(ascending=False)[:10]
        plt.title('Top 10 Occupations with Longest Life Span')
        plt.xlabel('Occupation')
        plt.ylabel('Average Life Span')
        plt.bar(life_span.index, life_span)
        plt.xticks(rotation='vertical')

    # Syft_Function 3 ----------------------------------------------------------------------------   
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
    
    # SUBMIT CODE REQUESTS -----------------------------------------------------------------------
    project.create_code_request(compute_short_lifespan_top_10_occupations)
    project.create_code_request(long_lifespan)
    project.create_code_request(actuary_occupation)
    print("Carl has submitted his code for review! (3/3)")
    print("→→ You may now begin Part Two of the Mission.")



#CONFIRMATION ----------------------------------------------------------------------------------------
print("Test Environment functions have been created!")