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
        name='Abby Asher', 
        email='abby@openmined.org', 
        password='abby',
        password_verify= 'abby'
    )
    print("External researcher 'Abby' has been created!")


# CODE SUBMISSION ---------------------------------------------------------------------------------

def code_submission(port):

    # Login as data scientist user
    ds_client = sy.login(
        email="abby@openmined.org", 
        password="abby", 
        port=8080
    )
    print("External Researcher Abby has logged in! (1/3)")

    # Create Project
    description="I would like to study, per the legal agreement, the relationships between occupation and the life span of population."
    
    project = ds_client.create_project(
        name="Occupations & Life Span Relationship",
        description=description,
        user_email_address= "abby@openmined.org"
    )
    print("Abby has created a project, 'Occupations & Life Span Relationship'! (2/3)")

    # Create Syft Functions
    print("Abby is writing code for her project...")

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
    def actuary_life_span(data):
        import numpy as np  # Import inside the function
    
        # Find all rows where the occupation is "Actuary"
        actuary = data[data['Occupation'] == 'Actuary']
        
        # Calculate the mean age of death for actuaries
        mean_age_of_death = actuary['Age of death'].mean()
        
        # Calculate the mean life expectancy of the associated country for actuaries
        country_of_origin_mean = actuary['Associated Country Life Expectancy'].mean()
    
        return mean_age_of_death, country_of_origin_mean
        
        # Example usage
        #actuary_life_span(data)

    # Syft_Function 3 ----------------------------------------------------------------------------   
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

    # SUBMIT CODE REQUESTS -----------------------------------------------------------------------
    project.create_code_request(compute_short_lifespan_top_10_occupations)
    project.create_code_request(actuary_life_span)
    project.create_code_request(long_lifespan)
    print("Abby has submitted her code for review! (3/3)")
    print("→→ You may now begin Part Two of the Mission.")



#CONFIRMATION ----------------------------------------------------------------------------------------
print("Test Environment functions have been created!")