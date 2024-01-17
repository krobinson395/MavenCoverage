import psycopg2


def getTopURLS():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432",
            database="packages_production"
        )
    
        cursor = connection.cursor()
        
        # Execute the query and fetch the first 1000 results
        #The 2482 number is due to duplicates in the db the resulting set is 1000 results
        query = """SELECT repository_url
    FROM (
        SELECT DISTINCT repository_url, dependent_packages_count
        FROM packages
        WHERE ecosystem LIKE 'maven' AND repository_url LIKE '%github%'
    ) AS subquery
    ORDER BY dependent_packages_count DESC
    LIMIT 200;"""
    
        cursor.execute(query)
    
        # Fetch all the results
        rows = cursor.fetchall()
        github_urls = list(set(rows))
        
        print("Finished db query")
        return(github_urls)
    except psycopg2.Error as e:
        print(f"Error with db service: {e}")
        return(None)
    
if __name__ == "__main__":
    github_urls = getTopURLS()
    print(f"Total URLS {len(github_urls)}")
    file_path = 'PackageUrls.txt'

    with open(file_path, 'w') as file:
        for url in github_urls:
            file.write(url[0] + '\n')