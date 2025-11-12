# this is the script for aggregating various datasets into a single dataframe

import pandas as pd
import geopandas as gpd


class DataAggregator():
    def __init__(self, index_name: str='EGID', index_type=int):

        print(f"Initializing DataAggregator... with index: {index_name}")

        self.setup = {
            'show log': False
        }

        self.index_name = index_name
        self.index_type = index_type

        self.aggregated_data = pd.DataFrame(index=pd.Index([], name=index_name))
        self.datasets = {}  # dictionary of dataframes
        self.data_records = {}  # dictionary to store metadata about datasets
        self.log = []  # list to store log messages

        
    def add_log(self, message: str):
        """Add a log message with timestamp"""
        timestamp = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        str_log = f"[{timestamp}] {message}"
        
        if self.setup['show log']:  print(str_log)
        else: print(str_log)

        self.log.append(str_log)

    def add_dataset(self, dataset_name: str, path: str, description: str, override=True, **kwargs):
        """Add a dataset to the aggregator from a file"""

        # check if dataset already exists
        if dataset_name in self.datasets:
            self.add_log(f"Dataset {dataset_name} already exists.")

            if override:
                self.add_log(f'Overriding existing dataset "{dataset_name}".')
            else:
                self.add_log(f'Skipping loading dataset "{dataset_name}".')
                return
            
        # save data info
        self.data_records[dataset_name] = {
            'path': path,
            'description': description
        }
        
        ## step 1: load data
        if path.endswith('.csv'):
            data = pd.read_csv(path, **kwargs)
        elif path.endswith('.xlsx'):
            data = pd.read_excel(path, **kwargs)
        elif path.endswith('.parquet'):
            data = pd.read_parquet(path, **kwargs)
        elif path.endswith('.geojson') or path.endswith('.json'):
            data = gpd.read_file(path, **kwargs)
        else:
            raise ValueError(f"Unsupported file format for {path}")

        self.datasets[dataset_name] = data

        return data


    def merge_dataset_by_index(self, dataset_name: str, header_index: str=None, merge_how='outer'):
        """Aggregate a dataset into the main aggregated_data dataframe, based on the index column (e.g. EGID)
        
        """
        
        data = self.datasets[dataset_name].copy()
        shape_before = self.aggregated_data.shape
        
        # check if index_col_name is provided
        if header_index is None:
            header_index = self.index_name

        ## set up index
        # check if index_col_name is in the data
        if header_index in data.columns:
            data.rename(columns={header_index: self.index_name}, inplace=True)
            data.set_index(self.index_name, inplace=True)
        else:
            self.add_log(f"Index column {header_index} not found in dataset {dataset_name}.")
            self.add_log(f"Use existing index.")

        data.index = data.index.astype(self.index_type)
        

        data.insert(0, f'dataset: {dataset_name}', 1)

        self.aggregated_data = self.aggregated_data.merge(data, left_index=True, right_index=True,
                                                          how=merge_how, suffixes=('', f'_{dataset_name}'))
        
        shape_after = self.aggregated_data.shape
        self.add_log(f"Aggregated dataset '{dataset_name}': {shape_before} -> {shape_after}")

    
    def merge_dataset_by_geometry(self, dataset_name: str, header_geometry: str='geometry', header_point: str='geometry',
                                  method: str='search'):
        """Aggregate a dataset into the main aggregated_data dataframe, based on spatial join of geometries

        input:
        -----
        dataset_name: name of the dataset (in `self.datasets`) to merge
        header_geometry: column name of the geometry data in `self.aggregated_data`
        header_point: column name of the geometry data in the dataset to merge
        """
        
        data = self.datasets[dataset_name].copy()
        agg = self.aggregated_data
        shape_before = agg.shape

        # check if `aggregated_data` has geometry column
        if header_geometry not in agg.columns:
            self.add_log(f"Geometry column {header_geometry} not found in aggregated data.")
            self.add_log(f"Skipping spatial merge.")
            return
        
        # check if header_point is provided
        if header_point not in data.columns:
            self.add_log(f"Point column {header_point} not found in dataset {dataset_name}.")
            self.add_log(f"Skipping spatial merge.")
            return
        

        aggregated_gdf = gpd.GeoDataFrame(agg, geometry=header_geometry)
        
        ## --- method 1 sjoin ---
        # more efficient for large datasets, but has issues that some points are missing
        if method == 'sjoin':

            ## set up geometry
            data_gdf = gpd.GeoDataFrame(data, geometry=header_point)
            data_gdf.insert(0, f'dataset: {dataset_name}', 1)            

            # perform spatial join
            merged_gdf = gpd.sjoin(aggregated_gdf, data_gdf, how='left', predicate='intersects', lsuffix='', rsuffix=dataset_name)

            agg = pd.DataFrame(merged_gdf)

        ## --- method 2 search ---
        # less efficient, but more reliable
        elif method == 'search':

            for indx, row in data.iterrows():
                point = row[header_point]

                # find matching geometries in aggregated_data
                matches = agg[agg[header_geometry].intersects(point)]

                print(len(matches))
                print(matches)

                data.loc[indx, 'EGID'] = matches.index.tolist()

            return data


        shape_after = agg.shape
        self.aggregated_data = agg
        self.add_log(f"Spatially merged dataset '{dataset_name}': {shape_before} -> {shape_after}")