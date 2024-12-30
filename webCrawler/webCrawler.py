import json
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

# File management
current_directory = os.getcwd()
print(f"Current directory: {current_directory}")
# Google search params
query = "pottery classes"
technologies = json.load(open(current_directory + "\\technologies.json"))
locations = json.load(open(current_directory + "\\locations.json"))
max_pages = 1

# Function to scrape the Google search results for the specified query and technology keyword
def scrape_google_search(query, technologies, max_pages, locations):
    options = Options()
    options.headless = True
    service = Service(executable_path='path/to/chromedriver')
    browser = webdriver.Chrome(service=service, options=options)
    search_results = []

    for location in locations:
        try:
            encoded_query = query.replace(" ", "+")
            encoded_location = location['name'].replace(" ", "+")
            search_url = f"https://www.google.com/search?q={encoded_query}+in+{encoded_location}"
            browser.get(search_url)

            print(f"Getting search results for keywords: {query} located in {location['name']}.")

            has_next_page = True
            page_number = 1

            while has_next_page and page_number <= max_pages:
                new_results = browser.execute_script("""
                    let results = [];
                    document.querySelectorAll("div.g").forEach(result => {
                        try {
                            results.push({
                                title: result.querySelector("h3") ? result.querySelector("h3").innerText : "",
                                domain: result.querySelector("a") ? new URL(result.querySelector("a").href).hostname : "",
                                location: arguments[0],
                                link: result.querySelector("a") ? result.querySelector("a").href : ""
                            });
                        } catch (error) {
                            console.log(`Error adding: ${result} /n ${error.message}`);
                        }
                    });
                    return results;
                """, location['name'])

                search_results.extend(new_results)
                print(f"Results from page {page_number} added. Total results: {len(search_results)}")

                try:
                    next_page_link = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "a#pnnext"))
                    )
                    next_page_link.click()
                    page_number += 1
                except TimeoutException:
                    has_next_page = False

        except Exception as e:
            print(f"Invalid URL: {e}")
            continue

    final_results = get_tech_specific_links(search_results, technologies, browser)
    browser.quit()
    return final_results

# Function to get the search results for the specified technologies
def get_tech_specific_links(search_results, technologies, browser):
    final_results = []

    for technology in technologies:
        for search_result in search_results:
            print(f"Reviewing: {search_result['title']} for {technology['name']}.")

            try:
                browser.get(search_result['link'])
                has_technology_in_meta = browser.execute_script("""
                    const metaTags = document.querySelectorAll("meta");
                    return Array.from(metaTags).some(meta => meta.content.includes(arguments[0]));
                """, technology['name'])

                has_technology_in_script = browser.execute_script("""
                    const scriptTags = document.querySelectorAll("script");
                    return Array.from(scriptTags).some(script => script.textContent.includes(arguments[0]));
                """, technology['name'])

                if has_technology_in_meta or has_technology_in_script:
                    final_results.append(search_result)
                    print(f"Technology {technology['name']} found in {search_result['title']}.")

            except Exception as e:
                print(f"Error navigating to {search_result['link']}: {e}")

    return final_results

# Function to export the results to a CSV file
def export_results_to_csv(results, directory):
    df = pd.DataFrame(results)
    file_path = os.path.join(directory, "results.csv")

    if not os.path.exists(file_path):
        df.to_csv(file_path, index=False, mode='w', header=True)
    else:
        df.to_csv(file_path, index=False, mode='a', header=False)

    print(f"Results exported to {file_path}")

# Main execution
if __name__ == "__main__":
    final_results = scrape_google_search(query, technologies, max_pages, locations)
    export_results_to_csv(final_results, current_directory)