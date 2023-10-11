import pandas as pd
import country_converter as coco
import geopandas as gpd
import pygal
import matplotlib.pyplot as plt
import adjustText

country_most_popular_ris = pd.read_csv('all_data_manual_software.csv')[
    ['organisation_country', 'repository_metadata_software_name']]

lat_long_per_country = pd.read_csv('data/countries_latitude_longitude.csv')


country_most_popular_ris = country_most_popular_ris.assign(
    country_name=coco.convert(names=country_most_popular_ris['organisation_country'], to='name_short'))

uq_countries = country_most_popular_ris['organisation_country'].nunique()

print('\n\n\n\n\n\n', uq_countries, '\n\n\n\n\n\n')

print(country_most_popular_ris)


grouped = country_most_popular_ris.groupby(
    ['country_name', 'repository_metadata_software_name']).size().reset_index(name='count')


def get_top(group):
    # Sort the group by count in descending order
    sorted_group = group.sort_values(by='count', ascending=False)
    # Take the top three rows
    top_one = sorted_group.head(1)
    return top_one


top_per_country = grouped.groupby('country_name', as_index=False).apply(
    get_top).reset_index(drop=True)
print(top_per_country)

country_most_popular_ris_with_coords = pd.merge(top_per_country, lat_long_per_country,
                                                left_on='country_name', right_on='name')
print(country_most_popular_ris_with_coords)

world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
world.columns = ['pop_est', 'continent',
                 'name', 'CODE', 'gdp_md_est', 'geometry']
print(world)

fig, ax = plt.subplots(figsize=(8, 6))

world.plot(color='lightgrey', ax=ax)


# merged = pd.merge(top_per_country, world,left_on='country_name', right_on='name')
# print(merged)

country_most_popular_ris_with_coords.plot(x='longitude', y='latitude', kind='scatter', label='repository_metadata_software_name',
                                          figsize=(25, 20),
                                          legend=True, ax=ax)

for i in range(0, 103):
    plt.text(float(country_most_popular_ris_with_coords.longitude[i]), float(country_most_popular_ris_with_coords.latitude[i]), "{}\n{}".format(
        country_most_popular_ris_with_coords.name[i], country_most_popular_ris_with_coords.repository_metadata_software_name[i]), size=10)


plt.show()
