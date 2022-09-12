class binary_enc(BaseEstimator, TransformerMixin):
    def __init__(self,columns):
        self.columns = columns
    def fit(self,df,y=None):
        self.encoder = OrdinalEncoder(handle_unknown='value',cols=self.columns,drop_invariant=True)
        self.encoder = self.encoder.fit(df)
        return self
    def transform(self,df,y=None):
        df_ = df.copy()
        df_ = self.encoder.transform(df_)
        df_[self.columns]= df_[self.columns]-1
        return df_




class scaler(BaseEstimator, TransformerMixin):
    def fit(self,df,*kargs):
        self.encoder = StandardScaler()
        self.encoder = self.encoder.fit(df)
        return self
    def transform(self,df,*kargs):
        df_ = df.copy()
        df_ = pd.DataFrame(self.encoder.transform(df_),columns=df_.columns,index=df_.index)
        return df_

class drop_columns(BaseEstimator, TransformerMixin):
    def __init__(self,columns):
        self.columns = columns
    def fit(self,df,*kargs):
        return self
    def transform(self,df,*kargs):
        df_ = df.copy()
        return df_.drop(self.columns,axis=1)

    
class mortality_feats(BaseEstimator, TransformerMixin):
    def fit(self,df,*kargs):
        return self
    
    def transform(self,df,*kargs):
        df_ = df.copy()
        city_mort = pd.read_csv('mortality_per_city.csv',index_col=0)
        

        df_['city_mortality']= [city_mort.loc[l].mortality if l in list(city_mort.index) else np.nan for l in df_.InterventionLocationName ]
        #city_mort.loc[df_.InterventionLocationName].set_index(df_.index)     
        return df_

class create_date_feats(BaseEstimator, TransformerMixin):
    def __init__(self,column):
        self.column = column
    def fit(self,df,*kargs):


        return self
    def transform(self,df,*kargs):
        df_ = df.copy()
        df_[self.column]= pd.to_datetime(df_[self.column])
        df_['day_of_year'] = df_[self.column].dt.dayofyear
        df_['hour'] = df_[self.column].dt.hour
        df_['day_of_year_cos'] = np.cos(2*np.pi*df_['day_of_year']/365)
        df_['day_of_year_sin'] = np.sin(2*np.pi*df_['day_of_year']/365)
        #df_['hour_cos'] = np.cos(2*np.pi*df_['hour']/24)
        #df_['hour_sin'] = np.sin(2*np.pi*df_['hour']/24)        
        return df_    
    
def four_races(df):
    if(df.SubjectEthnicityCode=='H'):
        return 'H'
    elif(df.SubjectRaceCode=='W'):
        return 'W'
    elif(df.SubjectRaceCode=='B'):
        return('B')

    else:
        return 'O'

def correct_statute(df):
    if df == 'Other':
        return 'Other/Error'
    else:
        return df