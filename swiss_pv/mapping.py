import pandas as pd

roof_tilt_map = pd.read_csv('data/roof_tilt_map.csv')

roof_aspect_map = pd.read_csv('data/roof_aspect_map.csv')

def get_roof_aspect_tilt_classes(df_roof):

    df_roof = df_roof.copy()

    for indx in df_roof.index:
        roof_tilt_value = df_roof.at[indx, 'ROOF_TILT']
        roof_aspect_value = df_roof.at[indx, 'ROOF_ASPECT']
        
        # Find tilt class
        tilt_class = roof_tilt_map[(roof_tilt_map['min'] <= roof_tilt_value) & 
                                    (roof_tilt_map['max'] > roof_tilt_value)]['tilt_class'].values[0]
        # Find aspect class
        aspect_class = roof_aspect_map[(roof_aspect_map['min'] <= roof_aspect_value) & 
                                        (roof_aspect_map['max'] > roof_aspect_value)]['aspect_class'].values[0]

        if tilt_class == 0:
            aspect_class = 'flat'
            
        df_roof.at[indx, 'ROOF_TILT_CLASS'] = tilt_class
        df_roof.at[indx, 'ROOF_ASPECT_CLASS'] = aspect_class

    df_roof['ROOF_TILT_CLASS'] = df_roof['ROOF_TILT_CLASS'].astype(int)    

    return df_roof