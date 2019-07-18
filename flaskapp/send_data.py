from flaskapp.get_info.store import Store

def convert_json(store):
    json_data =  {
            'name' : store.get_name(),
            'address' : store.get_address(),
            'icon' : store.get_icon(),
            'rating' : store.get_rating(),
            'reviews' : store.get_reviews(),
            'type' : store.get_types()
            }
    return json_data
