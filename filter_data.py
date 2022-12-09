
import pandas as pd 


def main():

    filename = './data/amenities-vancouver.json.gz'
    
    data = pd.read_json(filename, lines=True, orient='records', compression='gzip')
    
    data['amenity'] = data['amenity'].astype('string')
    # problems with one particular string
    data[(data['lat'] == 49.2653026) & (data['lon'] == -123.1453865)] = 'Carlos OBryans Neighborhood Pub'
    data.to_json('./data/amenities-vancouver_n.json.gz',orient='records', lines=True, compression='gzip') # save that change

    amenities = set(data['amenity'])
    
    # Create different categories for amenities
    # (To create a new category: create the list, modify 'others' and modify 'categories')
    
    food = ['bar',  'bbq',  'biergarten',  'bistro',  'cafe',  'car_rental',  'fast_food',  'food_court',  'ice_cream', \
            'internet_cafe',  'juice_bar',  'restaurant',  'vending_machine']
    transport = ['bicycle_parking',  'bicycle_rental', 'bicycle_repair_station',  'boat_rental',  'bus_station', 'car_rep', \
                'car_sharing',  'car_wash',  'charging_station',  'ferry_terminal',  'fuel',  'loading_dock', \
                 'motorcycle_parking',  'motorcycle_rental',  'parking',  'parking_entrance',  'parking_space', \
                 'seaplane terminal',  'taxi']
    education = ['college', 'cram_school',  'driving_school', 'kindergarten', 'language_school',  'library', 'music_school',\
                 'prep_school',  'research_institute',  'school',  'science',  'university']
    store = ['marketplace', 'shop|clothes']
    entertainment = ['Observation Platform',  'arts_centre',  'bar',  'biergarten',  'bistro',  'casino', 'cinema',  'clock', \
                     'gambling',  'gym',  'leisure',  'meditation_centre', 'nightclub',  'park',  'playground',  'pub', \
                    'social_centre',  'spa',  'stripclub',  'theatre']
    health = ['Pharmacy',  'pharmacy', 'chiropractor', 'clinic',  'dentist', 'doctors',  'first_aid',  'healthcare',  'hospital', \
              'nursery']
    payment = ['atm', 'atm;bank', 'bank',  'bureau_de_change',  'money_transfer',  'payment_terminal']
    
    # The last one is just the rest
    others = amenities - set(food) - set(transport) - set(education) - set(store) - set(entertainment)\
    - set(health) - set(payment)
    
    # Create dict with all of them
    categories = {'others' : others, 'food': food, 'transport': transport, 'education': education, 'store': store,\
                  'entertainment': entertainment, 'health':health , 'payment': payment}
     
        
    # Save different datasets
    
    for category, amenity_types in categories.items(): # iterate the dict
        subset_data = data[data['amenity'].isin(amenity_types)].copy()  # get the data
        if subset_data.shape[0] > 0: # There are places with that ammenity type(s)
            subset_data.to_json('./data/data_' + str(category) + '.json',orient='records', lines=True, compression='gzip') # save


if __name__ == '__main__':
    main()





