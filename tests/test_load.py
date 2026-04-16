import sys
sys.path.insert(0, ".") 

from app.data_processing import load_data, clean_data, merge_seasons, enrich_data

countries, summer, winter, ol_codes = load_data()
countries, summer, winter           = clean_data(countries, summer, winter)
all_olympics                        = merge_seasons(summer, winter, ol_codes)
all_olympics, medals_only           = enrich_data(all_olympics)

print(medals_only[["Year", "Season", "Country", "Athlete", "Medal"]].head(10))